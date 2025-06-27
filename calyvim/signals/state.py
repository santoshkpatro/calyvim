from django.db.models.signals import post_save
from django.dispatch import receiver
from calyvim.models import State, Team


@receiver(post_save, sender=Team)
def create_default_states(sender, instance, created, **kwargs):
    if created:
        new_states = [
            State(
                name="Backlog",
                team=instance,
                status="open",
                sequence=10000,
                color="#E8F4FD",  # Very light blue
            ),
            State(
                name="To Do",
                team=instance,
                status="open",
                sequence=20000,
                color="#F0F9FF",  # Very light sky blue
            ),
            State(
                name="In Progress",
                team=instance,
                status="active",
                sequence=30000,
                color="#FEF3C7",  # Light yellow/amber
            ),
            State(
                name="In Review",
                team=instance,
                status="active",
                sequence=40000,
                color="#FDF2F8",  # Very light pink
            ),
            State(
                name="Done",
                team=instance,
                status="closed",
                sequence=50000,
                color="#F0FDF4",  # Very light green
            ),
            State(
                name="Cancelled",
                team=instance,
                status="closed",
                sequence=60000,
                color="#F9FAFB",  # Very light gray
            ),
        ]
        State.objects.bulk_create(new_states)
