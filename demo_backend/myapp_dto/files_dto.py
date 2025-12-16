import graphene

from myapp_dto.enums import FileVisibiltyEnum
from .shared_dto import ResponseObject


class FileInputObjects(graphene.InputObjectType):
    file_name = graphene.String()
    file_path = graphene.String()


class Base64FileInputObjects(graphene.InputObjectType):
    base64_string = graphene.String()
    file_name = graphene.String()
    file_visibility = FileVisibiltyEnum()


class FileObjects(graphene.ObjectType):
    file_path = graphene.String()
    file_name = graphene.String()
    base_64_string = graphene.String()


class FileResponseObject(graphene.ObjectType):
    response = graphene.Field(ResponseObject)
    data = graphene.Field(FileObjects)