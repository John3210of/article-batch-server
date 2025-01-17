from article_app.services.utils.service_utils import create_response, exception_handler
from django.db import transaction

class BaseService:
    @staticmethod
    @exception_handler(method_name="get_object_by_id")
    def get_object_by_id(model, serializer_class, object_id):
        """
        단일 객체 조회
        """
        instance = model.objects.get(pk=object_id)
        serialized_data = serializer_class(instance).data
        return create_response(data=serialized_data)

    @staticmethod
    @exception_handler(method_name="get_all_objects")
    def get_all_objects(model, serializer_class):
        """
        모든 객체 조회
        """
        queryset = model.objects.all()
        serialized_data = serializer_class(queryset, many=True).data
        return create_response(data=serialized_data)

    @staticmethod
    @exception_handler(method_name="create_object")
    def create_object(serializer_class, data):
        """
        새 객체 생성
        """
        serializer = serializer_class(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return create_response(data=serializer.data, status_code=201)

    @staticmethod
    @exception_handler(method_name="update_object")
    def update_object(model, serializer_class, object_id, data):
        """
        특정 객체 업데이트
        """
        instance = model.objects.get(pk=object_id)
        serializer = serializer_class(instance, data=data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return create_response(data=serializer.data)

    @staticmethod
    @exception_handler(method_name="bulk_create_objects")
    def bulk_create_objects(serializer_class, data_list):
        """
        여러 객체 생성 (bulk_create)
        """
        validated_objects = []
        for data in data_list:
            serializer = serializer_class(data=data)
            serializer.is_valid(raise_exception=True)
            validated_objects.append(serializer)
        
        objects_to_create = [
            serializer.Meta.model(**serializer.validated_data) for serializer in validated_objects
        ]
        with transaction.atomic():
            serializer_class.Meta.model.objects.bulk_create(objects_to_create)

        return create_response(
            data=[serializer.data for serializer in validated_objects],
            status_code=201,
        )

