from datetime import timedelta
import logging
import random
import threading
import time
import traceback
import uuid
from typing import Any, Dict, Optional

from django.conf import settings
from django.core.cache import cache
from django.utils import timezone
from oauth2_provider.models import AccessToken
from myapp_accounts.models import ActivateAccountToken, ForgotPasswordRequestUser, Profile
from django.contrib.auth.models import User

from myapp_auth.models import UserPermissions
from myapp_utils.authentication import Authentication
from myapp_utils.notifications_utils import NotificationServices

CACHE_TTL_SECONDS = getattr(settings, "USER_CONTEXT_CACHE_TTL", 60 * 60)
logger = logging.getLogger(__name__)


class UserUtils:
    """
    Utilities for extracting a compact, cached 'user context' from a DOT access token or request.user.
    Returns context as: {"user": { ... }} for backward compatibility with existing callers.
    """

    def __init__(self, request):
        self.request = request
    
    @staticmethod
    def get_user(request=None, user=None):
        is_authenticated = False
        user_data = {}
        if not user:
            is_authenticated, user = Authentication.authenticate(request)
            if not is_authenticated and not user:
                return {}

            cached_data = cache.get(user.id)
            if cached_data:
                return cached_data
            
            profile = Profile.objects.filter(user=user).first()
            if not profile:
                return user_data
        else:
            profile = Profile.objects.filter(user=user).first()
            if not profile:
                return user_data
            
        # Set Profile Permissions
        user_permissions = [permission.permission.permission_code for permission in profile.get_user_permissions()]
        user_data.update({'permissions': user_permissions})
        
        # Set Profile Role
        if profile.get_user_role():
            user_data.update({'role': profile.get_user_role().role_name})
            
        user_data.update(
            {
                "id": str(profile.user_id),
                "unique_id": str(profile.unique_id),
                'account_type': profile.account_type,
                "phone_number": profile.phone_number,
            }
        )
        cache.set(user.id, user_data)
        return user_data
    
    def get_manufacturer(request=None, user=None):
        is_authenticated = False
        user_data = {}
        if not user:
            is_authenticated, user = Authentication.authenticate(request)
            if not is_authenticated and not user:
                return {}

            cached_data = cache.get(user.id)
            if cached_data:
                return cached_data
            
            profile = Profile.objects.filter(user=user).first()
            if not profile:
                return user_data
        else:
            profile = Profile.objects.filter(user=user).first()
            if not profile:
                return user_data
            
        # Set Profile Permissions
        user_permissions = [permission.permission.permission_code for permission in profile.get_user_permissions()]
        user_data.update({'permissions': user_permissions})
        
        # Set Profile Role
        if profile.get_user_role():
            user_data.update({'role': profile.get_user_role().role_name})
            
        user_data.update(
            {
                "id": str(profile.user_id),
                "unique_id": str(profile.unique_id),
                'account_type': profile.account_type,
                "phone_number": profile.phone_number,
            }
        )
        cache.set(user.id, user_data)
        return user_data
    # --------- Public: Field helpers (kept for backward compatibility) ---------
    @staticmethod
    def __profile__(info) -> Optional['Profile']:
        unique_id = UserUtils.get_user(info).get("unique_id")
        if not unique_id:
            return None
        return Profile.objects.select_related("user").filter(unique_id=unique_id).first()
    
    @staticmethod
    def __manufacturer_profile__(info) -> Optional['Profile']:
        unique_id = UserUtils.get_user(info).get("unique_id")
        if not unique_id:
            return None
        return Profile.objects.select_related("user").filter(unique_id=unique_id).first()
    
    @staticmethod
    def __profile_unique_id__(info)->Optional[str]:
        return UserUtils.get_user(info).get("unique_id")
    
    @staticmethod
    def __profile_id__(info) -> Optional[str]:
        return UserUtils.get_user(info).get('id')
    
    @staticmethod
    def __usertype__(info) -> Optional[str]:
        return UserUtils.get_user(info).get("account_type")

    @staticmethod
    def __designation__(request, process=None) -> Optional[str]:
        ctx = UserUtils._safe_ctx_from_request(request)
        return ctx.get("user", {}).get("designation_unique_id")

    @staticmethod
    def __designation_name__(request, process=None) -> Optional[str]:
        ctx = UserUtils._safe_ctx_from_request(request)
        return ctx.get("user", {}).get("designation_name")

    @staticmethod
    def __username__(request, process=None) -> Optional[str]:
        ctx = UserUtils._safe_ctx_from_request(request)
        return ctx.get("user", {}).get("username")

    @staticmethod
    def __permissions__(request) -> list[str]:
        ctx = UserUtils._safe_ctx_from_request(request)
        return ctx.get("user", {}).get("permissions", [])


    # --------- Internal helpers ---------
    @staticmethod
    def _safe_ctx_from_request(request) -> Dict[str, Any]:
        """
        Best-effort retrieval of {"user": {...}} context from the request’s Bearer token.
        Mirrors the previous pattern but is robust to missing/invalid headers.
        """
        try:
            token = UserUtils._get_bearer_token_from_request(request)
            if not token:
                # Fall back to request.user if available
                if hasattr(request, "user") and request.user and request.user.is_authenticated:
                    return UserUtils._context_from_user(request.user)
                return {}
            return UserUtils.get_user(token=token) or {}
        except (KeyError, ValueError):
            return {}
        except Exception:
            traceback.print_exc()
            return {}

    @staticmethod
    def _get_bearer_token_from_request(request) -> Optional[str]:
        """
        Extract 'Bearer <token>' from Authorization header. Returns <token> or None.
        """
        auth_header = UserUtils._get_header(request, "Authorization")
        if not auth_header:
            return None
        parts = auth_header.split()
        if len(parts) == 2 and parts[0].lower() == "bearer":
            return parts[1]
        return None

    @staticmethod
    def _get_header(request, key: str) -> Optional[str]:
        """
        Case-insensitive header fetch supporting both DRF's .headers and Django's META,
        plus GraphQL/HttpHeaders compatibility.
        """
        # 1️⃣ DRF or ASGI request with .headers
        if hasattr(request, "headers") and request.headers:
            try:
                val = request.headers.get(key)
                if val is not None:
                    return val
            except Exception:
                pass

        # 2️⃣ Django request with .META
        if hasattr(request, "META"):
            meta_key = "HTTP_" + key.upper().replace("-", "_")
            return request.META.get(meta_key)

        # 3️⃣ If request itself *is* headers-like (GraphQL)
        if isinstance(request, dict) and key in request:
            return request.get(key)

        # 4️⃣ If request is a HttpHeaders object (like from GraphQL)
        if hasattr(request, "get") and callable(request.get):
            try:
                return request.get(key)
            except Exception:
                pass

        return None

    @staticmethod
    def _ck_token(token: str) -> str:
        return f"userctx:token:{token}"

    @staticmethod
    def _ck_user(username: str) -> str:
        return f"userctx:user:{username}"

    @staticmethod
    def _context_from_token(token: str) -> Optional[Dict[str, Any]]:
        """
        Build user context from a DOT AccessToken. Returns {"user": {...}} or None.
        """
        try:
            at = (
                AccessToken.objects
                .select_related("user")
                .only("token", "expires", "user__id", "user__username", "user__is_active")
                .get(token=token)
            )
        except AccessToken.DoesNotExist:
            return None

        # Basic validity checks
        if at.expires <= timezone.now():
            return None
        if not at.user or not at.user.is_active:
            return None

        # Try username cache first
        username = at.user.username
        cached_by_user = cache.get(UserUtils._ck_user(username))
        if cached_by_user is not None:
            return cached_by_user

        # Build fresh and cache
        ctx = UserUtils._build_user_context(at.user)
        cache.set(UserUtils._ck_user(username), ctx, CACHE_TTL_SECONDS)
        return ctx

    @staticmethod
    def _context_from_user(user) -> Dict[str, Any]:
        """
        Build user context from a Django user instance, with caching by username.
        """
        if not user or not getattr(user, "is_authenticated", False):
            return {}
        ck = UserUtils._ck_user(user.username)
        cached = cache.get(ck)
        if cached is not None:
            return cached
        ctx = UserUtils._build_user_context(user)
        cache.set(ck, ctx, CACHE_TTL_SECONDS)
        return ctx

    @staticmethod
    def _build_user_context(user) -> Dict[str, Any]:
        """
        Hit your domain models to assemble the compact context.
        Mirrors (and improves) the structure you had before.
        Returns {"user": {...}}.
        """
        # Profile
        profile = (Profile.objects.select_related("user").only("unique_id","organization","phone_number","user__username","user__id").filter(user=user).first())
        if not profile:
            return {"user": {"display_name": getattr(user, "display_name", None)}}

        # Role & permissions (follow your relations; keep minimal fields)
        permissions = []
        assigned_role = getattr(profile.user, "user_role", None)

        if assigned_role:
            role_permissions_qs = assigned_role.role.role_permission.select_related("permission").only(
                "permission__permission_code"
            )
            permissions = [rp.permission.permission_code for rp in role_permissions_qs]

        ctx_user = {
            "id": str(profile.primary_key),
            "unique_id": str(profile.unique_id),
            "instituion": profile.organization.unique_id if profile.organization else None,
            "organization": profile.organization,
            'account_type': profile.account_type,
            "display_name": profile.display_name,
            "phone_number": profile.phone_number,
            "permissions": permissions,
        }

        return {"user": ctx_user}

    @classmethod
    def has_permission(cls, request, permissions: list[str], check_both: bool = False) -> bool:
        user_perms = cls.__permissions__(request)
        if check_both:
            # Check for both permissions
            for perm in permissions:
                if perm not in user_perms:
                    return False
            return True
        else:
            # Check for either permission
            return any(perm in user_perms for perm in permissions)
    
    @classmethod
    def generate_token(cls, expires_in=3600):
        """
        Generate a unique verification token for account activation or password reset.
        """
        request_token = str(uuid.uuid4())
        # Set expiration time
        expires_at = timezone.now() + timedelta(seconds=expires_in)
        print(f"[TOKEN GENERATED] Token: {request_token}, Expires At: {expires_at}")
        return request_token, expires_at
    
    @classmethod
    def generate_verification_code(cls, user, expires_in=86400):
        """
        Generate and store an account activation token for the given user.
        """
        token, expires_at = cls.generate_token(expires_in=expires_in)  # Token valid for 24 hours
        ActivateAccountToken.objects.create(
            user=user,
            token=token,
            is_used=False,
            expiration_time=expires_at
        )

        # Call function to delete user if not activated within expiration time (not implemented here)
        threading.Thread(target=cls._schedule_user_deletion, args=(user, expires_in), daemon=True).start()
        return token

    @classmethod
    def generate_reset_code(cls, user):
        """
        Generate and store a password reset token for the given user.
        """
        token, expires_at = cls.generate_token(expires_in=600)  # Token valid for 10 minutes
        ForgotPasswordRequestUser.objects.create(
            user=user,
            token=token,
            is_used=False,
            expiration_time=expires_at
        )

        return token
    
    @classmethod
    def _schedule_user_deletion(cls, user: User, expires_in):
        """
        Wait for expiration period and delete user if still inactive.
        """
        # Sleep for the token lifetime
        time.sleep(expires_in)
        # Check if user is still inactive and delete
        if user.is_active:
            return

        token = ActivateAccountToken.objects.filter(user__user=user, is_used=False).first()

        if token and token.expiration_time < timezone.now() and not user.is_active:
            print(f"[AUTO DELETE] Removing unactivated user: {user.username}")
            Profile.objects.filter(user=user).delete()
            token.delete()
            user.delete()

    @classmethod
    def send_phone_verification_otp(cls, profile: Profile) -> Optional[str]:
        """
        Send a phone verification OTP to the given user's phone number.
        Stores the OTP in cache with a 10-minute expiry.
        Retries SMS up to 3 times before failing.
        Returns the OTP if successfully sent, otherwise None.
        """
        if not profile.phone_number:
            print("Profile %s has no phone number.", profile.id)
            return None

        # Generate 6-digit OTP
        otp = f"{random.randint(100000, 999999)}"

        # Build cache key (unique per phone)
        cache_key = f"phone_otp_{profile.phone_number}"

        # Store in cache for 10 minutes (600 seconds)
        cache.set(cache_key, otp, timeout=600)

        sms_payload = {
            "reciver": profile.phone_number,
            "message_body": f"Your verification code is {otp}. It expires in 10 minutes."
        }

        # Send with retry logic
        for attempt in range(3):
            success = NotificationServices.shared_send_sms_notification(**sms_payload)
            if success:
                print(f"OTP {otp} sent to {profile.phone_number} (attempt {attempt + 1})")
                return otp

            print("Failed to send OTP to %s (attempt %d)", profile.phone_number, attempt + 1)
            time.sleep(1.5)

        logger.error("Failed to send OTP to %s after 3 attempts.", profile.phone_number)
        cache.delete(cache_key)
        return None

    @classmethod
    def verify_phone_otp(cls, profile: Profile, otp: str) -> bool:
        """
        Verify a phone OTP stored in cache.
        Returns True if valid, False otherwise.
        """
        cache_key = f"phone_otp_{profile.phone_number}"
        cached_otp = cache.get(cache_key)

        if not cached_otp:
            logger.info("OTP for %s expired or not found.", profile.phone_number)
            return False

        if str(cached_otp) != str(otp):
            logger.info("Invalid OTP for %s: received %s", profile.phone_number, otp)
            return False

        # OTP matches → clear it
        cache.delete(cache_key)
        logger.info("OTP for %s verified successfully.", profile.phone_number)
        profile.phone_verified = True
        profile.save(update_fields=["phone_verified"])
        return True


