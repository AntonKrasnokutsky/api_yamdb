from rest_framework import routers
from django.urls import include, path
from .views import (
    ReviewViewSet, TittleViewSet, GenreViewSet, CategoryViewSet,
    CommentViewSet,
)


router = routers.DefaultRouter()
router.register(r'titles/(?P<title_id>\d+)/reviews',
                ReviewViewSet,
                basename='reviews'
                )
router.register(r'titles/(?P<title_id>\d+)/reviews'
                r'/(?P<review_id>\d+)/comments',
                CommentViewSet,
                basename='comments'
                )
router.register(r'titles', TittleViewSet, basename='Title')
router.register(r'genres', GenreViewSet, basename='Genre')
router.register(r'categories', CategoryViewSet, basename='Category')

urlpatterns = [
    path('api/v1/', include(router.urls)),
]
