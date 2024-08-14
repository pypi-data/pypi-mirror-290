from ninja import NinjaAPI, errors
from ninja.security import APIKeyHeader

from pagesaver.authorization.models import APIToken
from pagesaver.record.api import router as record_router


class APIKey(APIKeyHeader):
    param_name = "Authorization"

    def authenticate(self, request, key):
        if token := APIToken.objects.filter(token=key).first():
            if token.verify():
                return token
        raise errors.AuthenticationError


api = NinjaAPI(auth=APIKey())

api.add_router("/record/", record_router)
