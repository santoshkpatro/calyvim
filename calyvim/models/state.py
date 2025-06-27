from django.db import models

from calyvim.models.common import BaseModel


class State(BaseModel):
    class Status(models.TextChoices):
        OPEN = ("open", "Open")
        ACTIVE = ("active", "Active")
        CLOSED = ("closed", "Closed")

    team = models.ForeignKey("Team", on_delete=models.CASCADE, related_name="states")
    name = models.CharField(max_length=128)
    status = models.CharField(
        max_length=16, choices=Status.choices, default=Status.OPEN
    )
    sequence = models.FloatField(default=10000)
    color = models.CharField(max_length=7, default="#111111")

    class Meta:
        db_table = "states"
        verbose_name = "State"
        verbose_name_plural = "States"
        ordering = ["sequence", "name"]
        constraints = [
            models.UniqueConstraint(
                fields=["team", "name"],
                name="unique_state_name_per_team",
            )
        ]
