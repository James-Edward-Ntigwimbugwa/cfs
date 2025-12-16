import inspect
import logging
from functools import wraps
import traceback
from django.db import transaction

from myapp_audit_logs.models import AuditLog
from myapp_dto.shared_dto import ResponseObject

logger = logging.getLogger(__name__)


def log_exceptions(func=None):
    """
    A decorator that wraps the passed in function and logs exceptions should one occur.

    The logger is configured to use the module's __name__ as the logger name.
    If an exception occurs within the wrapped function, the exception is logged
    with an error level and the exception is handled to `response code: 8 - Error occurred while processing request`.

    Args:
        func (function): The function to be wrapped by the decorator.

    Returns:
        function: The wrapped function that logs any exceptions.

    Example:
        @log_exceptions()
        def my_function():
            # Function implementation
    """

    def _get_info(args, kwargs, parameters):
        if 'info' in kwargs:
            return kwargs['info']
        info_index = parameters.index('info')
        if info_index < len(args):
            return args[info_index]
        raise ValueError("'info' parameter is required but not provided")

    def decorator(function):
        func_signature = inspect.signature(function)
        parameters = list(func_signature.parameters)

        if 'info' not in parameters:
            raise ValueError("The decorated function must have 'info' as one of its parameters.")

        @wraps(function)
        def wrapper(*args, **kwargs):
            info = _get_info(args, kwargs, parameters)
            try:
                with transaction.atomic():
                    return function(*args, **kwargs)
            except Exception as e:
                log = AuditLog.objects.create(errors={'message': f'Error in {function.__name__} for {info.field_name}: {type(e).__name__} - {str(e)}', 'traceback': traceback.format_exc()})
                setattr(info.context, "_partial_audit_log_id", log.unique_id)
                return info.return_type.graphene_type(response=ResponseObject.get_response(id=3))

        return wrapper

    if func is None:
        return decorator
    else:
        return decorator(func)

