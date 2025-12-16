import logging
import traceback
import graphene
from dotenv import dotenv_values
from django.db import transaction
from django.contrib.auth.models import User
from myapp_dto.accounts_dto import ActivateOrDeactivateUserInput, ChangePasswordInputObject, OTPVerificationInputObject, ProfileInputObject, ProfileObject, ResetPasswordInputObject, SignupWithGMSInputObject
from myapp_dto.enums import AccountsTypeChoices
from myapp_utils.decorators.permission import login_required
from myapp_utils.utils import Utils
from .models import ActivateAccountToken, ForgotPasswordRequestUser, Profile
from myapp_dto.shared_dto import ResponseObject
from myapp_utils.validators.input_validator import InputValidator
from myapp_dto_builders.accounts_builder import AccountBuilder
from myapp_utils.user_utils import UserUtils
from django.contrib.auth import authenticate
from django.utils import timezone
from django.core.cache import cache
import time
config = dotenv_values('.env')
logger = logging.getLogger(__name__)


# -------------------------------------------------
# User registartion and onboarding mutations
# -------------------------------------------------
class CreateAccountMutation(graphene.Mutation):
    class Arguments:
        input = ProfileInputObject(required=True)

    response = graphene.Field(ResponseObject)
    data = graphene.Field(ProfileObject)

    @classmethod
    def mutate(cls, root, info, input):
        # Check if passwords match
        if input.password != input.confirm_password:
            return cls(ResponseObject.get_response(id=10, message="Passwords do not match"), data=None)

        if not InputValidator.is_valid_email(input.email):
            return cls(ResponseObject.get_response(id=10, message="Invalid email provided."), data=None)

        profile_user, created = User.objects.get_or_create(
            username=input.email,
            defaults={
                'first_name': input.first_name,
                'last_name': input.last_name,
                'email': input.email,
                'is_active': False
            }
        )

        if not created:
            return cls(ResponseObject.get_response(id=3, message="Unable to complete registration with provided details"), data=None)

        profile_user.set_password(input.password)
        profile_user.save()

        v_result = Utils.validate_and_normalize_phone(input.phone_number)
        if not v_result['is_valid']:
            transaction.rollback()
            return cls(ResponseObject.get_response(id=10, message=v_result['message']), data=None)

        profile, _ = Profile.objects.update_or_create(
            user=profile_user,
            defaults={
                'phone_number': v_result['normalized']
            }
        )

        # Send account activation email
        UserUtils.generate_verification_code(profile)

        data = AccountBuilder.get_profile_data(id=profile.unique_id)
        return cls(ResponseObject.get_response(id=1), data=data)


class ActivateAccountMutation(graphene.Mutation):
    class Arguments:
        token = graphene.String(required=True)

    response = graphene.Field(ResponseObject)
    data = graphene.Field(ProfileObject)

    @classmethod
    def mutate(cls, root, info, token):
        try:
            activation_token = ActivateAccountToken.objects.filter(
                token=token, is_used=False).first()
            if activation_token is None:
                return cls(ResponseObject.get_response(id=9, message='Activation token not found.'))

            if activation_token.expiration_time < timezone.now():
                return cls(ResponseObject.get_response(id=17, message='Activation token has expired.'))

            profile = Profile.objects.filter(
                primary_key=activation_token.user.primary_key).first()
            if profile is None:
                return cls(ResponseObject.get_response(id=9, message='Profile not found for the user.'))

            profile.user.is_active = True
            profile.user.save(update_fields=['is_active'])

            profile.is_active = True
            profile.save(update_fields=['is_active'])

            activation_token.is_used = True
            activation_token.save()

            # Verify the phone number if exists by sending OTP
            if profile.phone_number:
                UserUtils.send_phone_verification_otp(profile)

            data = AccountBuilder.get_profile_data(id=profile.unique_id)
            return cls(ResponseObject.get_response(id=1), data=data)
        except Exception as e:
            logger.error(f'ActivateAccountMutation :: {e}')
            traceback.print_exc()
            return cls(ResponseObject.get_response(id=5))


class UpdateAccountMutation(graphene.Mutation):
    class Arguments:
        input = ProfileInputObject(required=True)

    response = graphene.Field(ResponseObject)
    data = graphene.Field(ProfileObject)

    @classmethod
    @login_required()
    def mutate(cls, root, info, input):
        if not InputValidator.is_valid_email(input.email):
            return cls(ResponseObject.get_response(id=10, message="Invalid email provided."), data=None)

        profile = Profile.objects.filter(unique_id=input.unique_id).first()
        if profile is None:
            return cls(ResponseObject.get_response(id=9, message="Profile not found"), data=None)

        profile.user.first_name = input.first_name
        profile.user.last_name = input.last_name
        profile.user.email = input.email
        profile.user.save()

        # Update profile fields if provided
        v_result = Utils.validate_and_normalize_phone(input.phone_number)
        if not v_result['is_valid']:
            transaction.set_rollback(True)
            return cls(ResponseObject.get_response(id=10, message=v_result['message']), data=None)

        profile.phone_number = v_result['normalized']
        profile.job_title = input.job_title
        profile.display_name = input.display_name
        profile.name_pronunciation = input.name_pronunciation
        profile.pronouns = input.pronouns
        profile.share_pronouns = input.share_pronouns
        profile.location = input.location
        profile.department = input.department
        profile.save()

        data = AccountBuilder.get_profile_data(id=profile.unique_id)
        return cls(ResponseObject.get_response(id=1), data=data)


# -------------------------------------------------
# Admin user management mutations
# -------------------------------------------------
class CreateAdminUserMutation(graphene.Mutation):
    class Arguments:
        input = ProfileInputObject(required=True)

    response = graphene.Field(ResponseObject)
    data = graphene.Field(ProfileObject)

    @classmethod
    @login_required(permissions=['can_create_system_users'], user_types=['SYSTEM_ADMIN'])
    def mutate(cls, root, info, input):
        profile_user, _ = User.objects.update_or_create(
            username=input.email,
            defaults={
                'first_name': input.first_name,
                'last_name': input.last_name,
                'email': input.email,
                'is_active': True
            }
        )

        v_result = Utils.validate_and_normalize_phone(input.phone_number)
        if not v_result['is_valid']:
            transaction.set_rollback(True)
            return cls(ResponseObject.get_response(id=10, message=v_result['message']), data=None)

        profile, _ = Profile.objects.update_or_create(
            user=profile_user,
            defaults={
                'job_title': input.job_title,
                'phone_number': v_result['normalized'],
                'is_verified': True,
                'public_servant': True,
                'account_type': AccountsTypeChoices.SUPER_ADMIN.value,
            }
        )

        data = AccountBuilder.get_profile_data(id=profile.unique_id)
        return cls(ResponseObject.get_response(id=1), data=data)


class UpdateAdminUserMutation(graphene.Mutation):
    class Arguments:
        input = ProfileInputObject(required=True)

    response = graphene.Field(ResponseObject)
    data = graphene.Field(ProfileObject)

    @classmethod
    @login_required(permissions=['can_create_system_users'], user_types=['SYSTEM_ADMIN'])
    def mutate(cls, root, info, input):
        # Find profile
        query_set = Profile.objects.filter(unique_id=input.unique_id).first()
        if not query_set:
            return cls(ResponseObject.get_response(9, "User with this id doesn't exit"), data=None)

        # Update profile fields
        query_set.user.first_name = input.first_name
        query_set.user.last_name = input.last_name
        query_set.user.email = input.email
        query_set.user.save()

        query_set.phone_number = input.phone_number
        query_set.location = input.location
        query_set.save()

        data = AccountBuilder.get_profile_data(id=query_set.unique_id)
        return cls(ResponseObject.get_response(id=1), data=data)


class DeleteAdminUserMutation(graphene.Mutation):
    class Arguments:
        unique_id = graphene.String(required=True)

    response = graphene.Field(ResponseObject)

    @classmethod
    @login_required(permissions=['can_create_system_users'], user_types=['SYSTEM_ADMIN'])
    def mutate(cls, root, info, unique_id):
        query_set = Profile.objects.filter(unique_id=unique_id).first()
        if not query_set:
            return cls(ResponseObject.get_response(id=9, message='User with that ID does not exist'))

        query_set.is_active = False
        query_set.save()

        query_set.user.is_active = False
        query_set.user.save()
        return cls(ResponseObject.get_response(id=1))


# -------------------------------------------------
# Upgrade User to Institution admin
# -----------------------------------------------
class UpgradeUserToInstitutionAdminMutation(graphene.Mutation):
    class Arguments:
        unique_id = graphene.String(required=True)

    response = graphene.Field(ResponseObject)
    data = graphene.Field(ProfileObject)

    @classmethod
    @login_required(permissions=['can_create_user'], user_types=['SYSTEM_ADMIN'])
    def mutate(cls, root, info, unique_id):
        query_set = Profile.objects.filter(unique_id=unique_id).first()
        if not query_set:
            return cls(ResponseObject.get_response(id=9, message='User with that ID does not exist'))

        query_set.account_type = AccountsTypeChoices.DISTRIBUTOR.value
        query_set.save(update_fields=['account_type'])
        return cls(ResponseObject.get_response(id=1))


# -------------------------------------------------
# Admin user management mutations
# -------------------------------------------------
class ChangeUserPasswordMutation(graphene.Mutation):
    class Arguments:
        input = ChangePasswordInputObject(required=True)

    response = graphene.Field(ResponseObject)

    @classmethod
    # @login_required()
    def mutate(cls, root, info, input):
        try:
            profile_unique_id = UserUtils.__profile__(info.context)
            profile_user = Profile.objects.filter(
                unique_id=profile_unique_id, is_active=True).first()
            if profile_user is None:
                return cls(ResponseObject.get_response(id=5))

            if not authenticate(username=profile_user.user.username, password=input.old_password):
                return cls(ResponseObject.get_response(id=58))

            profile_user.user.set_password(input.new_password)
            profile_user.user.save()

            # TODO Revoke any token associated with this current passwd

            return cls(ResponseObject.get_response(id=1))
        except Exception as _e:
            return cls(ResponseObject.get_response(id=5))


class ActivateOrDeactivateUserMutation(graphene.Mutation):
    class Arguments:
        input = ActivateOrDeactivateUserInput(required=True)

    response = graphene.Field(ResponseObject)
    data = graphene.Field(ProfileObject)

    @classmethod
    @login_required(permissions=['can_create_user'], user_types=['SYSTEM_ADMIN'])
    def mutate(cls, root, info, input):
        query_set = Profile.objects.filter(unique_id=input.unique_id).first()
        if not query_set:
            return cls(ResponseObject.get_response(id=9, message="User with this id doesn't exit"))

        if input.deactivate is None:
            return cls(ResponseObject.get_response(id=2, message="Deactivate field is required"))

        query_set.user.is_active = not input.deactivate
        query_set.user.save()

        query_set.is_active = not input.deactivate
        query_set.save()

        data = AccountBuilder.get_profile_data(id=query_set.unique_id)

        return cls(ResponseObject.get_response(id=1), data=data)


# -------------------------------------------------
# Password reset mutations
# -------------------------------------------------

class ForgotPasswordMutation(graphene.Mutation):
    class Arguments:
        email = graphene.String(required=True)

    response = graphene.Field(ResponseObject)

    @classmethod
    def mutate(cls, root, info, email):
        if not InputValidator.is_valid_email(email):
            return cls(ResponseObject.get_response(id=2), data=None)

        user = User.objects.filter(username=email).first()
        if user is None:
            return cls(response=ResponseObject.get_response(id=9))

        # Verify if user has reset request that is not used and not expired
        existing_request = ForgotPasswordRequestUser.objects.filter(
            user__user=user, is_used=False, expiration_time__gt=timezone.now()).first()
        if existing_request:
            return cls(ResponseObject.get_response(id=1, message="A password reset request is already active. Please check your email."))

        user_profile = Profile.objects.filter(user=user).first()
        UserUtils.generate_reset_code(user_profile)
        return cls(ResponseObject.get_response(id=1))


class ResetForgotedPasswordMutation(graphene.Mutation):
    class Arguments:
        input = ResetPasswordInputObject()

    response = graphene.Field(ResponseObject)

    @classmethod
    def mutate(cls, root, info, input):
        reset_request = ForgotPasswordRequestUser.objects.filter(
            token=input.request_token, is_used=False).first()
        if reset_request is None:
            return cls(ResponseObject.get_response(id=9, message='Invalid or used reset token.'))

        if reset_request.expiration_time < timezone.now():
            return cls(ResponseObject.get_response(id=17, message='Reset token has expired.'))

        profile = Profile.objects.filter(user=reset_request.user).first()
        if profile is None:
            return cls(ResponseObject.get_response(id=9, message='Profile not found for the user.'))

        profile.user.set_password(input.password)
        profile.user.save()
        reset_request.is_used = True
        reset_request.save()

        return cls(ResponseObject.get_response(id=1, message='Password has been reset successfully.'))


# -------------------------------------------------
# Update User Phone Number, Validate and Resend OTP mutation
# -------------------------------------------------
class UpdateUserPhoneNumberMutation(graphene.Mutation):
    class Arguments:
        input = ProfileInputObject(required=True)

    response = graphene.Field(ResponseObject)
    data = graphene.Field(ProfileObject)

    @classmethod
    @login_required()
    def mutate(cls, root, info, input):
        profile_unique_id = UserUtils.__profile__(info.context)
        profile = Profile.objects.filter(unique_id=profile_unique_id).first()
        if profile is None:
            return cls(ResponseObject.get_response(id=9, message="Profile not found"), data=None)

        profile.phone_number = input.phone_number
        profile.save(update_fields=['phone_number'])

        # Send OTP to the new phone number for verification
        UserUtils.send_phone_verification_otp(profile)
        data = AccountBuilder.get_profile_data(id=profile.unique_id)
        return cls(ResponseObject.get_response(id=1), data=data)


class ResendOTPMutation(graphene.Mutation):
    class Arguments:
        phone_number = graphene.String(required=True)

    response = graphene.Field(ResponseObject)
    resend_time = graphene.Int()

    @classmethod
    def mutate(cls, root, info, phone_number):
        try:
            # Cache keys
            resend_time_key = f"resend_time_{phone_number}"
            resend_count_key = f"resend_count_{phone_number}"

            # Prevent too frequent resends
            resend_time = cache.get(resend_time_key)
            resend_count = cache.get(resend_count_key) or 0

            if resend_time and resend_time > time.time():
                wait_for = int(resend_time - time.time())
                return cls(response=ResponseObject(id="5", message=f"OTP already sent. Please wait {wait_for} seconds before requesting again."), resend_time=wait_for)

            # Validate phone number exists
            profile = Profile.objects.filter(phone_number=phone_number).first()
            if not profile:
                return cls(response=ResponseObject.get_response(id=4, message="Phone number not found."), resend_time=0)

            # Send OTP using shared utils
            otp = UserUtils.send_phone_verification_otp(profile)
            if not otp:
                return cls(response=ResponseObject.get_response(id=5, message="Failed to send OTP."), resend_time=0)

            # Increase resend delay progressively, capped at 5 minutes
            new_resend_count = resend_count + 1
            new_resend_time = min(60 * 5, 60 * 2 ** new_resend_count)
            cache.set(resend_time_key, time.time() + new_resend_time)
            cache.set(resend_count_key, new_resend_count)

            return cls(response=ResponseObject.get_response(id=1, message="OTP resent successfully."), resend_time=new_resend_time)

        except Exception as e:
            logger.error(f"ResendOTPMutation :: {e}")
            traceback.print_exc()
            return cls(response=ResponseObject.get_response(id=5, message="Unexpected error occurred."), resend_time=0)


class VefifyOTPMutation(graphene.Mutation):
    class Arguments:
        input = OTPVerificationInputObject(required=True)

    response = graphene.Field(ResponseObject)

    @classmethod
    def mutate(cls, root, info, input):
        try:
            profile = Profile.objects.filter(
                phone_number=input.phone_number).first()

            print("------------------PROFILE----------------------", profile)
            if not profile:
                return cls(response=ResponseObject.get_response(id=4, message="Phone number not found."))

            is_valid_otp = UserUtils.verify_phone_otp(profile, input.otp)
            if not is_valid_otp:
                return cls(response=ResponseObject.get_response(id=6, message="Invalid OTP provided."))

            profile.phone_verified = True
            profile.is_verified = True
            profile.save(update_fields=['phone_verified'])

            return cls(response=ResponseObject.get_response(id=1, message="Phone number verified successfully."))

        except Exception as e:
            logger.error(f"VefifyOTPMutation :: {e}")
            traceback.print_exc()
            return cls(response=ResponseObject.get_response(id=5, message="Unexpected error occurred."))


# TODO Complete this logic
class InitiatePasswordResetMutation(graphene.Mutation):
    class Arguments:
        unique_id = graphene.String(required=True)

    response = graphene.Field(ResponseObject)

    @classmethod
    @login_required(user_types=['SYSTEM_ADMIN', 'ORGANIZATION_ADMIN'])
    def mutate(cls, root, info, unique_id):
        query_set = Profile.objects.filter(unique_id=unique_id).first()
        if not query_set:
            return cls(ResponseObject.get_response(id=9, message='User with that ID does not exist'))

        query_set.account_type = AccountsTypeChoices.DISTRIBUTOR.value
        query_set.save(update_fields=['account_type'])
        return cls(ResponseObject.get_response(id=1))


class Mutation(graphene.ObjectType):
    create_account_mutation = CreateAccountMutation.Field(
        description="PERMISSIONS=[], USER_TYPES=[], AUTHENTICATED = Flase")
    activate_account_mutation = ActivateAccountMutation.Field(
        description="PERMISSIONS=[], USER_TYPES=[], AUTHENTICATED = Flase")
    update_account_mutation = UpdateAccountMutation.Field(
        description="PERMISSIONS=[], USER_TYPES=[], AUTHENTICATED = True")

    create_admin_user_mutation = CreateAdminUserMutation.Field(
        description="PERMISSIONS=['can_create_system_users'], USER_TYPES=['SYSTEM_ADMIN']")
    update_admin_user_mutation = UpdateAdminUserMutation.Field(
        description="PERMISSIONS=['can_create_system_users'], USER_TYPES=['SYSTEM_ADMIN']")
    delete_admin_user_mutation = DeleteAdminUserMutation.Field(
        description="PERMISSIONS=['can_create_system_users'], USER_TYPES=['SYSTEM_ADMIN']")

    upgrade_user_to_institution_admin_mutation = UpgradeUserToInstitutionAdminMutation.Field(
        description="PERMISSIONS=['can_create_system_users'], USER_TYPES=['SYSTEM_ADMIN']")

    change_user_password_mutation = ChangeUserPasswordMutation.Field(
        description="PERMISSIONS=['can_create_system_users'], USER_TYPES=['SYSTEM_ADMIN']")
    activate_or_dectivate_user_mutation = ActivateOrDeactivateUserMutation.Field(
        description="PERMISSIONS=['can_create_system_users'], USER_TYPES=['SYSTEM_ADMIN']")

    forgot_password_mutation = ForgotPasswordMutation.Field(
        description="PERMISSIONS=[], USER_TYPES=[], AUTHENTICATED = Flase")
    reset_forgoted_password_mutation = ResetForgotedPasswordMutation.Field(
        description="PERMISSIONS=[], USER_TYPES=[], AUTHENTICATED = Flase")

    update_user_phone_number_mutation = UpdateUserPhoneNumberMutation.Field(
        description="PERMISSIONS=[], USER_TYPES=[], AUTHENTICATED = True")
    resend_otp_mutation = ResendOTPMutation.Field(
        description="PERMISSIONS=[], USER_TYPES=[], AUTHENTICATED = Flase")
    verify_otp_mutation = VefifyOTPMutation.Field(
        description="PERMISSIONS=[], USER_TYPES=[], AUTHENTICATED = Flase")

    initiate_password_reset_mutation = InitiatePasswordResetMutation.Field(
        description="PERMISSIONS=[], USER_TYPES=[], AUTHENTICATED = Flase")
