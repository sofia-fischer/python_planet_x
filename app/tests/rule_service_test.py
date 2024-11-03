from unittest import TestCase

from app.services.board_service import GenerationService
from app.services.rule_service import RuleService
from app.valueObjects.rules import NotInSectorRule


class TestRuleService(TestCase):
    def test_rule_generate_start_rule(self) -> None:
        sectors = GenerationService().generate()
        rule = RuleService().generate_start_rule(sectors, [])

        assert rule is not None
        assert rule.valid(sectors) is None
        assert isinstance(rule, NotInSectorRule)

    def test_rule_generate_conference_rule(self) -> None:
        sectors = GenerationService().generate()
        rule = RuleService().generate_conference_rule(sectors, [])

        assert rule is not None
        assert rule.valid(sectors) is None
