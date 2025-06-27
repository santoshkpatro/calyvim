from django.db.models.signals import post_save
from django.dispatch import receiver
from calyvim.models import Organization, OrganizationMember


@receiver(post_save, sender=Organization)
def create_organization_owner(sender, instance, created, **kwargs):
    if created:
        # Automatically create the owner member for the organization
        OrganizationMember.objects.create(
            organization=instance,
            user=instance.created_by,
            role=OrganizationMember.Role.OWNER,
            confirmed_at=instance.created_at,
        )
