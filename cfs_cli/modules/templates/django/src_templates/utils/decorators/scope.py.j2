from provider.oauth2.models import AccessToken
from functools import wraps
from graphql import GraphQLError

def has_scope(required_scope):
    def decorator(func):
        @wraps(func)
        def wrapper(cls, root, info, *args, **kwargs):
            token_header = info.context.META.get("HTTP_AUTHORIZATION", "")
            token = token_header.replace("Bearer ", "")

            try:
                access_token = AccessToken.objects.select_related("client").get(token=token)
                if required_scope not in access_token.get_scope_string().split():
                    raise GraphQLError("Permission denied: insufficient scope")
            except AccessToken.DoesNotExist:
                raise GraphQLError("Invalid or missing access token")
            return func(cls, root, info, *args, **kwargs)
        return wrapper
    return decorator
