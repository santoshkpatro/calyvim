import random, string
from django.db import models
from django.utils.text import slugify
from django.core.exceptions import ValidationError

from calyvim.models.base import BaseModel


class Organization(BaseModel):
    name = models.CharField(max_length=128)
    slug = models.SlugField(max_length=128, unique=True)
    description = models.TextField(blank=True, null=True)
    website = models.URLField(blank=True, null=True)
    owner = models.ForeignKey(
        "User", on_delete=models.RESTRICT, related_name="owned_organizations"
    )

    members = models.ManyToManyField(
        "User",
        through="OrganizationMember",
        related_name="organizations",
        through_fields=("organization", "user"),
    )

    class Meta:
        db_table = "organizations"
        ordering = ["created_at"]
        verbose_name = "Organization"
        verbose_name_plural = "Organizations"

    def __str__(self):
        return f"{self.name}"

    def get_unique_org_slug(self, org_name):
        base_slug = slugify(org_name.split()[0])  # Use only first word

        # Try base_slug directly
        if not Organization.objects.filter(slug=base_slug).exists():
            return base_slug

        # Retry with 2-digit suffix
        for _ in range(5):
            suffix = "".join(random.choices(string.digits, k=2))
            candidate = f"{base_slug}{suffix}"
            if not Organization.objects.filter(slug=candidate).exists():
                return candidate

        raise ValidationError(
            "Unable to generate unique organization slug after 5 attempts"
        )

    def save(self, *args, **kwargs):
        if self._state.adding:
            if not self.slug:
                self.slug = self.get_unique_org_slug(self.name)
        return super().save(*args, **kwargs)


class OrganizationMember(BaseModel):
    class Role(models.TextChoices):
        OWNER = ("owner", "Owner")
        ADMIN = ("admin", "Admin")
        MEMBER = ("member", "Member")

    organization = models.ForeignKey(
        "Organization", on_delete=models.CASCADE, related_name="organization_members"
    )
    user = models.ForeignKey(
        "User", on_delete=models.CASCADE, related_name="user_organization_memberships"
    )
    role = models.CharField(max_length=10, choices=Role.choices, default=Role.MEMBER)
    accepted_at = models.DateTimeField(blank=True, null=True)
    invited_by = models.ForeignKey(
        "User",
        on_delete=models.CASCADE,
        related_name="invited_organization_memberships",
        blank=True,
        null=True,
    )

    class Meta:
        db_table = "organization_members"
        unique_together = ("organization", "user")
        ordering = ["-created_at"]
        verbose_name = "Organization Member"
        verbose_name_plural = "Organization Members"

    def __str__(self):
        return f"{str(self.id)}"
