from django.db import models

from calyvim.models.common import BaseModel
from calyvim.models.fallbacks import get_anonymous_user


class Team(BaseModel):
    organization = models.ForeignKey(
        "Organization",
        on_delete=models.CASCADE,
        related_name="teams",
    )
    name = models.CharField(max_length=128)
    bio = models.TextField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_by = models.ForeignKey(
        "User",
        on_delete=models.SET(get_anonymous_user),
        related_name="created_teams",
    )
    issue_prefix = models.CharField(max_length=16, blank=True)

    class Meta:
        db_table = "teams"
        verbose_name = "Team"
        verbose_name_plural = "Teams"
        ordering = ["name"]
        constraints = [
            models.UniqueConstraint(
                fields=["organization", "name"],
                name="unique_team_name_per_organization",
            )
        ]

    def __str__(self):
        return f"Team ({self.id})"

    def save(self, *args, **kwargs):
        if self._state.adding:
            if not self.issue_prefix:
                # Generate a default issue prefix based on the team name
                self.issue_prefix = self.name[:3].upper()
        return super().save(*args, **kwargs)


class TeamMember(BaseModel):
    class Role(models.TextChoices):
        ADMIN = ("admin", "Admin")
        LEAD = ("lead", "Lead")
        MANAGER = ("manager", "Manager")
        CONTRIBUTOR = ("contributor", "Contributor")
        VIEWER = ("viewer", "Viewer")

    team = models.ForeignKey(
        "Team",
        on_delete=models.CASCADE,
        related_name="members",
    )
    user = models.ForeignKey(
        "User",
        on_delete=models.CASCADE,
        related_name="team_members",
    )
    role = models.CharField(
        max_length=16,
        choices=Role.choices,
        default=Role.CONTRIBUTOR,
    )
    role_description = models.CharField(
        max_length=64, blank=True, null=True, help_text="Description of the role"
    )

    class Meta:
        db_table = "team_members"
        verbose_name = "Team Member"
        verbose_name_plural = "Team Members"
        ordering = ["team", "user"]
        constraints = [
            models.UniqueConstraint(
                fields=["team", "user"],
                name="unique_team_member_per_team",
            )
        ]

    def __str__(self):
        return f"TeamMember ({self.id})"
