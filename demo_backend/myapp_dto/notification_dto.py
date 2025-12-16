import graphene

from myapp_dto.enums import InAppNotificationTypeEnum
from myapp_dto.shared_dto import PageObject, ResponseObject
from myapp_mixins.base_object import BaseFilteringObject, BaseObject




class NotificationFilteringObject(BaseFilteringObject): ...


class NotificationObject(BaseObject):
    title = graphene.String()
    message = graphene.String()
    viewed = graphene.Boolean()
    notification_type = InAppNotificationTypeEnum()
    callback_item_id = graphene.String()


class NotificationResponseObject(graphene.ObjectType):
    response = graphene.Field(ResponseObject)
    page = graphene.Field(PageObject)
    data = graphene.List(NotificationObject)


class UnreadNotificationInputObject(graphene.InputObjectType):
    unread_all = graphene.Boolean()
    unique_ids = graphene.List(graphene.String)
