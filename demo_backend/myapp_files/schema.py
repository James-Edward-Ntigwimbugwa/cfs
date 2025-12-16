import logging
import traceback
import graphene
from  graphene import ObjectType
from myapp_utils.decorators.permission import login_required
from myapp_dto.files_dto import *
from myapp_utils.file_utils import UploadFile
from myapp_utils.cache.decorator import cached_resolver

logger = logging.getLogger(__name__)

class Query(ObjectType):
    get_base64_file = graphene.Field(FileResponseObject, file_path=graphene.String(required=True))

    @staticmethod
    @login_required()
    @cached_resolver(timeout=60 * 60 * 24, vary_headers=[])
    def resolve_get_base64_file(self, info, file_path=None, **kwargs):
        try:
            base_64 = UploadFile.base64_decrypted_file(file_path)
            data = FileObjects(file_path=file_path, file_name=file_path, base_64_string=base_64)
            return info.return_type.graphene_type(ResponseObject.get_response(id=1), data=data)
        except FileNotFoundError as e:
            logger.error(f'[AttachmentFiles] Get Base64 file :: {e}')
            traceback.print_exc()
            return info.return_type.graphene_type(ResponseObject.get_response(id=9, message='File not found'), data=None)
        except Exception as e:
            logger.error(f'[AttachmentFiles] Get Base64 file :: {e}')
            traceback.print_exc()
            return info.return_type.graphene_type(ResponseObject.get_response(id=3), data=None)
