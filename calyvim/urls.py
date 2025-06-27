from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import SimpleRouter

from calyvim.api.accounts.views import AccountViewSet

api_router = SimpleRouter(trailing_slash=False)

api_router.register("accounts", AccountViewSet, basename="account")

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include(api_router.urls)),
]
