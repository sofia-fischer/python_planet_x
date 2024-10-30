from unittest import TestCase

from app.services.board_service import GenerationService
from app.services.rule_service import RuleService


class TestRuleService(TestCase):
    def test_rule_service(self) -> None:
        service = RuleService()
        sectors = GenerationService().generate()
        start_rules = service.generate_start_rules(sectors, 5)
        conference_rules = service.generate_conferences(sectors, start_rules)

        assert len(start_rules) == 5, "Actual: " + str(len(start_rules))
        assert len(conference_rules.all()) == 7, "Actual: " + str(len(conference_rules.all()))
