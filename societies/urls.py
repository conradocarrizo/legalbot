from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import SocietyViewSet

router = DefaultRouter()
router.register(r"societies", SocietyViewSet)

urlpatterns = [
    path("", include(router.urls)),
]
