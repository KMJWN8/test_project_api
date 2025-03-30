from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (
    DepartmentViewSet,
    DivisionViewSet,
    EmployeeViewSet,
    ServiceViewSet,
    TeamViewSet,
)

router = DefaultRouter()
router.register(r"services", ServiceViewSet, basename="service")
router.register(r"departments", DepartmentViewSet, basename="department")
router.register(r"divisions", DivisionViewSet, basename="division")
router.register(r"teams", TeamViewSet, basename="team")
router.register(r"employees", EmployeeViewSet, basename="employee")

urlpatterns = [
    path("api/", include(router.urls)),
]
