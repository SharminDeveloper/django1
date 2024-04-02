from rest_framework import authentication
from rest_framework.authtoken.models import Token
from datetime import datetime , timedelta , timezone
from django.utils.translation import gettext_lazy as _
from rest_framework import status
from rest_framework.exceptions import APIException
class TimePassed(APIException):
    status_code = status.HTTP_401_UNAUTHORIZED
    default_detail = "Time passed. The token is over 7 days old. We destroyed the token. You have to get a new token."
class CustomTokenAuthentication(authentication.TokenAuthentication):
    def expired(self,token):
        now = datetime.now(timezone.utc)
        seven_days = timedelta(days=7)
        created_time = token.created
        if created_time + seven_days <= now :
            return True
        return False
    def authenticate(self, request):
        result = super().authenticate(request)
        if result is None:
            try:
                raw_token = request.headers.get('Authentication')
                if raw_token is None:
                    raw_token = request.headers.get('Authorization')
            except:
                pass
            token = raw_token[6:-1] + raw_token[-1]
        else:
            token = str(result[1])       
        token_instance = Token.objects.get(key = token)
        if self.expired(token_instance):
            token_instance.delete()
            raise TimePassed
        return result
        