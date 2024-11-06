import uuid
from random import choices
from string import ascii_uppercase, digits

from django.db import models

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
    PlanetXLocationRule,
    WithinNSectorsRule,
)
from app.valueObjects.sectors import Sectors


class Game(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    identifier = models.CharField(max_length=20)
    time_count = models.PositiveSmallIntegerField(default=0)
    score = models.PositiveSmallIntegerField(default=0)
    notice1 = models.PositiveSmallIntegerField(default=Luminary.fill_with_all().value)
    notice2 = models.PositiveSmallIntegerField(default=Luminary.fill_with_all().value)
    notice3 = models.PositiveSmallIntegerField(default=Luminary.fill_with_all().value)
    notice4 = models.PositiveSmallIntegerField(default=Luminary.fill_with_all().value)
    notice5 = models.PositiveSmallIntegerField(default=Luminary.fill_with_all().value)
    notice6 = models.PositiveSmallIntegerField(default=Luminary.fill_with_all().value)
    notice7 = models.PositiveSmallIntegerField(default=Luminary.fill_with_all().value)
    notice8 = models.PositiveSmallIntegerField(default=Luminary.fill_with_all().value)
    notice9 = models.PositiveSmallIntegerField(default=Luminary.fill_with_all().value)
    notice10 = models.PositiveSmallIntegerField(default=Luminary.fill_with_all().value)
    notice11 = models.PositiveSmallIntegerField(default=Luminary.fill_with_all().value)
    notice12 = models.PositiveSmallIntegerField(default=Luminary.fill_with_all().value)

    def add_time(self, time: int) -> int:
        self.time_count += time
        self.save()
        return self.time_count

    def set_notes(self, sectors: Sectors) -> None:
        self.notice1 = sectors[0].value
        self.notice2 = sectors[1].value
        self.notice3 = sectors[2].value
        self.notice4 = sectors[3].value
        self.notice5 = sectors[4].value
        self.notice6 = sectors[5].value
        self.notice7 = sectors[6].value
        self.notice8 = sectors[7].value
        self.notice9 = sectors[8].value
        self.notice10 = sectors[9].value
        self.notice11 = sectors[10].value
        self.notice12 = sectors[11].value
        self.save()

    def get_notes(self) -> Sectors:
        return Sectors().fill({
            0: Luminary(self.notice1),
            1: Luminary(self.notice2),
            2: Luminary(self.notice3),
            3: Luminary(self.notice4),
            4: Luminary(self.notice5),
            5: Luminary(self.notice6),
            6: Luminary(self.notice7),
            7: Luminary(self.notice8),
            8: Luminary(self.notice9),
            9: Luminary(self.notice10),
            10: Luminary(self.notice11),
            11: Luminary(self.notice12),
        })

    def get_sectors(self) -> Sectors:
        board = Board.objects.get(game=self)
        return Sectors().fill({
            0: Luminary(board.sector1),
            1: Luminary(board.sector2),
            2: Luminary(board.sector3),
            3: Luminary(board.sector4),
            4: Luminary(board.sector5),
            5: Luminary(board.sector6),
            6: Luminary(board.sector7),
            7: Luminary(board.sector8),
            8: Luminary(board.sector9),
            9: Luminary(board.sector10),
            10: Luminary(board.sector11),
            11: Luminary(board.sector12),
        })

    def get_rules(self) -> list['Rule']:
        return Rule.objects.filter(game=self)

    def get_theories(self) -> list['Theory']:
        return Theory.objects.filter(game=self)

    @staticmethod
    def where_identifier(identifier: str) -> 'Game':
        return Game.objects.get(identifier=identifier)

    @staticmethod
    def create_game() -> 'Game':
        identifier = ''.join(choices(ascii_uppercase + digits, k=6))
        game = Game.objects.create(identifier=identifier)
        game.save()
        return game

class Board(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    sector1 = models.PositiveSmallIntegerField(choices=Luminary.options())
    sector2 = models.PositiveSmallIntegerField(choices=Luminary.options())
    sector3 = models.PositiveSmallIntegerField(choices=Luminary.options())
    sector4 = models.PositiveSmallIntegerField(choices=Luminary.options())
    sector5 = models.PositiveSmallIntegerField(choices=Luminary.options())
    sector6 = models.PositiveSmallIntegerField(choices=Luminary.options())
    sector7 = models.PositiveSmallIntegerField(choices=Luminary.options())
    sector8 = models.PositiveSmallIntegerField(choices=Luminary.options())
    sector9 = models.PositiveSmallIntegerField(choices=Luminary.options())
    sector10 = models.PositiveSmallIntegerField(choices=Luminary.options())
    sector11 = models.PositiveSmallIntegerField(choices=Luminary.options())
    sector12 = models.PositiveSmallIntegerField(choices=Luminary.options())

    @staticmethod
    def create_board(game: Game, sectors: Sectors) -> 'Board':
        board = Board.objects.create(
            game=game,
            sector1=sectors[0].value,
            sector2=sectors[1].value,
            sector3=sectors[2].value,
            sector4=sectors[3].value,
            sector5=sectors[4].value,
            sector6=sectors[5].value,
            sector7=sectors[6].value,
            sector8=sectors[7].value,
            sector9=sectors[8].value,
            sector10=sectors[9].value,
            sector11=sectors[10].value,
            sector12=sectors[11].value
        )
        board.save()
        return board


class Rule(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    type = models.CharField(max_length=50)
    origin = models.CharField(max_length=50)
    icon = models.PositiveSmallIntegerField(choices=Luminary.options())
    other_icon = models.PositiveSmallIntegerField(choices=Luminary.options(), null=True)
    sector = models.PositiveSmallIntegerField(null=True)
    start = models.PositiveSmallIntegerField(null=True)
    end = models.PositiveSmallIntegerField(null=True)
    count = models.PositiveSmallIntegerField(null=True)

    @staticmethod
    def create(game: Game, origin: str, rule: BaseRule) -> 'Rule':
        return Rule.objects.create(
            game=game,
            type=rule.__class__.__name__,
            origin=origin,
            icon=rule.icon.value,
            other_icon= rule.other_icon.value if hasattr(rule, 'other_icon') else None,
            sector=rule.sector if hasattr(rule, 'sector') else None,
            start=rule.start if hasattr(rule, 'start') else None,
            end=rule.end if hasattr(rule, 'end') else None,
            count=rule.count if hasattr(rule, 'count') else None
        )

    def get_rule(self) -> BaseRule:
        if self.type == 'InSectorRule':
            return InSectorRule(Luminary(self.icon), self.sector)
        if self.type == 'NotInSectorRule':
            return NotInSectorRule(Luminary(self.icon), self.sector)
        if self.type == 'NextToRule':
            return NextToRule(Luminary(self.icon), Luminary(self.other_icon))
        if self.type == 'NotNextToRule':
            return NotNextToRule(Luminary(self.icon), Luminary(self.other_icon))
        if self.type == 'CountInSectorsRule':
            return CountInSectorsRule(Luminary(self.icon), self.start, self.end, self.count)
        if self.type == 'BandOfSectorsRule':
            return BandOfSectorsRule(Luminary(self.icon), self.count)
        if self.type == 'WithinNSectorsRule':
            return WithinNSectorsRule(Luminary(self.icon), Luminary(self.other_icon), self.count)
        if self.type == 'NotWithinNSectorsRule':
            return NotWithinNSectorsRule(Luminary(self.icon), Luminary(self.other_icon), self.count)
        if self.type == 'PlanetXLocationRule':
            return PlanetXLocationRule(Luminary(self.icon), self.sector, Luminary(self.other_icon))
        raise ValueError(f"Unknown rule type: {self.type}")

class Theory(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    time_count_created = models.PositiveSmallIntegerField()
    luminary = models.PositiveSmallIntegerField(choices=Luminary.options())
    sector = models.PositiveSmallIntegerField()
    time_count_reviewed = models.PositiveSmallIntegerField()
    score = models.PositiveSmallIntegerField(null=True)

    def get_luminary(self) -> Luminary:
        return Luminary(self.luminary)

    @staticmethod
    def create_from(game: Game, icon: Luminary, sector: int) -> 'Theory':
        actual_icon = game.get_sectors()[sector]
        return Theory.objects.create(
            game=game,
            time_count_created=game.time_count,
            luminary=icon.value,
            sector=sector,
            time_count_reviewed=game.time_count + 6,
            score=icon.score() if icon in actual_icon else 0
        )

# class Move(models.Model):
#     id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
#     created_at = models.DateTimeField(auto_now_add=True)
#     game = models.ForeignKey(Game, on_delete=models.CASCADE)
#     timeCount = models.PositiveSmallIntegerField()
#     type = models.CharField(max_length=50)
#     data = models.JSONField()
