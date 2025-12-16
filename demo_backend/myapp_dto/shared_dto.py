import json
import graphene
import logging
from pathlib import Path
from django.conf import settings

logger = logging.getLogger(__name__)


class PageObject(graphene.ObjectType):
    number = graphene.Int()
    has_next_page = graphene.Boolean()
    has_previous_page = graphene.Boolean()
    next_page_number = graphene.Int()
    previous_page_number = graphene.Int()
    number_of_pages = graphene.Int()
    total_items = graphene.Int()
    pages = graphene.List(graphene.Int)

    @staticmethod
    def get_page(page_object):
        previous_page_number = 0
        next_page_number = 0

        if page_object.number > 1:
            previous_page_number = page_object.previous_page_number()

        try:
            next_page_number = page_object.next_page_number()
        except Exception as e:
            logger.error(f'Error getting next page number for page {page_object.number}: {e}')
            next_page_number + page_object.number

        return PageObject(
            number=page_object.number,
            has_next_page=page_object.has_next(),
            has_previous_page=page_object.has_previous(),
            next_page_number=next_page_number,
            previous_page_number=previous_page_number,
            number_of_pages=page_object.paginator.num_pages,
            total_items=page_object.paginator.count,
            pages=page_object.paginator.page_range,
        )


class ResponseObject(graphene.ObjectType):
    id = graphene.String()
    status = graphene.Boolean()
    code = graphene.Int()
    message = graphene.String()

    @staticmethod
    def __read_code_file(code_id: int):
        # Use absolute path based on Django's BASE_DIR
        responses_file = Path(settings.BASE_DIR) / 'myapp_assets' / 'responses.json'
        with open(responses_file, 'r') as file:
            file_codes = file.read()
            response_codes = json.loads(file_codes)
            response_code = next(code for code in response_codes if int(code['id']) == int(code_id))
            return response_code

    @staticmethod
    def get_response(id: str, message: str | None = None):
        try:
            response_code = ResponseObject.__read_code_file(id)
            return ResponseObject(
                response_code['id'],
                response_code['status'],
                response_code['code'],
                message=message if message else response_code['message'],
            )
        except Exception as e:
            logger.error(f'Error getting response code: {e}')
            return ResponseObject()


