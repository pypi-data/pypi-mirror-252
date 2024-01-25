import re
from typing import Union

from pyimportcyclefinder.protocol.base.re import (
    ReBuiltInBasePatternProtocol
)
from pyimportcyclefinder.protocol.base.regex import (
    BaseRegexPackagePatternProtocol
)
from pyimportcyclefinder.protocol.re import ReBuiltInPatternProtocol
from pyimportcyclefinder.protocol.regex import (
    RegexPackagePatternProtocol
)
import pytest
import regex

AnyRePattern = Union[ReBuiltInBasePatternProtocol, RegexPackagePatternProtocol]


@pytest.fixture()
def re_and_regex_instances():
    test_str = "THING"
    rep = re.compile(".*HIN.*")
    regexp = regex.compile(".*HIN.*")
    return {
            're_pattern_instance': rep,
            'regex_pattern_instance': regexp,
            're_match_instance': rep.match(test_str),
            'regex_match_instance': regexp.match(test_str),
            're_scanner_instance': rep.scanner(test_str),
            'regex_scanner_instance': regexp.scanner(test_str),
            'regex_splitter_instance': regexp.splititer(test_str)
    }


class TestPatternProtocolsAndTypes:
    @staticmethod
    def test_re_pattern_type_subclass_of_base_pattern_protocol():
        assert (issubclass(re.Pattern, ReBuiltInBasePatternProtocol))

    @staticmethod
    def test_re_pattern_type_not_subclass_of_base_extended_pattern_protocol():
        assert (not issubclass(re.Pattern, BaseRegexPackagePatternProtocol))

    @staticmethod
    def test_regex_pattern_type_subclass_of_base_pattern_protocol():
        assert (issubclass(regex.Pattern, ReBuiltInBasePatternProtocol))

    @staticmethod
    def test_regex_pattern_type_subclass_of_base_extended_pattern_protocol():
        assert (issubclass(regex.Pattern, BaseRegexPackagePatternProtocol))

    @staticmethod
    def test_base_pattern_protocol_not_subclass_of_re_pattern_type():
        assert (not issubclass(ReBuiltInBasePatternProtocol, re.Pattern))

    @staticmethod
    def test_base_pattern_protocol_not_subclass_of_regex_pattern_type():
        assert (not issubclass(ReBuiltInBasePatternProtocol, regex.Pattern))

    @staticmethod
    def test_base_extended_pattern_protocol_not_subclass_of_re_pattern_type():
        assert (not issubclass(BaseRegexPackagePatternProtocol, re.Pattern))

    @staticmethod
    def test_base_extended_pattern_protocol_not_subclass_of_regex_pattern_type():
        assert (not issubclass(BaseRegexPackagePatternProtocol, regex.Pattern))

    @staticmethod
    def test_base_extended_pattern_protocol_subclass_of_base_pattern_protocol():
        assert (issubclass(BaseRegexPackagePatternProtocol, ReBuiltInBasePatternProtocol))

    @staticmethod
    def test_base_pattern_protocol_not_subclass_of_base_extended_pattern_protocol():
        assert (not issubclass(ReBuiltInBasePatternProtocol, BaseRegexPackagePatternProtocol))

    @staticmethod
    def test_re_pattern_instance_of_base_pattern_protocol(re_and_regex_instances):
        assert (
                isinstance(
                        re_and_regex_instances["re_pattern_instance"],
                        ReBuiltInBasePatternProtocol
                )
        )

    @staticmethod
    def test_re_pattern_instance_of_pattern_protocol(re_and_regex_instances):
        assert (
                isinstance(
                        re_and_regex_instances["re_pattern_instance"],
                        ReBuiltInPatternProtocol
                )
        )

    @staticmethod
    def test_re_pattern_not_instance_of_extended_base_pattern_protocol(re_and_regex_instances):
        assert (
                not isinstance(
                        re_and_regex_instances["re_pattern_instance"],
                        BaseRegexPackagePatternProtocol
                )
        )

    @staticmethod
    def test_re_pattern_not_instance_of_extended_pattern_protocol(re_and_regex_instances):
        assert (
                not isinstance(
                        re_and_regex_instances["re_pattern_instance"],
                        RegexPackagePatternProtocol
                        )
        )

    @staticmethod
    def test_regex_pattern_instance_of_base_pattern_protocol(re_and_regex_instances):
        assert (
                isinstance(
                        re_and_regex_instances["regex_pattern_instance"],
                        ReBuiltInBasePatternProtocol
                )
        )

    @staticmethod
    def test_regex_pattern_instance_of_pattern_protocol(re_and_regex_instances):
        assert (
                isinstance(
                        re_and_regex_instances["regex_pattern_instance"],
                        ReBuiltInPatternProtocol
                )
        )

    @staticmethod
    def test_regex_pattern_instance_of_base_extended_pattern_protocol(re_and_regex_instances):
        assert (
                isinstance(
                        re_and_regex_instances["regex_pattern_instance"],
                        BaseRegexPackagePatternProtocol
                )
        )

    @staticmethod
    def test_regex_pattern_instance_of_extended_pattern_protocol(re_and_regex_instances):
        assert (
                isinstance(
                        re_and_regex_instances["regex_pattern_instance"],
                        RegexPackagePatternProtocol
                )
        )
