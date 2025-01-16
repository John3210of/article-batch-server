from rest_framework.response import Response
import logging
from functools import wraps
from rest_framework.exceptions import ValidationError

logger = logging.getLogger(__name__)

def handle_unexpected_error(error, method_name):
    """
    알 수 없는 에러에 대해 응답합니다.
    예외를 로깅하고 표준화된 에러 응답을 반환합니다.
    """
    logger.exception(f"Unexpected error in {method_name}: {error}")
    return create_response(
        success=False,
        error_code="ERR500",
        data={"message": "Unknown error occurred"},
        status_code=500
    )

def create_response(success: bool = True, error_code: str = None, data: dict = None, status_code: int = 200):
    """
    공통 응답 형식에 대한 정의입니다.
    정의된 에러에 대한 응답입니다.
    Args:
        success (bool): 요청 성공 여부
        error_code (str): 에러 코드
        data (dict): 응답 데이터
        status_code (int): HTTP 상태 코드
    Returns:
        Response: Django Rest Framework Response 객체
    """
    response_data = {
        "success": success,
        "errorCode": error_code,
        "data": data
    }
    return Response(response_data, status=status_code)

def exception_handler(method_name=""):
    """
    공통 예외 처리를 담당하는 데코레이터.
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except args[0].DoesNotExist:
                return create_response(
                    success=False,
                    error_code="ERR404",
                    data={"message": f"{args[0].__name__} not found"},
                    status_code=404
                )
            except ValidationError as e:
                return create_response(
                    success=False,
                    error_code="ERR400",
                    data=e.detail,
                    status_code=400
                )
            except Exception as e:
                logger.exception(f"Unexpected error in {method_name}: {e}")
                return create_response(
                    success=False,
                    error_code="ERR500",
                    data={"message": "Unknown error occurred"},
                    status_code=500
                )
        return wrapper
    return decorator
