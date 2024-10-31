from random import shuffle, randrange, choice

from app.valueObjects.luminary import Luminary
from app.valueObjects.rules import BaseRule, NextToRule, NotNextToRule, BandOfSectorsRule, WithinNSectorsRule, \
    NotInSectorRule, Conferences
from app.valueObjects.sectors import Sectors


class RuleService:

    @staticmethod
    def get_base_rules() -> [BaseRule]:
        return [
            NextToRule(Luminary.ASTEROID, Luminary.ASTEROID),
            NextToRule(Luminary.NEBULA, Luminary.EMPTY_SPACE),
            NotNextToRule(Luminary.DWARF_PLANET, Luminary.PLANET_X),
        ]

    def generate_start_rules(self, sectors: Sectors, count: int = 6) -> [BaseRule]:
        rules = []
        while len(rules) < count:
            rule = self.__generate_not_in_rule(sectors)
            if rule in rules:
                continue
            rules.append(rule)
        return rules

    def generate_conferences(self, sectors: Sectors, start_rules: [BaseRule]) -> Conferences:
        rules = []

        while len(rules) <= 5:
            rule = self.__random_rule(sectors)
            if rule in rules or rule in start_rules:
                continue

            rules.append(rule)
        x_rule = self.__random_rule(sectors, True)

        shuffle(rules)
        return Conferences(
            alpha=rules[0],
            beta=rules[1],
            gamma=rules[2],
            delta=rules[3],
            epsilon=rules[4],
            roh=rules[5],
            xi=x_rule,
        )

    def __random_rule(self, sectors: Sectors, for_x: bool = False):
        rule = None
        while rule is None:
            match (randrange(0, 5)):
                case 0:
                    rule = self.__generate_next_to_rule(sectors, for_x)
                case 1:
                    rule = self.__generate_not_next_to_rule(sectors, for_x)
                case 2:
                    rule = self.__generate_in_band_rule(sectors, for_x)
                case 3:
                    rule = self.__generate_within_sectors_rule(sectors, for_x)
                case _:
                    rule = self.__generate_not_within_sectors_rule(sectors, for_x)
        return rule

    def __shuffeled_icons(self):
        icons = list(set(Luminary) - {Luminary.PLANET_X})
        shuffle(icons)
        return icons

    def __generate_not_in_rule(self, sectors: Sectors) -> BaseRule | None:
        indices = list(range(0, 12))
        shuffle(indices)
        for index in indices:
            luminary = sectors[index]
            if Luminary.PLANET_X in luminary:
                continue
            icons = list(set(Luminary) - {Luminary.PLANET_X, luminary})
            return NotInSectorRule(icon=choice(icons), sector=index)

    def __generate_next_to_rule(self, sectors: Sectors, for_x: bool = False) -> BaseRule | None:
        if for_x:
            return None
        for icon in self.__shuffeled_icons():
            for next_to in self.__shuffeled_icons():
                rule = NextToRule(icon=icon, other_icon=next_to)
                if rule.valid(sectors) is None:
                    return rule

    def __generate_not_next_to_rule(self, sectors: Sectors, for_x: bool = False) -> BaseRule | None:
        for icon in (self.__shuffeled_icons() if not for_x else [Luminary.PLANET_X]):
            for not_next_to in self.__shuffeled_icons():
                if for_x and not_next_to == Luminary.DWARF_PLANET:
                    continue
                rule = NotNextToRule(icon=icon, other_icon=not_next_to)
                if rule.valid(sectors) is None:
                    return rule

    def __generate_in_band_rule(self, sectors: Sectors, for_x: bool = False) -> BaseRule | None:
        for icon in (self.__shuffeled_icons() if not for_x else [Luminary.PLANET_X]):
            bands = [5, 4, 3]
            shuffle(bands)
            for band in bands:
                rule = BandOfSectorsRule(icon=icon, count=band)
                if rule.valid(sectors) is None:
                    return rule

    def __generate_within_sectors_rule(self, sectors: Sectors, for_x: bool = False) -> BaseRule | None:
        for icon in (self.__shuffeled_icons() if not for_x else [Luminary.PLANET_X]):
            withins = [6, 5, 4, 3]
            shuffle(withins)
            for within in withins:
                for other_icon in self.__shuffeled_icons():
                    rule = WithinNSectorsRule(icon=icon, other_icon=other_icon, count=within)
                    if rule.valid(sectors) is None:
                        return rule

    def __generate_not_within_sectors_rule(self, sectors: Sectors, for_x: bool = False) -> BaseRule | None:
        for icon in (self.__shuffeled_icons() if not for_x else [Luminary.PLANET_X]):
            withins = [6, 5, 4, 3]
            shuffle(withins)
            for within in withins:
                for other_icon in self.__shuffeled_icons():
                    rule = WithinNSectorsRule(icon=icon, other_icon=other_icon, count=within)
                    if rule.valid(sectors) is not None:
                        return rule
