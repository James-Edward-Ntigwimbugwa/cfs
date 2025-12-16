from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.core.cache import cache
from dotenv import dotenv_values
config = dotenv_values('.env')


def get_any_unique_id(instance):
    """Returns the first attribute with 'unique_id' in the name and a non-empty value."""
    for field in dir(instance):
        if "unique_id" in field and not field.startswith("_"):
            value = getattr(instance, field, None)
            if value:
                return field, value
    return None, None


@receiver(post_save)
def cache_all_models_post_save(sender, instance, **kwargs):
    field_name, unique_value = get_any_unique_id(instance)
    if not unique_value:
        return

    model_name = sender._meta.label_lower  # e.g., "myapp.paper"
    key = f"{model_name}:{field_name}:{unique_value}"
    cache.set(key, instance, timeout=int(config.get("CACHE_TIMEOUT", 3600)))


@receiver(post_delete)
def cache_all_models_post_delete(sender, instance, **kwargs):
    field_name, unique_value = get_any_unique_id(instance)
    if not unique_value:
        return

    model_name = sender._meta.label_lower
    key = f"{model_name}:{field_name}:{unique_value}"
    cache.delete(key)
