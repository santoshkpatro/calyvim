from django.db import models

from calyvim.models.common import BaseModel
from calyvim.models.fallbacks import get_anonymous_user


class Issue(BaseModel):
    class IssueType(models.TextChoices):
        TASK = ("task", "Task")
        GOAL = ("goal", "Goal")
        STORY = ("story", "Story")

    organization = models.ForeignKey(
        "Organization",
        on_delete=models.CASCADE,
        related_name="issues",
    )
    team = models.ForeignKey(
        "Team",
        on_delete=models.CASCADE,
        related_name="team_issues",
    )
    parent = models.ForeignKey(
        "self",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="sub_issues",
    )
    goal = models.ForeignKey(
        "self",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="goal_issues",
    )
    issue_type = models.CharField(
        max_length=16, choices=IssueType.choices, default=IssueType.TASK
    )
    summary = models.CharField(max_length=512)
    description = models.TextField(blank=True, null=True)
    name = models.CharField(max_length=32, blank=True)
    number = models.IntegerField(blank=True)
    state = models.ForeignKey("State", on_delete=models.PROTECT, related_name="issues")
    sequence = models.FloatField(default=50000)
    created_by = models.ForeignKey(
        "User",
        on_delete=models.SET(get_anonymous_user),
        related_name="created_issues",
    )
    due_date = models.DateField(blank=True, null=True)
    completed_at = models.DateTimeField(blank=True, null=True)

    archived_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = "issues"
        verbose_name = "Issue"
        verbose_name_plural = "Issues"
        ordering = ["sequence", "number"]
        constraints = [
            models.UniqueConstraint(
                fields=["team", "number"],
                name="unique_issue_number_per_team",
            ),
            models.UniqueConstraint(
                fields=["organization", "name"],
                name="unique_issue_name_per_organization",
            ),
        ]

    def __str__(self):
        return f"Issue ({self.id}) - {self.summary}"


class IssueGoal(BaseModel):
    class Status(models.TextChoices):
        PENDING = ("pending", "Pending")
        APPROVED = ("approved", "Approved")
        REJECTED = ("rejected", "Rejected")

    goal = models.ForeignKey("Issue", on_delete=models.CASCADE, related_name="goals")
    team = models.ForeignKey(
        "Team", on_delete=models.CASCADE, related_name="team_issue_goals"
    )
    status = models.CharField(
        max_length=16, choices=Status.choices, default=Status.PENDING
    )
    reviewed_by = models.ForeignKey(
        "User",
        on_delete=models.SET(get_anonymous_user),
        related_name="reviewed_goal_issues",
    )
    reviewed_at = models.DateTimeField(blank=True, null=True)
    comment = models.TextField(blank=True, null=True)

    class Meta:
        db_table = "issue_goals"
        verbose_name = "Issue Goal"
        verbose_name_plural = "Issue Goals"
        ordering = ["goal", "team"]
        constraints = [
            models.UniqueConstraint(
                fields=["goal", "team"],
                name="unique_goal_per_team",
            )
        ]


class IssueSnapshot(BaseModel):
    issue = models.ForeignKey(
        "Issue", on_delete=models.CASCADE, related_name="snapshots"
    )
    state = models.ForeignKey(
        "State", on_delete=models.PROTECT, related_name="issue_snapshots"
    )
    date = models.DateField()

    class Meta:
        db_table = "issue_snapshots"
        verbose_name = "Issue Snapshot"
        verbose_name_plural = "Issue Snapshots"
        ordering = ["date"]
        constraints = [
            models.UniqueConstraint(
                fields=["issue", "state", "date"],
                name="unique_issue_snapshot_per_issue_state_date",
            )
        ]
