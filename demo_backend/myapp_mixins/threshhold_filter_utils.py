from django.db.models import Q
from myapp_dto.enums import ThresholdOperator

class ThresholdFilterUtils:
    @staticmethod
    def build_threshold_filter(field_name: str, value, operator: str) -> Q:
        """
        Builds a Q filter based on threshold operator.

        :param field_name: the model field name (e.g. "capacity")
        :param value: the value to compare (can be int or list of two ints for BETWEEN)
        :param operator: one of the ThresholdOperator enum values
        :return: Q object to be used in filter chaining
        """
        if value is None or operator is None:
            return Q()
        
        filters = Q()
        if len(value) != 0:
            if operator == ThresholdOperator.GREATER_THAN:
                filters &= Q(**{f"{field_name}__gt": value[0]})
            elif operator == ThresholdOperator.LESS_THAN:
                filters &= Q(**{f"{field_name}__lt": value[0]})
            elif operator == ThresholdOperator.EQUALS_TO:
                filters &= Q(**{f"{field_name}": value[0]})
            elif operator == ThresholdOperator.BETWEEN:
                if len(value) == 2:
                    filters &= Q(**{f"{field_name}__gte": value[0], f"{field_name}__lte": value[1]})

        return filters  # fallback: no-op filter



