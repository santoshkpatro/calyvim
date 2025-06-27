import secrets
from django.db import models
from django.utils import timezone
from calyvim.models.common import BaseModel
from calyvim.models.fallbacks import get_anonymous_user


class Organization(BaseModel):
    name = models.CharField(max_length=128)
    description = models.TextField(blank=True, null=True)

    is_active = models.BooleanField(default=True)
    created_by = models.ForeignKey(
        "User",
        on_delete=models.SET(get_anonymous_user),
        related_name="created_organizations",
    )

    users = models.ManyToManyField(
        "User",
        through="OrganizationMember",
        related_name="organizations",
        through_fields=("organization", "user"),
    )

    class Meta:
        db_table = "organizations"
        verbose_name = "Organization"
        verbose_name_plural = "Organizations"
        ordering = ["name"]
        constraints = []

    def __str__(self):
        return f"Organization ({self.id})"


class OrganizationMember(BaseModel):
    class Role(models.TextChoices):
        OWNER = ("owner", "Owner")
        ADMIN = ("admin", "Admin")
        MEMBER = ("member", "Member")

    organization = models.ForeignKey(
        "Organization", on_delete=models.CASCADE, related_name="members"
    )
    user = models.ForeignKey(
        "User", on_delete=models.CASCADE, related_name="organization_members"
    )
    role = models.CharField(max_length=32, choices=Role.choices, default=Role.MEMBER)
    confirmed_at = models.DateTimeField(null=True, blank=True)
    invited_by = models.ForeignKey(
        "User",
        on_delete=models.SET(get_anonymous_user),
        related_name="invited_members",
        blank=True,
        null=True,
    )

    class Meta:
        db_table = "organization_members"
        verbose_name = "Organization Member"
        verbose_name_plural = "Organization Members"
        ordering = ["-created_at"]
        constraints = [
            models.UniqueConstraint(
                fields=["organization", "user"], name="unique_organization_member"
            )
        ]

    def __str__(self):
        return f"OrganizationMember ({self.id})"


class OrganizationInvite(BaseModel):
    organization = models.ForeignKey(
        "Organization", on_delete=models.CASCADE, related_name="invites"
    )
    email = models.EmailField()
    role = models.CharField(max_length=32, choices=OrganizationMember.Role.choices)
    invited_by = models.ForeignKey(
        "User",
        on_delete=models.SET(get_anonymous_user),
        related_name="organization_invites",
    )
    token = models.CharField(max_length=64, unique=True)
    accepted_at = models.DateTimeField(null=True, blank=True)
    rejected_at = models.DateTimeField(null=True, blank=True)
    expires_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = "organization_invites"
        verbose_name = "Organization Invite"
        verbose_name_plural = "Organization Invites"
        ordering = ["-created_at"]
        constraints = [
            # Prevents multiple *active* invites (not yet accepted or rejected and not expired)
            models.UniqueConstraint(
                fields=["organization", "email"],
                condition=models.Q(
                    accepted_at__isnull=True,
                    rejected_at__isnull=True,
                    expires_at__gt=models.functions.Now(),
                ),
                name="unique_active_organization_invite",
            )
        ]

    def __str__(self):
        return f"OrganizationInvite ({self.id})"

    def save(self, *args, **kwargs):
        if self._state.adding:
            if not self.token:
                # Generate a unique token for the invite
                self.token = secrets.token_urlsafe(32)

            if not self.expires_at:
                # Set a default expiration time (e.g., 3 days from now)
                self.expires_at = timezone.now() + timezone.timedelta(days=3)

        super().save(*args, **kwargs)

    def confirm(self):
        """Mark the invite as accepted."""
        if self.accepted_at or self.rejected_at:
            raise ValueError("Invite has already been accepted or rejected.")

        if self.expires_at < timezone.now():
            raise ValueError("Invite has expired and cannot be accepted.")

        self.accepted_at = timezone.now()
        self.save(update_fields=["accepted_at"])
