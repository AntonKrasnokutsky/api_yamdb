from rest_framework import routers
from django.urls import include, path
from .views import (
    ReviewViewSet, TittleViewSet, GenreViewSet, CategoryViewSet
)
from users.views import UserViewSet, user_get_token, user_signup

router = routers.DefaultRouter()
router.register(r'titles/(?P<title_id>\d+)/reviews',
                ReviewViewSet,
                basename='reviews'
                )
router.register(r'titles', TittleViewSet, basename='Title')
router.register(r'genres', GenreViewSet, basename='Genre')
router.register(r'categories', CategoryViewSet, basename='Category')
router.register('users', UserViewSet, basename='users')

urlpatterns = [
    path('auth/token/', user_get_token, name='get_token'),
    path('auth/signup/', user_signup, name='signup'),
    path('v1/', include(router.urls)),
]
