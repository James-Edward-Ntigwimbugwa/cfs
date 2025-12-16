import traceback
import logging
from django.db.models import ForeignKey
from django.db import IntegrityError

from myapp_dto.shared_dto import ResponseObject

logger = logging.getLogger(__name__)
import enum

def resolve_enum_value(value):
    if isinstance(value, enum.Enum):
        return value.name
    return value


# --- Generic CRUD Helpers ---
def handle_create(model, input_data, update_fields, builder_method, unique_fields = ['name']):
    try:
        data_dict = {}
        for field in update_fields:
            value = getattr(input_data, field, None)
            # Extract enum value if applicable
            value = resolve_enum_value(value)

            # Resolve ForeignKey fields to model instances
            model_field = model._meta.get_field(field)
            if isinstance(model_field, ForeignKey) and value:
                related_model = model_field.remote_field.model
                value = related_model.objects.filter(unique_id=value).first()

            data_dict[field] = value

        try:
            # Try creating the new object
            query_set = model.objects.create(**data_dict)

        except IntegrityError as e:
            if "UNIQUE constraint" in str(e):
                # Try to get the existing object by unique fields (like `name`)
                  # Customize per model if needed
                lookup = {field: data_dict[field] for field in unique_fields if field in data_dict}
                query_set = model.objects.filter(**lookup).first()

                if query_set:
                    logger.info(f"{model.__name__}: Existing object returned due to UNIQUE constraint.")
                else:
                    logger.error(f"{model.__name__}: Duplicate error, but no object found for lookup: {lookup}")
                    return ResponseObject.get_response(id='5'), None
            else:
                raise  # re-raise if not a duplicate error
            
        data = builder_method(id=query_set.unique_id)
        return ResponseObject.get_response(id=1), data

    except Exception as e:
        logger.error(f"{model.__name__} Create Error: {e}")
        traceback.print_exc()
        return ResponseObject.get_response(id='5'), None
    

def handle_update_or_create(model, input_data, update_fields, builder_method, unique_lookup_fields = ['name']):
    try:
        data_dict = {}
        for field in update_fields:
            value = getattr(input_data, field, None)
            # Extract enum value if applicable
            value = resolve_enum_value(value)

            # Resolve foreign key fields to model instances
            model_field = model._meta.get_field(field)
            if isinstance(model_field, ForeignKey) and value:
                related_model = model_field.remote_field.model
                value = related_model.objects.filter(unique_id=value).first()

            data_dict[field] = value
            data_dict['is_active'] = True

        if getattr(input_data, "unique_id", None):
            # Update via unique_id
            query_set, _ = model.objects.update_or_create(
                unique_id=input_data.unique_id,
                defaults=data_dict
            )
        else:
            # Try to find using alternate unique fields (customize as needed)
            lookup = {field: data_dict[field] for field in unique_lookup_fields if field in data_dict}

            existing_obj = model.objects.filter(**lookup).first()
            if existing_obj:
                for key, value in data_dict.items():
                    setattr(existing_obj, key, value)
                existing_obj.save()
                query_set = existing_obj
            else:
                query_set = model.objects.create(**data_dict)

        data = builder_method(id=query_set.unique_id)
        return ResponseObject.get_response(id='1'), data
    except Exception as e:
        logger.error(f"{model.__name__} Create/Update Error: {e}")
        traceback.print_exc()
        return ResponseObject.get_response(id='5'), None


def handle_update(model, input_data, update_fields, builder_method):
    try:
        query_set = model.objects.filter(unique_id=input_data.unique_id, is_active=True).first()
        if not query_set:
            return ResponseObject.get_response(id="9"), None

        for field in update_fields:
            value = getattr(input_data, field, None)
            # Extract enum value if applicable
            value = resolve_enum_value(value)

            # Resolve ForeignKey fields to model instances
            model_field = model._meta.get_field(field)
            if isinstance(model_field, ForeignKey) and value:
                related_model = model_field.remote_field.model
                value = related_model.objects.filter(unique_id=value).first()

            setattr(query_set, field, value)

        query_set.save()
        data = builder_method(id=query_set.unique_id)
        return ResponseObject.get_response(id='1'), data
    except Exception as e:
        logger.error(f"{model.__name__} Update Error: {e}")
        traceback.print_exc()
        return ResponseObject.get_response(id='5'), None


def handle_delete(model, unique_id):
    try:
        query_set = model.objects.filter(unique_id=unique_id, is_active=True).first()
        if not query_set:
            return ResponseObject.get_response(id='9')
        query_set.is_active = False
        query_set.save()
        return ResponseObject.get_response(id='1')
    except Exception as e:
        logger.error(f"{model.__name__} Delete Error: {e}")
        traceback.print_exc()
        return ResponseObject.get_response(id='5')
    
    