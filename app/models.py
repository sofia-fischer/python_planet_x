import uuid

from django.db import models

from app.valueObjects.luminary import Luminary


class Game(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    identifier = models.CharField(max_length=20)
    timeCount = models.PositiveSmallIntegerField(default=0)
    score = models.PositiveSmallIntegerField(default=0)
    notice1 = models.PositiveSmallIntegerField(default=Luminary.fill_with_all())
    notice2 = models.PositiveSmallIntegerField(default=Luminary.fill_with_all())
    notice3 = models.PositiveSmallIntegerField(default=Luminary.fill_with_all())
    notice4 = models.PositiveSmallIntegerField(default=Luminary.fill_with_all())
    notice5 = models.PositiveSmallIntegerField(default=Luminary.fill_with_all())
    notice6 = models.PositiveSmallIntegerField(default=Luminary.fill_with_all())
    notice7 = models.PositiveSmallIntegerField(default=Luminary.fill_with_all())
    notice8 = models.PositiveSmallIntegerField(default=Luminary.fill_with_all())
    notice9 = models.PositiveSmallIntegerField(default=Luminary.fill_with_all())
    notice10 = models.PositiveSmallIntegerField(default=Luminary.fill_with_all())
    notice11 = models.PositiveSmallIntegerField(default=Luminary.fill_with_all())
    notice12 = models.PositiveSmallIntegerField(default=Luminary.fill_with_all())

    def visible_sectors(self) -> list[int]:
        return [(sector + self.timeCount) % 12 for sector in range(0, 6)]

class Board(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    sector1 = models.PositiveSmallIntegerField(choices=[(option.value, option.name) for option in list(Luminary)])
    sector2 = models.PositiveSmallIntegerField(choices=[(option.value, option.name) for option in list(Luminary)])
    sector3 = models.PositiveSmallIntegerField(choices=[(option.value, option.name) for option in list(Luminary)])
    sector4 = models.PositiveSmallIntegerField(choices=[(option.value, option.name) for option in list(Luminary)])
    sector5 = models.PositiveSmallIntegerField(choices=[(option.value, option.name) for option in list(Luminary)])
    sector6 = models.PositiveSmallIntegerField(choices=[(option.value, option.name) for option in list(Luminary)])
    sector7 = models.PositiveSmallIntegerField(choices=[(option.value, option.name) for option in list(Luminary)])
    sector8 = models.PositiveSmallIntegerField(choices=[(option.value, option.name) for option in list(Luminary)])
    sector9 = models.PositiveSmallIntegerField(choices=[(option.value, option.name) for option in list(Luminary)])
    sector10 = models.PositiveSmallIntegerField(choices=[(option.value, option.name) for option in list(Luminary)])
    sector11 = models.PositiveSmallIntegerField(choices=[(option.value, option.name) for option in list(Luminary)])
    sector12 = models.PositiveSmallIntegerField(choices=[(option.value, option.name) for option in list(Luminary)])
    conferenceAlpha = models.JSONField()
    conferenceBeta = models.JSONField()
    conferenceGamma = models.JSONField()
    conferenceDelta = models.JSONField()
    conferenceEpsilon = models.JSONField()
    conferenceRoh = models.JSONField()
    conferenceXi = models.JSONField()

class Theory(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    timeCount = models.PositiveSmallIntegerField()
    luminary = models.PositiveSmallIntegerField(choices=[(option.value, option.name) for option in list(Luminary)])
    sector = models.PositiveSmallIntegerField()
    reviewed_at = models.DateTimeField(null=True)
    score = models.PositiveSmallIntegerField(null=True)

class Move(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    timeCount = models.PositiveSmallIntegerField()
    type = models.CharField(max_length=50)
    data = models.JSONField()
