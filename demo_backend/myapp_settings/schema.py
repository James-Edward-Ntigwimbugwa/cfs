import logging
from django.db.models import Q
import graphene

from myapp_dto.settings_dto import FullLocationObject, FullLocationResponseObject, LocationResponseObject
from myapp_dto.shared_dto import ResponseObject
from myapp_dto_builders.settings_dto_builder import SettingsBuilder
from myapp_settings.models import Districts, Regions, Streets, Wards
from myapp_utils.decorators.permission import login_required


logger = logging.getLogger(__name__)


class Query(graphene.ObjectType):
    get_all_regions = graphene.Field(LocationResponseObject)
    get_all_district = graphene.Field(LocationResponseObject, region_unique_id=graphene.String())
    get_all_wards = graphene.Field(LocationResponseObject, district_unique_id=graphene.String())
    get_full_location = graphene.Field(FullLocationResponseObject, street_unique_id=graphene.String())

    @staticmethod
    def resolve_get_all_regions(self, info, **kwargs):
        filters = Q(is_active=True)

        query_set = Regions.objects.filter(filters).only('unique_id')
        resp_data = [SettingsBuilder.get_region_data(id=query.unique_id) for query in query_set]


        return info.return_type.graphene_type(response=ResponseObject.get_response(id=1), data=resp_data)

    @staticmethod
    def resolve_get_all_district(self, info, region_unique_id, **kwargs):
        filters = Q(is_active=True,
                    district_region__unique_id=region_unique_id)

        query_set = Districts.objects.filter(filters).only('unique_id')

        resp_data = [SettingsBuilder.get_district_data(id=query.unique_id) for query in query_set]

        return info.return_type.graphene_type(response=ResponseObject.get_response(id=1), data=resp_data)

    @staticmethod
    def resolve_get_all_wards(self, info, district_unique_id, **kwargs):
        filters = Q(is_active=True,
                    ward_district__unique_id=district_unique_id)

        query_set = Wards.objects.filter(filters).only('unique_id')
        resp_data = [SettingsBuilder.get_ward_data(id=query.unique_id) for query in query_set]

        return info.return_type.graphene_type(response=ResponseObject.get_response(id=1), data=resp_data)
    
    @staticmethod
    def resolve_get_full_location(self, info, street_unique_id, **kwargs):
        filters = Q(is_active=True, unique_id = street_unique_id)

        query_set = Streets.objects.filter(filters).only('unique_id')
        resp_data = [SettingsBuilder.get_full_location_data(id=query.unique_id) for query in query_set]

        return info.return_type.graphene_type(response=ResponseObject.get_response(id=1), data=resp_data)