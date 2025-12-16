import inspect
import logging
from functools import wraps

from myapp_audit_logs.models import AuditLog
from myapp_dto.shared_dto import ResponseObject
import traceback

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

    def decorator(function):
        func_signature = inspect.signature(function)
        parameters = list(func_signature.parameters)

        if 'info' not in parameters:
            raise ValueError("The decorated function must have 'info' as one of its parameters.")

        @wraps(function)
        def wrapper(*args, **kwargs):
            if 'info' in kwargs:
                info = kwargs['info']
            else:
                info_index = parameters.index('info')
                if info_index < len(args):
                    info = args[info_index]
                else:
                    raise ValueError("'info' parameter is required but not provided")

            try:
                return function(*args, **kwargs)
            except Exception as e:
                # error = logger.error(f'Error in {function.__name__} for {info.field_name}: {type(e).__name__} - {str(e)}',
                #              exc_info=True)
                log = AuditLog.objects.create(
                    errors={'message': f'Error in {function.__name__} for {info.field_name}: {type(e).__name__} - {str(e)}', 'traceback': traceback.format_exc()},
                )
                setattr(info.context, "_partial_audit_log_id", log.unique_id)
                return info.return_type.graphene_type(response=ResponseObject.get_response(id=3))

        return wrapper

    if func is None:
        return decorator
    else:
        return decorator(func)
