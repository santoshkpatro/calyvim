from django.contrib import admin
from django.urls import path, include, re_path
from rest_framework.routers import SimpleRouter

from calyvim.api.accounts.views import AccountViewSet
from calyvim.views import index

api_router = SimpleRouter(trailing_slash=False)

api_router.register("accounts", AccountViewSet, basename="account")

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include(api_router.urls)),
    re_path(r"^(?:.*)/?$", index, name="index"),  # Catch-all route
]
