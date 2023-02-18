from rest_framework import routers
from django.urls import include, path

from .views import (
    ReviewViewSet, TittleViewSet, GenreViewSet, CategoryViewSet,
    CommentViewSet,
)


router = routers.DefaultRouter()
router.register(
    r'titles/(?P<title_id>\d+)/reviews',
    ReviewViewSet,
    basename='reviews'
)
router.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet,
    basename='comments'
)
router.register('titles', TittleViewSet, basename='Title')
router.register('genres', GenreViewSet, basename='Genre')
router.register('categories', CategoryViewSet, basename='Category')

urlpatterns = [
    path('api/v1/', include(router.urls)),
]
