from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.response import Response
from api.authentication import CustomTokenAuthentication
from rest_framework.authtoken.models import Token
class CustomObtainAuthToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        if CustomTokenAuthentication().expired(token):
            token.delete()
            token = Token.objects.create(user=user)
        return Response({'token': token.key})
custom_obtain_auth_token = CustomObtainAuthToken.as_view()