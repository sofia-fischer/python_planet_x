from random import choice, randrange, shuffle

from app.services.board_service import GenerationService
from app.valueObjects.luminary import Luminary
from app.valueObjects.rules import (
    BandOfSectorsRule,
    BaseRule,
    CountInSectorsRule,
    InSectorRule,
    NextToRule,
    NotInSectorRule,
    NotNextToRule,
    NotWithinNSectorsRule,
    WithinNSectorsRule,
)
from app.valueObjects.sectors import Sectors


class RuleService:

    @staticmethod
    def get_base_rules() -> list[BaseRule]:
        return [
            NextToRule(Luminary.ASTEROID, Luminary.ASTEROID),
            NextToRule(Luminary.NEBULA, Luminary.EMPTY_SPACE),
            NotNextToRule(Luminary.DWARF_PLANET, Luminary.PLANET_X),
        ]

    def generate_start_rule(self, sectors: Sectors, existing_rules: list[BaseRule]) -> NotInSectorRule:
        while True:
            rule = self.__generate_not_in_rule(sectors)
            if rule is None:
                continue
            if rule not in existing_rules:
                return rule

    def generate_conference_rule(self, sectors: Sectors, existing_rules: list[BaseRule]) -> BaseRule:
        rule: BaseRule | None = None
        while rule is None:
            match (randrange(0, 5)):
                case 0:
                    rule = self.__generate_next_to_rule(sectors)
                case 1:
                    rule = self.__generate_not_next_to_rule(sectors)
                case 2:
                    rule = self.__generate_in_band_rule(sectors)
                case 3:
                    rule = self.__generate_within_sectors_rule(sectors)
                case _:
                    rule = self.__generate_not_within_sectors_rule(sectors)
            if rule in existing_rules or rule in self.get_base_rules():
                rule = None
        return rule

    def __shuffeled_icons(self) -> list[Luminary]:
        icons = list(set(Luminary) - {Luminary.PLANET_X})
        shuffle(icons)
        return icons

    def __generate_not_in_rule(self, sectors: Sectors) -> NotInSectorRule | None:
        indices = list(range(0, sectors.COUNT))
        shuffle(indices)
        for index in indices:
            luminary = sectors[index]
            if Luminary.PLANET_X in luminary:
                continue
            if Luminary.MOON in luminary and index not in GenerationService.POSSIBLE_MOON_SECTORS:
                continue
            icons = list(set(Luminary) - {Luminary.PLANET_X, luminary})
            return NotInSectorRule(icon=choice(icons), sector=index)
        return None

    def __generate_next_to_rule(self, sectors: Sectors, for_x: bool = False) -> NextToRule | None:
        if for_x:
            return None
        for icon in self.__shuffeled_icons():
            for next_to in self.__shuffeled_icons():
                rule = NextToRule(icon=icon, other_icon=next_to)
                if rule.valid(sectors) is None:
                    return rule
        return None

    def __generate_not_next_to_rule(self, sectors: Sectors, for_x: bool = False) -> NotNextToRule | None:
        for icon in (self.__shuffeled_icons() if not for_x else [Luminary.PLANET_X]):
            for not_next_to in self.__shuffeled_icons():
                if for_x and not_next_to == Luminary.DWARF_PLANET:
                    continue
                rule = NotNextToRule(icon=icon, other_icon=not_next_to)
                if rule.valid(sectors) is None:
                    return rule
        return None

    def __generate_in_band_rule(self, sectors: Sectors, for_x: bool = False) -> BandOfSectorsRule | None:
        for icon in (self.__shuffeled_icons() if not for_x else [Luminary.PLANET_X]):
            bands = [5, 4, 3]
            shuffle(bands)
            for band in bands:
                rule = BandOfSectorsRule(icon=icon, count=band)
                if rule.valid(sectors) is None:
                    return rule
        return None

    def __generate_within_sectors_rule(self, sectors: Sectors, for_x: bool = False) -> WithinNSectorsRule | None:
        for icon in (self.__shuffeled_icons() if not for_x else [Luminary.PLANET_X]):
            withins = [4, 3, 2]
            shuffle(withins)
            for within in withins:
                for other_icon in self.__shuffeled_icons():
                    rule = WithinNSectorsRule(icon=icon, other_icon=other_icon, count=within)
                    if rule.valid(sectors) is None:
                        return rule
        return None

    def __generate_not_within_sectors_rule(self, sectors: Sectors, for_x: bool = False) -> NotWithinNSectorsRule | None:
        for icon in (self.__shuffeled_icons() if not for_x else [Luminary.PLANET_X]):
            withins = [5, 4, 3, 2]
            shuffle(withins)
            for within in withins:
                for other_icon in self.__shuffeled_icons():
                    rule = NotWithinNSectorsRule(icon=icon, other_icon=other_icon, count=within)
                    if rule.valid(sectors) is not None:
                        return rule
        return None

    @staticmethod
    def get_valid_in_sector_rule(sectors: Sectors, index: int) -> InSectorRule:
        if Luminary.PLANET_X in sectors[index]:
            return InSectorRule(Luminary.EMPTY_SPACE, index)
        return InSectorRule(sectors[index], index)

    @staticmethod
    def get_valid_count_in_sector_rule(sectors: Sectors, icon: Luminary, start: int, end: int) -> CountInSectorsRule:
        absolut_end = end if end >= start else end + sectors.COUNT
        steps = absolut_end - start
        counter = 0
        for count in range(0, steps):
            if icon in sectors[(start + count) % sectors.COUNT]:
                counter += 1
        return CountInSectorsRule(icon, start, end, counter)
