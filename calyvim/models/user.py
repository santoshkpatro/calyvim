from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.utils import timezone

from calyvim.models.common import BaseModel


class UserManager(models.Manager):
    def create_superuser(self, email, full_name, password=None):
        today = timezone.now()
        user = self.model(
            email=email,
            full_name=full_name,
            is_admin=True,
            verified_at=today,
            date_joined=today,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user


class ActiveUserManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(date_joined__isnull=False)


class User(AbstractBaseUser, BaseModel):
    username = models.CharField(max_length=150, blank=True, unique=True)
    email = models.EmailField(unique=True)
    full_name = models.CharField(max_length=255, blank=True)
    display_name = models.CharField(max_length=255, blank=True)
    is_2f_enabled = models.BooleanField(default=False)

    verified_at = models.DateTimeField(null=True, blank=True)
    password_expired = models.BooleanField(default=False)

    last_login_at = models.DateTimeField(null=True, blank=True)
    last_login_ip = models.GenericIPAddressField(null=True, blank=True)

    is_admin = models.BooleanField(default=False)
    date_joined = models.DateTimeField(blank=True, null=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username", "full_name"]

    objects = UserManager()
    active_objects = ActiveUserManager()

    class Meta:
        db_table = "users"
        verbose_name = "User"
        verbose_name_plural = "Users"
        ordering = ["-created_at"]
        constraints = []

    def __str__(self):
        return f"User ({self.email})"

    def save(self, *args, **kwargs):
        if self._state.adding:
            if not self.username:
                self.username = self.generate_username()
            if not self.display_name:
                self.display_name = self.full_name or self.username
        return super().save(*args, **kwargs)

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin
