from typing import TYPE_CHECKING  # noqa:F401

from ddtrace.internal.compat import pattern_type
from ddtrace.internal.constants import MAX_UINT_64BITS as _MAX_UINT_64BITS
from ddtrace.internal.glob_matching import GlobMatcher
from ddtrace.internal.logger import get_logger
from ddtrace.internal.utils.cache import cachedmethod
from ddtrace.internal.utils.deprecations import DDTraceDeprecationWarning
from ddtrace.vendor.debtcollector import deprecate


if TYPE_CHECKING:  # pragma: no cover
    from typing import Any  # noqa:F401
    from typing import Optional  # noqa:F401
    from typing import Tuple  # noqa:F401

    from ddtrace._trace.span import Span  # noqa:F401

log = get_logger(__name__)
KNUTH_FACTOR = 1111111111111111111


class SamplingRule(object):
    """
    Definition of a sampling rule used by :class:`DatadogSampler` for applying a sample rate on a span
    """

    NO_RULE = object()

    def __init__(
        self,
        sample_rate,  # type: float
        service=NO_RULE,  # type: Any
        name=NO_RULE,  # type: Any
        resource=NO_RULE,  # type: Any
        tags=NO_RULE,  # type: Any
        provenance="default",  # type: str
    ):
        # type: (...) -> None
        """
        Configure a new :class:`SamplingRule`

        .. code:: python

            DatadogSampler([
                # Sample 100% of any trace
                SamplingRule(sample_rate=1.0),

                # Sample no healthcheck traces
                SamplingRule(sample_rate=0, name='flask.request'),

                # Sample all services ending in `-db` based on a regular expression
                SamplingRule(sample_rate=0.5, service=re.compile('-db$')),

                # Sample based on service name using custom function
                SamplingRule(sample_rate=0.75, service=lambda service: 'my-app' in service),
            ])

        :param sample_rate: The sample rate to apply to any matching spans
        :type sample_rate: :obj:`float` greater than or equal to 0.0 and less than or equal to 1.0
        :param service: Rule to match the `span.service` on, default no rule defined
        :type service: :obj:`object` to directly compare, :obj:`function` to evaluate, or :class:`re.Pattern` to match
        :param name: Rule to match the `span.name` on, default no rule defined
        :type name: :obj:`object` to directly compare, :obj:`function` to evaluate, or :class:`re.Pattern` to match
        :param tags: A dictionary whose keys exactly match the names of tags expected to appear on spans, and whose
            values are glob-matches with the expected span tag values. Glob matching supports "*" meaning any
            number of characters, and "?" meaning any one character. If all tags specified in a SamplingRule are
            matches with a given span, that span is considered to have matching tags with the rule.
        """
        # Enforce sample rate constraints
        if not 0.0 <= sample_rate <= 1.0:
            raise ValueError(
                (
                    "SamplingRule(sample_rate={}) must be greater than or equal to 0.0 and less than or equal to 1.0"
                ).format(sample_rate)
            )
        self.sample_rate = float(sample_rate)
        # since span.py converts None to 'None' for tags, and does not accept 'None' for metrics
        # we can just create a GlobMatcher for 'None' and it will match properly
        self._tag_value_matchers = (
            {k: GlobMatcher(str(v)) for k, v in tags.items()} if tags != SamplingRule.NO_RULE else {}
        )
        self.tags = tags
        self.service = self.choose_matcher(service)
        self.name = self.choose_matcher(name)
        self.resource = self.choose_matcher(resource)
        self.provenance = provenance

    @property
    def sample_rate(self):
        # type: () -> float
        return self._sample_rate

    @sample_rate.setter
    def sample_rate(self, sample_rate):
        # type: (float) -> None
        self._sample_rate = sample_rate
        self._sampling_id_threshold = sample_rate * _MAX_UINT_64BITS

    def _pattern_matches(self, prop, pattern):
        # If the rule is not set, then assume it matches
        # DEV: Having no rule and being `None` are different things
        #   e.g. ignoring `span.service` vs `span.service == None`
        if pattern is self.NO_RULE:
            return True
        if isinstance(pattern, GlobMatcher):
            return pattern.match(str(prop))

        # If the pattern is callable (e.g. a function) then call it passing the prop
        #   The expected return value is a boolean so cast the response in case it isn't
        if callable(pattern):
            try:
                return bool(pattern(prop))
            except Exception:
                log.warning("%r pattern %r failed with %r", self, pattern, prop, exc_info=True)
                # Their function failed to validate, assume it is a False
                return False

        # The pattern is a regular expression and the prop is a string
        if isinstance(pattern, pattern_type):
            try:
                return bool(pattern.match(str(prop)))
            except (ValueError, TypeError):
                # This is to guard us against the casting to a string (shouldn't happen, but still)
                log.warning("%r pattern %r failed with %r", self, pattern, prop, exc_info=True)
                return False

        # Exact match on the values
        return prop == pattern

    @cachedmethod()
    def _matches(self, key):
        # type: (Tuple[Optional[str], str, Optional[str]]) -> bool
        # self._matches exists to maintain legacy pattern values such as regex and functions
        service, name, resource = key
        for prop, pattern in [(service, self.service), (name, self.name), (resource, self.resource)]:
            if not self._pattern_matches(prop, pattern):
                return False
        else:
            return True

    def matches(self, span):
        # type: (Span) -> bool
        """
        Return if this span matches this rule

        :param span: The span to match against
        :type span: :class:`ddtrace._trace.span.Span`
        :returns: Whether this span matches or not
        :rtype: :obj:`bool`
        """
        tags_match = self.tags_match(span)
        return tags_match and self._matches((span.service, span.name, span.resource))

    def tags_match(self, span):
        # type: (Span) -> bool
        tag_match = True
        if self._tag_value_matchers:
            tag_match = self.check_tags(span.get_tags(), span.get_metrics())
        return tag_match

    def check_tags(self, meta, metrics):
        if meta is None and metrics is None:
            return False

        tag_match = False
        for tag_key in self._tag_value_matchers.keys():
            value = meta.get(tag_key)
            tag_match = self._tag_value_matchers[tag_key].match(str(value))
            # If the value doesn't match in meta, check the metrics
            if tag_match is False:
                value = metrics.get(tag_key)
                # Floats: Matching floating point values with a non-zero decimal part is not supported.
                # For floating point values with a non-zero decimal part, any all * pattern always returns true.
                # Other patterns always return false.
                if isinstance(value, float):
                    if not value.is_integer():
                        if self._tag_value_matchers[tag_key].pattern == "*":
                            tag_match = True
                        else:
                            return False
                        continue
                    else:
                        value = int(value)

                tag_match = self._tag_value_matchers[tag_key].match(str(value))
            else:
                continue
            # if we don't match with all specified tags for a rule, it's not a match
            if tag_match is False:
                return False

        return tag_match

    def sample(self, span):
        """
        Return if this rule chooses to sample the span

        :param span: The span to sample against
        :type span: :class:`ddtrace._trace.span.Span`
        :returns: Whether this span was sampled
        :rtype: :obj:`bool`
        """
        if self.sample_rate == 1:
            return True
        elif self.sample_rate == 0:
            return False

        return ((span._trace_id_64bits * KNUTH_FACTOR) % _MAX_UINT_64BITS) <= self._sampling_id_threshold

    def _no_rule_or_self(self, val):
        if val is self.NO_RULE:
            return "NO_RULE"
        elif val is None:
            return "None"
        elif type(val) == GlobMatcher:
            return val.pattern
        else:
            return val

    def choose_matcher(self, prop):
        # We currently support the ability to pass in a function, a regular expression, or a string
        # If a string is passed in we create a GlobMatcher to handle the matching
        if callable(prop) or isinstance(prop, pattern_type):
            # deprecated: passing a function or a regular expression'
            deprecate(
                "Using methods or regular expressions for SamplingRule matching is deprecated. ",
                message="Please move to passing in a string for Glob matching.",
                removal_version="3.0.0",
                category=DDTraceDeprecationWarning,
            )
            return prop
        # Name and Resource will never be None, but service can be, since we str()
        #  whatever we pass into the GlobMatcher, we can just use its matching
        elif prop is None:
            prop = "None"
        else:
            return GlobMatcher(prop) if prop != SamplingRule.NO_RULE else SamplingRule.NO_RULE

    def __repr__(self):
        return "{}(sample_rate={!r}, service={!r}, name={!r}, resource={!r}, tags={!r}, provenance={!r})".format(
            self.__class__.__name__,
            self.sample_rate,
            self._no_rule_or_self(self.service),
            self._no_rule_or_self(self.name),
            self._no_rule_or_self(self.resource),
            self._no_rule_or_self(self.tags),
            self.provenance,
        )

    __str__ = __repr__

    def __eq__(self, other):
        # type: (Any) -> bool
        if not isinstance(other, SamplingRule):
            raise TypeError("Cannot compare SamplingRule to {}".format(type(other)))
        return str(self) == str(other)
