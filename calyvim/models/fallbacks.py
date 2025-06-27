from django.contrib.auth import get_user_model


def get_anonymous_user():
    """
    Returns a user instance representing an anonymous user.
    This is useful for cases where a user is not authenticated.
    """
    User = get_user_model()
    anonymous_user = User.objects.filter(is_anonymous=True).first()
    return anonymous_user
