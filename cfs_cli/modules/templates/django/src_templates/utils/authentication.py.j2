from django.utils.timezone import now
from django.contrib.auth.backends import BaseBackend
from oauth2_provider.models import Application, AccessToken


class Authentication(BaseBackend):
    """
    Custom authentication backend using Django OAuth Toolkit.
    Supports GraphQL `info.context` or standard Django `request`.
    """

    def authenticate_header(self, request):
        return "Bearer"

    @staticmethod
    def authenticate(info):
        """
        Authenticates a GraphQL request based on the Bearer token in headers.
        Returns (success: bool, user: User|None)
        """
        try:
            # Detect whether 'info' is a GraphQL ResolveInfo or a WSGIRequest
            if hasattr(info, "context") and hasattr(info.context, "headers"):
                # GraphQL 'info'
                headers = info.context.headers
            elif hasattr(info, "headers"):
                # Direct Django WSGIRequest
                headers = info.headers
            else:
                return False, None
            
            authorization_header = headers.get("Authorization")

            if not authorization_header or not authorization_header.startswith("Bearer "):
                return False, None

            # Extract token value
            bearer_token = authorization_header.split(" ")[1]

            # Get latest application (you might want to improve this for multi-client setups)
            application = Application.objects.last()

            # Validate token
            token = AccessToken.objects.filter(
                token=bearer_token,
                application=application,
                expires__gt=now(),
            ).select_related("user").first()

            if token:
                return True, token.user

            return False, None

        except Exception:
            # Log internally if needed
            return False, None

    @classmethod
    def get_authenticated_user(cls, request):
        """
        Simplified authentication check for middleware or REST views.
        """
        if hasattr(request, "user") and request.user.is_authenticated:
            return True

        auth_header = request.META.get("HTTP_AUTHORIZATION", "")
        if not auth_header.startswith("Bearer "):
            return False

        try:
            class MockInfo:
                class context:
                    headers = {"Authorization": auth_header}

            success, _ = cls.authenticate(MockInfo())
            return success
        except Exception:
            return False
