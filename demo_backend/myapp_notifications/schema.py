import logging

from django.db.models import Q
import graphene
from myapp_dto.notification_dto import NotificationFilteringObject, NotificationResponseObject
from myapp_dto_builders.notifications_dto_builder import NotificationBuilder
from myapp_dto_builders.response_builder import build_response
from myapp_notifications.models import *
from myapp_utils.decorators.permission import login_required
from myapp_utils.user_utils import UserUtils

logger = logging.getLogger(__name__)


class Query(graphene.ObjectType):
    get_all_in_app_notifications = graphene.Field(NotificationResponseObject, filtering=NotificationFilteringObject(), description='PERMISSIONS=[]')

    @login_required()
    def resolve_get_all_in_app_notifications(self, info, filtering=None, **kwargs):
        profile_unique_id = UserUtils.__profile__(info.context)
        filters = Q(is_active=True, related_in_app_notification__receiver__unique_id=profile_unique_id)
        return build_response(InAppNotifications, filters, NotificationBuilder.get_notification_data, info)
