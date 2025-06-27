from django.db.models.signals import post_migrate
from django.dispatch import receiver
from calyvim.models import User
from django.utils import timezone


@receiver(post_migrate)
def ensure_anonymous_user(sender, **kwargs):
    """
    Ensure that the anonymous user exists after migrations.
    This is a placeholder function to ensure the anonymous user is created.
    """

    if not User.objects.filter(is_anonymous=True).exists():
        User.objects.create(
            email="anonymous@calyvim.com",
            full_name="Anonymous User",
            is_anonymous=True,
            date_joined=timezone.now(),
        )
