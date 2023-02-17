from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import UserViewSet, SignUpView, GetTokenView


router = DefaultRouter()
router.register('users', UserViewSet, basename='users')

urlpatterns = [
    path('v1/auth/token/', GetTokenView.as_view(), name='get_token'),
    path('v1/auth/signup/', SignUpView.as_view(), name='signup'),
    path('v1/', include(router.urls)),
]
