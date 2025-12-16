import logging

from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.utils import timezone
from dotenv import dotenv_values
from myapp_accounts.models import ActivateAccountToken, ForgotPasswordRequestUser, Profile
from myapp_dto.enums import InAppNotificationTypeChoices
from .views import NotificationService

logger = logging.getLogger(__name__)

config = dotenv_values('.env')
FRONTEND_URL = config['FRONTEND_URL']


class ReceiverUtils:
    @staticmethod
    def get_receivers_by_profile_type(profile_type):
        """Return all users with a given profile type."""
        return Profile.objects.filter(account_type=profile_type, is_active=True)


@receiver(post_save, sender=ActivateAccountToken)
def handle_account_created(sender, instance: ActivateAccountToken, created, **kwargs):
    """
    Signal triggered whenever a new account is created. Sends a notification to the user to activate their account.
    """
    if instance.is_used:
        return

    try:
        token_url = f"{FRONTEND_URL}/activate-account/{instance.token}"

        NotificationService.send_notification_via_code(
            receivers=[instance.user.user.email],
            code='ACCOUNT_ACTIVATION',
            context={
                'DateTime': timezone.now().strftime('%d %b, %Y %I:%M %p'),
                'front_end_url': f'{token_url}',
                'cc_list': [],
            },
            item_type=InAppNotificationTypeChoices.ACCOUNTS.value,
            callback_item=instance.user.unique_id,
            html_template='accounts/account_activation.html'
        )
    except Exception as e:
        logger.error(f'Error sending account confirmation notification: {e}')


@receiver(post_save, sender=ForgotPasswordRequestUser)
def handle_forgot_password_request(sender, instance: ForgotPasswordRequestUser, created, **kwargs):
    """
    Signal triggered whenever a new password reset request is created. Sends a notification to the user to reset their password.
    """
    try:
        token_url = f"{FRONTEND_URL}/password-reset/{instance.token}"

        time_diff = instance.expiration_time - timezone.now()
        minutes_remaining = int(time_diff.total_seconds() / 60)

        NotificationService.send_notification_via_code(
            receivers=[instance.user.user.email],
            code='USER_PASSWORD_RESET_REQUEST',
            context={
                'ExpireTimeInMinutes': minutes_remaining,
                'front_end_url': f'{token_url}',
                'cc_list': [],
            },
            item_type=InAppNotificationTypeChoices.ACCOUNTS.value,
            callback_item=instance.user.unique_id,
            html_template='accounts/password_reset.html'
        )
    except Exception as e:
        logger.error(f'Error sending account confirmation notification: {e}')
