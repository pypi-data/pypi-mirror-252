import re

from pyimportcyclefinder.protocol.base.re import (
    BasePatternProtocol
)
from pyimportcyclefinder.protocol.base.regex import (
    BaseExtendedPatternProtocol
)
from pyimportcyclefinder.protocol.re import PatternProtocol
from pyimportcyclefinder.protocol.regex import (
    ExtendedPatternProtocol
)
import pytest
import regex


@pytest.fixture()
def re_and_regex_instances():
    test_str = "THING"
    rep = re.compile(".*HIN.*")
    regexp = regex.compile(".*HIN.*", flags=regex.V1)
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
        assert (issubclass(re.Pattern, BasePatternProtocol))

    @staticmethod
    def test_re_pattern_type_not_subclass_of_base_extended_pattern_protocol():
        assert (not issubclass(re.Pattern, BaseExtendedPatternProtocol))

    @staticmethod
    def test_regex_pattern_type_subclass_of_base_pattern_protocol():
        assert (issubclass(regex.Pattern, BasePatternProtocol))

    @staticmethod
    def test_regex_pattern_type_subclass_of_base_extended_pattern_protocol():
        assert (issubclass(regex.Pattern, BaseExtendedPatternProtocol))

    @staticmethod
    def test_base_pattern_protocol_not_subclass_of_re_pattern_type():
        assert (not issubclass(BasePatternProtocol, re.Pattern))

    @staticmethod
    def test_base_pattern_protocol_not_subclass_of_regex_pattern_type():
        assert (not issubclass(BasePatternProtocol, regex.Pattern))

    @staticmethod
    def test_base_extended_pattern_protocol_not_subclass_of_re_pattern_type():
        assert (not issubclass(BaseExtendedPatternProtocol, re.Pattern))

    @staticmethod
    def test_base_extended_pattern_protocol_not_subclass_of_regex_pattern_type():
        assert (not issubclass(BaseExtendedPatternProtocol, regex.Pattern))

    @staticmethod
    def test_base_extended_pattern_protocol_subclass_of_base_pattern_protocol():
        assert (issubclass(BaseExtendedPatternProtocol, BasePatternProtocol))

    @staticmethod
    def test_base_pattern_protocol_not_subclass_of_base_extended_pattern_protocol():
        assert (not issubclass(BasePatternProtocol, BaseExtendedPatternProtocol))

    @staticmethod
    def test_re_pattern_instance_of_base_pattern_protocol(re_and_regex_instances):
        assert (isinstance(re_and_regex_instances["re_pattern_instance"], BasePatternProtocol))

    @staticmethod
    def test_re_pattern_instance_of_pattern_protocol(re_and_regex_instances):
        assert (isinstance(re_and_regex_instances["re_pattern_instance"], PatternProtocol))

    @staticmethod
    def test_re_pattern_not_instance_of_extended_base_pattern_protocol(re_and_regex_instances):
        assert (
                not isinstance(
                        re_and_regex_instances["re_pattern_instance"], BaseExtendedPatternProtocol
                )
        )

    @staticmethod
    def test_re_pattern_not_instance_of_extended_pattern_protocol(re_and_regex_instances):
        assert (
                not isinstance(
                        re_and_regex_instances["re_pattern_instance"], ExtendedPatternProtocol
                        ))

    @staticmethod
    def test_regex_pattern_instance_of_base_pattern_protocol(re_and_regex_instances):
        assert (isinstance(re_and_regex_instances["regex_pattern_instance"], BasePatternProtocol))

    @staticmethod
    def test_regex_pattern_instance_of_pattern_protocol(re_and_regex_instances):
        assert (isinstance(re_and_regex_instances["regex_pattern_instance"], PatternProtocol))

    @staticmethod
    def test_regex_pattern_instance_of_base_extended_pattern_protocol(re_and_regex_instances):
        assert (isinstance(
                re_and_regex_instances["regex_pattern_instance"], BaseExtendedPatternProtocol
                ))

    @staticmethod
    def test_regex_pattern_instance_of_extended_pattern_protocol(re_and_regex_instances):
        assert (
                isinstance(
                        re_and_regex_instances["regex_pattern_instance"], ExtendedPatternProtocol
                        ))
