import logging
from myapp_accounts.models import *
from myapp_dto.accounts_dto import *
from myapp_dto_builders.auth_dto_builder import AuthBuilder
from myapp_utils.cache_utils import get_cached_model_or_db
logger = logging.getLogger(__name__)

class AccountBuilder:
    @classmethod
    def get_profile_data(cls, id):
        query_set: Profile = get_cached_model_or_db(Profile, id)
        if not query_set:
            return None
        
        user_role = getattr(query_set.user, "user_role", None)

        return ProfileObject(
            id=query_set.primary_key,
            unique_id=query_set.unique_id,
            first_name=query_set.user.first_name,
            last_name=query_set.user.last_name,
            email=query_set.user.email,
            phone_number=query_set.phone_number,
            location=query_set.location,
            is_verified=query_set.is_verified,
            phone_verified=query_set.phone_verified,    
            is_active=query_set.is_active,
            account_type = query_set.account_type or None,
            created_at= query_set.created_at if query_set.created_at else None,
            role=AuthBuilder.get_role_data(user_role.role.unique_id) if user_role else None
        )