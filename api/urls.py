from django.urls import path
from django.conf.urls import include
from .views import HabitViewSet, DailyCheckViewSet, UserViewSet
from rest_framework import routers

router = routers.DefaultRouter()
router.register('habits', HabitViewSet)
router.register('dailychecks', DailyCheckViewSet)
router.register('users', UserViewSet)

urlpatterns = [
    path('', include(router.urls)),
]