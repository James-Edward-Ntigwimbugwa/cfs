from django.core.management.base import BaseCommand
from django.apps import apps
from django.db import models
import inspect

def get_field_definition(field):
    """
    Reconstructs the field definition string with parameters.
    """
    field_class = field.__class__.__name__
    args = []
    kwargs = []

    # Common keyword arguments
    if hasattr(field, 'max_length') and field.max_length:
        kwargs.append(f"max_length={field.max_length}")
    if field.null:
        kwargs.append("null=True")
    if field.blank:
        kwargs.append("blank=True")
    if field.unique:
        kwargs.append("unique=True")
    if field.primary_key:
        kwargs.append("primary_key=True")
    if field.auto_created and field.primary_key:
        return None  # skip auto-created PKs
    if field.default != models.fields.NOT_PROVIDED:
        default_value = field.default
        if callable(default_value):
            default_value = default_value.__name__
        kwargs.append(f"default={repr(default_value)}")
    if field.choices:
        kwargs.append(f"choices={repr(field.choices)}")

    field_def = f"    {field.name} = models.{field_class}("
    field_def += ", ".join(args + kwargs)
    field_def += ")"
    return field_def

class Command(BaseCommand):
    help = 'Lists all models into a single Python file with field definitions'

    def handle(self, *args, **options):
        output_file = 'new_models_dump.py'

        with open(output_file, 'w') as f:
            f.write("from django.db import models\n\n")

            for model in apps.get_models():
                model_name = model.__name__
                app_label = model._meta.app_label

                f.write(f"class {model_name}(models.Model):\n")

                fields = model._meta.fields
                body_written = False
                for field in fields:
                    line = get_field_definition(field)
                    if line:
                        f.write(line + "\n")
                        body_written = True

                if not body_written:
                    f.write("    pass\n")

                f.write("\n    class Meta:\n")
                f.write(f"        app_label = '{app_label}'\n\n\n")

        self.stdout.write(self.style.SUCCESS(f"All models written to {output_file}"))
