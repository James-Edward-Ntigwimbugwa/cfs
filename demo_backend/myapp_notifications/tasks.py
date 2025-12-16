from datetime import timedelta
from django.utils import timezone

from myapp_accounts.models import Profile
from .models import InAppNotifications
from celery import shared_task
from dotenv import dotenv_values
config = dotenv_values('.env')
FRONTEND_URL = config['FRONTEND_URL']
import logging
logger = logging.getLogger(__name__)

def handle_new_notification(message_data):
    """Celery task to handle new notifications"""
    receiver = message_data.get("receiver")
    sender = message_data.get("sender")
    
    if not isinstance(receiver, Profile):
        if isinstance(receiver, str):
            lookup = Profile.objects.filter(user__email=receiver).first()
            if lookup:
                receiver = lookup
            else:
                print(f"No matching profile for receiver email {receiver}, skipping in-app creation.")
                return None
        
    notification = InAppNotifications.objects.create(
        message=message_data['message'],
        sender=sender,
        receiver=receiver,
        callback_item_id=message_data.get('callback_item', None),
        notification_type=message_data.get('item_type', None),
        received_at=timezone.now(),
    )
    return f'Created notification {notification.unique_id}'


def handle_read_notification(notification_data):
    """Celery task to handle read notifications"""
    unique_id = notification_data.get('notification_id', None)
    if not unique_id:
        return 'No notification_id provided'

    notification = InAppNotifications.objects.filter(unique_id=unique_id).first()
    if notification is None:
        return f'Notification {unique_id} not found'

    if notification.read_on:
        return f'Notification {unique_id} already read'

    notification.read_on = timezone.now()
    notification.save()
    return f'Marked notification {unique_id} as read'



