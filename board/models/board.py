import uuid

from django.db import models

from board.valueObjects.luminary import Luminary


class Board(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    identifier = models.CharField(max_length=20)
    timeCount = models.PositiveSmallIntegerField(default=0)
    score = models.PositiveSmallIntegerField(default=0)
    sector1 = models.PositiveSmallIntegerField(choices=[option for option in Luminary])
    sector2 = models.PositiveSmallIntegerField(choices=[option for option in Luminary])
    sector3 = models.PositiveSmallIntegerField(choices=[option for option in Luminary])
    sector4 = models.PositiveSmallIntegerField(choices=[option for option in Luminary])
    sector5 = models.PositiveSmallIntegerField(choices=[option for option in Luminary])
    sector6 = models.PositiveSmallIntegerField(choices=[option for option in Luminary])
    sector7 = models.PositiveSmallIntegerField(choices=[option for option in Luminary])
    sector8 = models.PositiveSmallIntegerField(choices=[option for option in Luminary])
    sector9 = models.PositiveSmallIntegerField(choices=[option for option in Luminary])
    sector10 = models.PositiveSmallIntegerField(choices=[option for option in Luminary])
    sector11 = models.PositiveSmallIntegerField(choices=[option for option in Luminary])
    sector12 = models.PositiveSmallIntegerField(choices=[option for option in Luminary])
    notice1 = models.PositiveSmallIntegerField(default=Luminary.all())
    notice2 = models.PositiveSmallIntegerField(default=Luminary.all())
    notice3 = models.PositiveSmallIntegerField(default=Luminary.all())
    notice4 = models.PositiveSmallIntegerField(default=Luminary.all())
    notice5 = models.PositiveSmallIntegerField(default=Luminary.all())
    notice6 = models.PositiveSmallIntegerField(default=Luminary.all())
    notice7 = models.PositiveSmallIntegerField(default=Luminary.all())
    notice8 = models.PositiveSmallIntegerField(default=Luminary.all())
    notice9 = models.PositiveSmallIntegerField(default=Luminary.all())
    notice10 = models.PositiveSmallIntegerField(default=Luminary.all())
    notice11 = models.PositiveSmallIntegerField(default=Luminary.all())
    notice12 = models.PositiveSmallIntegerField(default=Luminary.all())
    theory3 = models.PositiveSmallIntegerField(choices=[option for option in Luminary], null=True)
    theory6 = models.PositiveSmallIntegerField(choices=[option for option in Luminary], null=True)
    theory9 = models.PositiveSmallIntegerField(choices=[option for option in Luminary], null=True)
    theory12 = models.PositiveSmallIntegerField(choices=[option for option in Luminary], null=True)
    conferenceAlpha = models.JSONField()
    conferenceBeta = models.JSONField()
    conferenceGamma = models.JSONField()
    conferenceDelta = models.JSONField()
    conferenceEpsilon = models.JSONField()
    conferenceRoh = models.JSONField()
    conferenceXi = models.JSONField()

    def visible_sectors(self) -> list[int]:
        return [(sector + self.timeCount) % 12 + 1 for sector in range(0, 6)]
