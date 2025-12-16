import graphene
from myapp_dto.enums import TimeRangeEnum

class BaseFilteringObject(graphene.InputObjectType):
    is_active = graphene.Boolean()
    unique_id = graphene.String()
    search_term = graphene.String()
    page_size = graphene.Int()
    page_number = graphene.Int(required=True)
    time_range = TimeRangeEnum() 
    time_from = graphene.DateTime()
    time_to = graphene.DateTime()
    created_by = graphene.String()


class BaseObject(graphene.ObjectType):
    id = graphene.String()
    unique_id = graphene.String()
    is_active = graphene.Boolean()
    created_at = graphene.DateTime()
    