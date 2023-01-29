from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import UserViewSet, user_get_token, user_signup


router = DefaultRouter()
router.register('users', UserViewSet, basename='users')

urlpatterns = [
    path('v1/auth/token/', user_get_token, name='get_token'),
    path('v1/auth/signup/', user_signup, name='signup'),
    path('v1/', include(router.urls)),
]
