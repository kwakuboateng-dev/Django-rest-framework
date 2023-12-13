from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from .serializers import UserSerializer

from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated


@api_view(['POST'])
def login(request):
    username = request.data.get('username')
    password = request.data.get('password')
    if not username or not password:
        return Response({"error": "Both username and password are required"}, status=status.HTTP_400_BAD_REQUEST)
    user = get_object_or_404(User, username=username)
    if not user.check_password(password):
        return Response({"error": "Invalid username or password"}, status=status.HTTP_400_BAD_REQUEST)

    # User authentication successful, generate token and return response
    token, created = Token.objects.get_or_create(user=user)
    serializer = UserSerializer(instance=user)
    return Response({"token": token.key, "user": serializer.data})


@api_view(['POST'])
def signup(request):
    serializer = UserSerializer(data=request.data)
    if not serializer.is_valid():
        return Response({"error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    else:
        user_data = serializer.validated_data
        user = User.objects.create_user(**user_data)
        token, created = Token.objects.get_or_create(user=user)
        return Response({"token": token.key, "user": serializer.data})


@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def test_token(request):
    return Response("passed for {}".format(request.user.email))
