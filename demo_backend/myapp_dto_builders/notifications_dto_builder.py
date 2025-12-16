from myapp_dto.notification_dto import NotificationObject
from myapp_notifications.models import InAppNotifications
from myapp_utils.cache_utils import get_cached_model_or_db


class NotificationBuilder:

    @classmethod
    def get_notification_data(cls, id):
        query_set: InAppNotifications = get_cached_model_or_db(InAppNotifications, id)
        if not query_set:
            return None

        return NotificationObject(
            id=query_set.primary_key,
            unique_id=query_set.unique_id,
            title=query_set.message,
            message=query_set.message,
            viewed=query_set.read_on is not None,
            notification_type=query_set.notification_type,
            callback_item_id=query_set.callback_item_id,
            created_date=query_set.created_at,
        )
