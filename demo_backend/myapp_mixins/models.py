import random
from django.db import models
from django.contrib.auth.models import User
from myapp_utils.generators import Generator


class BaseModel(models.Model):
    primary_key = models.AutoField(primary_key=True)
    unique_id = models.BigIntegerField(editable=False, default=Generator.generate_64bit_int_uuid, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    updated_date = models.DateTimeField(auto_now=True, null=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name="created_%(class)s_set")

    class Meta:
        abstract = True


class RegistrationNumberModel(models.Model):
    PREFIX = None
    registration_number = models.CharField(
        max_length=12, unique=True, blank=True)

    class Meta:
        abstract = True

    def generate_unique_registration_number(self):
        from myapp_utils.utils import Utils

        while True:
            reg = Utils.generate_prefixed_code(prefix= self.PREFIX)
            if not self.__class__.objects.filter(registration_number=reg).exists():
                return reg

    def save(self, *args, **kwargs):
        if not self.registration_number:
            if not self.PREFIX:
                raise ValueError("PREFIX must be defined in the model")
            self.registration_number = self.generate_unique_registration_number()

        super().save(*args, **kwargs)
