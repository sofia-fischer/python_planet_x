from abc import ABC, abstractmethod
from dataclasses import dataclass

from app.valueObjects.luminary import Luminary
from app.valueObjects.sectors import Sectors


@dataclass
class BaseRule(ABC):
    icon: Luminary

    @abstractmethod
    def valid(self, sectors: Sectors) -> str | None:
        pass

    @abstractmethod
    def description(self) -> str:
        pass


@dataclass
class InSectorRule(BaseRule):
    icon: Luminary
    sector: int

    def valid(self, sectors: Sectors) -> str | None:
        if self.icon in sectors[self.sector]:
            return None

        return f"In sector {self.sector + 1} is no {self.icon.to_string()}."

    def description(self) -> str:
        return f"In sector {self.sector + 1} is {self.icon.to_string()}."


@dataclass
class NotInSectorRule(BaseRule):
    icon: Luminary
    sector: int

    def valid(self, sectors: Sectors) -> str | None:
        if self.icon not in sectors[self.sector]:
            return None

        return f"In sector {self.sector + 1} is {self.icon.to_string()}."

    def description(self) -> str:
        return f"In sector {self.sector + 1} is no {self.icon.to_string()}."


@dataclass
class NextToRule(BaseRule):
    icon: Luminary
    other_icon: Luminary

    def valid(self, sectors: Sectors) -> str | None:
        for index, luminary in sectors:
            if self.icon not in luminary:
                continue

            if (self.other_icon not in sectors[(index + 1) % sectors.COUNT]
                    and self.other_icon not in sectors[(index - 1) % sectors.COUNT]):
                return f"{self.icon.to_string()} is not next to {self.other_icon.to_string()}."
        return None

    def description(self) -> str:
        return f"{self.icon.to_string()} is always next to {self.other_icon.to_string()}."


@dataclass
class NotNextToRule(BaseRule):
    icon: Luminary
    other_icon: Luminary

    def  valid(self, sectors: Sectors) -> str | None:
        for index, luminary in sectors:
            if self.icon not in luminary:
                continue

            if (self.other_icon in sectors[(index + 1) % sectors.COUNT]
                    or self.other_icon in sectors[(index - 1) % sectors.COUNT]):
                return f"{self.icon.to_string()} is next to {self.other_icon.to_string()}."
        return None

    def description(self) -> str:
        return f"{self.icon.to_string()} is never next to {self.other_icon.to_string()}."


@dataclass
class CountInSectorsRule(BaseRule):
    icon: Luminary
    start: int
    end: int
    count: int

    def valid(self, sectors: Sectors) -> str | None:
        absolut_end = self.end if self.end >= self.start else self.end + sectors.COUNT
        counter = 0
        for index in [index % sectors.COUNT for index in range(0, absolut_end - self.start + 1)]:
            if self.icon in sectors[(self.start + index) % sectors.COUNT]:
                counter += 1

        if counter == self.count:
            return None

        return (f"There are {counter} {self.icon.to_string()} within sector {self.start + 1} to {self.end + 1},"
                f" but there should be {self.count}.")

    def description(self) -> str:
        return f"There are {self.count} {self.icon.to_string()} within sector {self.start + 1} to {self.end + 1}."


@dataclass
class BandOfSectorsRule(BaseRule):
    icon: Luminary
    count: int

    def valid(self, sectors: Sectors) -> str | None:
        # the board is valid if all icons are within n consecutive sectors.
        # therefor the board is valid, if there exists a band of 12-n sectors, which do not contain the icon.
        out_of_band = sectors.COUNT - self.count

        for index, _ in sectors:
            found_icon = False
            for count in range(0, out_of_band):
                if self.icon in sectors[(index + count) % sectors.COUNT]:
                    found_icon = True
                    break
            if not found_icon:
                return None
        return f"Not all {self.icon.to_string()} are within {self.count} sectors."

    def description(self) -> str:
        return f"All {self.icon.to_string()} are within a band of {self.count} sectors."


@dataclass
class NotWithinNSectorsRule(BaseRule):
    icon: Luminary
    other_icon: Luminary
    count: int

    def valid(self, sectors: Sectors) -> str | None:
        indices_with_icon = [index for index, luminary in sectors if self.icon in luminary]

        for index in indices_with_icon:
            for count in range(0, self.count + 1):
                if self.other_icon in sectors[(index + count) % sectors.COUNT]:
                    return f"{self.icon.to_string()} is within {self.count} sectors of {self.other_icon.to_string()}."
                if self.other_icon in sectors[(index - count) % sectors.COUNT]:
                    return f"{self.icon.to_string()} is within {self.count} sectors of {self.other_icon.to_string()}."
        return None

    def description(self) -> str:
        return f"{self.icon.to_string()} is never within {self.count} sectors of {self.other_icon.to_string()}."


@dataclass
class WithinNSectorsRule(BaseRule):
    icon: Luminary
    other_icon: Luminary
    count: int

    def valid(self, sectors: Sectors) -> str | None:
        indices_with_icon = [index for index, luminary in sectors if self.icon in luminary]

        for index in indices_with_icon:
            found_other_icon = False
            for count in range(0, self.count + 1):
                if self.other_icon in sectors[(index + count) % sectors.COUNT]:
                    found_other_icon = True
                if self.other_icon in sectors[(index - count) % sectors.COUNT]:
                    found_other_icon = True
            if not found_other_icon:
                return f"{self.icon.to_string()} is not within {self.count} sectors of {self.other_icon.to_string()}."
        return None

    def description(self) -> str:
        return f"{self.icon.to_string()} is always within {self.count} sectors of {self.other_icon.to_string()}."


@dataclass
class PlanetXLocationRule(BaseRule):
    # Predecessor
    icon: Luminary
    sector: int
    # Successor
    other_icon: Luminary

    def valid(self, sectors: Sectors) -> str | None:
        error = (f"Planet X is NOT correctly located in sector {self.sector + 1} "
                 f"with {self.icon.to_string()} as predecessor and {self.other_icon.to_string()} as successor.")
        if Luminary.PLANET_X not in sectors[self.sector]:
            return error
        if self.icon not in sectors[(self.sector - 1) % sectors.COUNT]:
            return error
        if self.other_icon not in sectors[(self.sector + 1) % sectors.COUNT]:
            return error
        return None

    def description(self) -> str:
        return (f"Planet X was located in sector {self.sector + 1} "
                f"with {self.icon.to_string()} as predecessor and {self.other_icon.to_string()} as successor.")
