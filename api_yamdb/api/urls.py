from rest_framework import routers

from django.urls import include, path

from .views import ReviewViewSet

router = routers.DefaultRouter()

router.register(r'titles/(?P<title_id>\d+)/reviews',
                ReviewViewSet,
                basename='reviews'
                )


urlpatterns = [
    path('', include(router.urls)),
]
