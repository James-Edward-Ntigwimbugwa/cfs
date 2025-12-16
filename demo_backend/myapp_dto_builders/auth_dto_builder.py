from myapp_auth.models import *
from myapp_dto.auth_dto import UserPermissionsGroupObject, UserPermissionsObject, UserRolesObject
from myapp_utils.cache_utils import  get_cached_model_or_db

class AuthBuilder:
    @classmethod
    def get_role_data(cls, id):
        query_set = UserRoles.objects.filter(unique_id = id).first()
        if not query_set:
            return None

        permissions_list = []
        for permission in query_set.get_role_permissions:
            permissions_list.append(cls.get_permission_data(id=permission.permission.unique_id))

        return UserRolesObject(
            id=query_set.primary_key,
            unique_id=query_set.unique_id,
            is_active=query_set.is_active,
            role_name=query_set.role_name,
            role_type=query_set.role_type,
            role_description=query_set.role_name,
            role_createddate=query_set.created_at,
            permissions=permissions_list,
        )

    @classmethod
    def get_permission_group_data(cls, id):
        query_set: UserPermissionsGroup = get_cached_model_or_db(UserPermissionsGroup, id)
        if not query_set:
            return None

        return UserPermissionsGroupObject(
            id=query_set.primary_key,
            unique_id=query_set.unique_id,
            is_active=query_set.is_active,
            group_name=query_set.group_name,
            group_description=query_set.group_description,
            group_permissions=list(map(lambda permission: cls.get_permission_data(id=permission.unique_id), query_set.permission_group.filter(is_active=True).all())),
        )

    @classmethod
    def get_permission_data(cls, id):
        query_set: UserPermissions = get_cached_model_or_db(UserPermissions, id)
        if not query_set:
            return None

        return UserPermissionsObject(
            id=query_set.primary_key,
            unique_id=query_set.unique_id,
            is_active=query_set.is_active,
            permission_name=query_set.permission_name,
            permission_code=query_set.permission_code,
            is_global=query_set.is_global,
            created_at=query_set.created_at,
        )
    

