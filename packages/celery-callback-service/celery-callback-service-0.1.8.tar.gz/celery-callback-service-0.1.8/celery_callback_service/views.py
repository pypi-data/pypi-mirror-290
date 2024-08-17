import pydantic
from django_apis.views import apiview
from django_apis.helpers.auth import http_bearer_auth_protect

from .services import celery_callback_service
from .settings import CELERY_CALLBACK_SERVICE_APIKEYS

"""
{'success': True, 'msg': 'OK', 'code': 0, 'data': False}
"""


class CallbackPayload(pydantic.BaseModel):
    uid: str


@apiview(methods="post")
def callback_view(request, payload: CallbackPayload) -> bool:
    """回调任务调度接口。"""
    http_bearer_auth_protect(request, apikeys=CELERY_CALLBACK_SERVICE_APIKEYS)
    return celery_callback_service(payload.uid)
