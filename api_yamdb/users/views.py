from django.core.mail import send_mail
from django.contrib.auth.tokens import default_token_generator
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import action, api_view
from rest_framework.filters import SearchFilter
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework_simplejwt.tokens import RefreshToken

from .models import User
from .permissions import IsAdmin
from .serializers import SignUpSerializer, TokenSerializer, UserSerializer


@api_view(['POST'])
def user_signup(request):
    serializer = SignUpSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
        serializer.save()
        user = serializer.instance
        confirmation_code = default_token_generator.make_token(user)
        send_mail(
            'Код подтверждения',
            f'{confirmation_code}',
            'from@example.com',
            [serializer.validated_data.get('email')],
            fail_silently=False,
        )
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def user_get_token(request):
    serializer = TokenSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    user = get_object_or_404(
        User,
        username=serializer.validated_data['username']
    )
    refresh = RefreshToken.for_user(user)
    return Response({'refresh': str(refresh)}, status=status.HTTP_200_OK)


class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    filter_backends = (SearchFilter, )
    search_fields = ('username', )
    lookup_field = 'username'
    permission_classes = (IsAdmin, )
    serializer_class = UserSerializer

    @action(
        methods=['GET', 'PATCH'],
        permission_classes=[IsAuthenticated],
        url_path='me',
        detail=False,
    )
    def user_profile(self, request):
        if request.method == 'PATCH':
            serializer = self.serializer_class(request.user, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            if request.user.role == 'user':
                serializer.validated_data['role'] = 'user'
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        serializer = self.serializer_class(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)
