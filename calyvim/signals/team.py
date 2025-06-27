from django.db.models.signals import post_save
from django.dispatch import receiver
from calyvim.models import Team, TeamMember


@receiver(post_save, sender=Team)
def create_team_admin(sender, instance, created, **kwargs):
    if created:
        TeamMember.objects.create(
            team=instance,
            user=instance.created_by,
            role=TeamMember.Role.ADMIN,
        )
