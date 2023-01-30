from rest_framework import routers

<<<<<<< HEAD
from django.urls import include, path

from .views import ReviewViewSet

router = routers.DefaultRouter()

router.register(r'titles/(?P<title_id>\d+)/reviews',
                ReviewViewSet,
                basename='reviews'
                )
=======

from django.urls import include, path

from .views import (
    TittleViewSet, GenreViewSet, CategoryViewSet
)

router = routers.DefaultRouter()
router.register(r'titles', TittleViewSet, basename='Title')
router.register(r'genres', GenreViewSet, basename='Genre')
router.register(r'categories', CategoryViewSet, basename='Category')
>>>>>>> d92db10 (endpoints updated)


urlpatterns = [
    path('', include(router.urls)),
]
