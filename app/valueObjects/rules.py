from abc import abstractmethod
from dataclasses import dataclass
from app.valueObjects.luminary import Luminary
from app.valueObjects.sectors import Sectors


@dataclass
class BaseRule:
    @abstractmethod
    def valid(self, sectors: Sectors) -> str | None:
        pass


@dataclass
class InSectorRule(BaseRule):
    icon: Luminary
    sector: int

    def valid(self, sectors: Sectors) -> str | None:
        if self.icon in sectors[self.sector]:
            return None

        return f"{self.icon.name} is not in sector {self.sector + 1}."


@dataclass
class NotInSectorRule(BaseRule):
    icon: Luminary
    sector: int

    def valid(self, sectors: Sectors) -> str | None:
        if self.icon not in sectors[self.sector]:
            return None

        return f"{self.icon.name} is in sector {self.sector + 1}."


@dataclass
class NextToRule(BaseRule):
    icon: Luminary
    next_to: Luminary

    def valid(self, sectors: Sectors) -> str | None:
        for index, luminary in sectors:
            if self.icon not in luminary:
                continue

            if self.next_to not in sectors[(index + 1) % 12] and self.next_to not in sectors[(index - 1) % 12]:
                return f"{self.icon.name} is not next to {self.next_to.name}."
        return None


@dataclass
class NotNextToRule(BaseRule):
    icon: Luminary
    not_next_to: Luminary

    def valid(self, sectors: Sectors) -> str | None:
        for index, luminary in sectors:
            if self.icon not in luminary:
                continue

            if self.not_next_to in sectors[(index + 1) % 12] or self.not_next_to in sectors[(index - 1) % 12]:
                return f"{self.icon.name} is next to {self.not_next_to.name}."
        return None


@dataclass
class CountInSectorsRule(BaseRule):
    icon: Luminary
    start: int
    end: int
    count: int

    def valid(self, sectors: Sectors) -> str | None:
        absolut_end = self.end if self.end >= self.start else self.end + 12

        counter = 0
        for index in [index % 12 for index in range(self.start, absolut_end)]:
            if self.icon in sectors[index]:
                counter += 1

        if counter == self.count:
            return None

        return f"Between sectors {self.start + 1} and {self.end + 1}, there are not {self.count} {self.icon.name}."


@dataclass
class BandOfSectorsRule(BaseRule):
    icon: Luminary
    band: int

    def valid(self, sectors: Sectors) -> str | None:
        # the board is valid if all icons are within n consecutive sectors.
        # therefor the board is valid, if there exists a band of 12-n sectors, which do not contain the icon.
        out_of_band = 12 - self.band

        for index, luminary in sectors:
            found_icon = False
            for count in range(0, out_of_band):
                if self.icon in sectors[(index + count) % 12]:
                    found_icon = True
                    break
            if not found_icon:
                return None
        return f"Not all {self.icon.name} are within {self.band} sectors."


@dataclass
class NotWithinNSectorsRule(BaseRule):
    icon: Luminary
    other_icon: Luminary
    within: int

    def valid(self, sectors: Sectors) -> str | None:
        for index, luminary in sectors:
            if self.icon not in luminary:
                continue

            for count in range(1, self.within):
                if self.other_icon in sectors[(index + count) % 12]:
                    return f"{self.icon.name} is within {self.within} sectors of {self.other_icon.name}."
        return None


@dataclass
class WithinNSectorsRule(BaseRule):
    icon: Luminary
    other_icon: Luminary
    within: int

    def valid(self, sectors: Sectors) -> str | None:
        indices_with_icon = [index for index, luminary in sectors if self.icon in luminary]

        for index in indices_with_icon:
            found_other_icon = False
            for count in [count % 12 for count in range(index, index + self.within)]:
                if self.other_icon in sectors[(index + count) % 12]:
                    found_other_icon = True
            if not found_other_icon:
                return f"{self.icon.name} is not within {self.within} sectors of {self.other_icon.name}."
        return None
