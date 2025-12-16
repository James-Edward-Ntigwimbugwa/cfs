import graphene

from myapp_dto.shared_dto import PageObject, ResponseObject
from myapp_mixins.base_object import BaseFilteringObject


class AuditLogObject(graphene.ObjectType):
    id = graphene.String()
    unique_id = graphene.String()
    timestamp = graphene.DateTime()
    execution_time_ms = graphene.Float()
    path = graphene.String()
    method = graphene.String()
    status_code = graphene.Int()
    message = graphene.String()
    user_id = graphene.ID()
    is_staff = graphene.Boolean()
    ip_address = graphene.String()
    user_agent = graphene.String()
    referrer = graphene.String()
    operation_name = graphene.String()
    operation_type = graphene.String()
    query = graphene.String()
    variables = graphene.JSONString()
    errors = graphene.JSONString()


class AuditLogsResponseObject(graphene.ObjectType):
    response = graphene.Field(ResponseObject)
    page = graphene.Field(PageObject)
    data = graphene.List(AuditLogObject)

class AuditLogFilterInput(BaseFilteringObject):
    user = graphene.String()
