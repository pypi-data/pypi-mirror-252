from rest_framework.request import Request
from rest_framework.views import APIView

from energy_base.models import JWTUser


class BaseRequest(Request):

    @property
    def user(self) -> JWTUser:
        return super(BaseRequest, self).user()


class BaseAPIView(APIView):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.request: BaseRequest | None = None
