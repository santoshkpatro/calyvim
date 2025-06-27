import uuid
from django.db import models
from django.db import transaction


class BaseModel(models.Model):
    """
    An abstract base model that provides a UUID primary key.
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
        ordering = ["-created_at"]

    def apply_updates(self, **kwargs):
        """
        Apply updates to the model instance and save it within a transaction.
        """
        try:
            with transaction.atomic():
                for key, value in kwargs.items():
                    setattr(self, key, value)
                self.save(update_fields=kwargs.keys())
                return True, None
        except Exception as e:
            # Handle exceptions as needed, e.g., log the error or re-raise it
            print(f"Error applying updates: {e}")
            return False, str(e)
