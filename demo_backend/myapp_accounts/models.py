from django.db import models
from django.contrib.auth.models import User
from myapp_auth.models import UsersAssignedRoles
from myapp_dto.enums import AccountsTypeChoices
from myapp_mixins.models import BaseModel, RegistrationNumberModel


class Profile(BaseModel, RegistrationNumberModel):
    PREFIX = "ACC"
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="user_profiles")
    phone_number = models.CharField(max_length=15, blank=True)
    location = models.CharField(
        max_length=100, blank=True, help_text="City or location")
    phone_verified = models.BooleanField(default=False, blank=True)
    is_verified = models.BooleanField(default=False, blank=True)
    account_type = models.CharField(
        default=AccountsTypeChoices.CUSTOMER.value, choices=AccountsTypeChoices.choices(), max_length=9000, blank=True)

    class Meta:
        db_table = "myapp_profiles_tbl"
        verbose_name = "PROFILES"
        verbose_name_plural = "PROFILES"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.user.username}'s Profile"

    def get_user_role(self):
        try:
            assigned_role = UsersAssignedRoles.objects.filter(user=self.user).first()
            if getattr(assigned_role, "is_active", True):
                return assigned_role.role
            return None
        except UsersAssignedRoles.DoesNotExist:
            return None

    def get_user_permissions(self):
        role = self.get_user_role()
        return role.get_role_permissions if role is not None else []
        


class ForgotPasswordRequestUser(BaseModel):
    user = models.ForeignKey(
        Profile, related_name='request_profile', on_delete=models.CASCADE)
    token = models.CharField(max_length=300, editable=False, default=None)
    is_used = models.BooleanField(default=False)
    expiration_time = models.DateTimeField(null=True)

    class Meta:
        db_table = 'forgot_password_request'
        ordering = ['-primary_key']
        verbose_name_plural = 'FORGOT PASSWORD REQUESTS'

    def __str__(self):
        return f'{self.user} - {self.token}'


class ActivateAccountToken(BaseModel):
    user = models.ForeignKey(
        Profile, related_name='profile_activation', on_delete=models.CASCADE)
    token = models.CharField(max_length=300, editable=False, default=None)
    is_used = models.BooleanField(default=False)
    expiration_time = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = 'activate_account_token'
        ordering = ['-primary_key']
        verbose_name_plural = 'ACTIVATE ACCOUNT TOKEN'

    def __str__(self):
        return f'{self.user} - {self.token}'
