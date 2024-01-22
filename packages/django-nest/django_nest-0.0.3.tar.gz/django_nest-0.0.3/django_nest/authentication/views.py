from django.contrib.auth import authenticate
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
from .models import JWTToken
from .serializers import JWTTokenSerializer
from drf_yasg.utils import swagger_auto_schema

class JWTTokenView(APIView):

    def refresh_token(self, user):
        refresh = RefreshToken.for_user(user)
        JWTToken.objects.update_or_create(user=user, defaults={'token': refresh.access_token})
        return refresh.access_token

    @swagger_auto_schema(request_body=JWTTokenSerializer)
    def post(self, request):
        serializer = JWTTokenSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=400)
        user = authenticate(username=request.data.get("username"), password=request.data.get("password"))
        if user is not None:
            token = JWTToken.objects.filter(user=user).first()
            if token is None:
                refresh = self.refresh_token(user)
                return Response({'token': f'Bearer {str(refresh)}'})
            try:
                AccessToken(token.token)
            except:
                refresh = self.refresh_token(user)
                return Response({'token': f'Bearer {str(refresh)}'})
            return Response({'token': f'Bearer {token.token}'})
        else:
            return Response({'error': 'Usuário ou senha inválidos'}, status=401)
