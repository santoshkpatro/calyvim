from django.contrib import admin
from django.urls import path, include, re_path
from rest_framework.routers import SimpleRouter

from calyvim.views.index import AppView
from calyvim.views.home import IndexView
from calyvim.views.accounts import LoginView

from calyvim.api.accounts.views import AccountViewSet
from calyvim.api.teams.views import TeamViewSet
from calyvim.api.organizations.views import OrganizationViewSet

api_router = SimpleRouter(trailing_slash=False)

api_router.register("accounts", AccountViewSet, basename="account")
api_router.register("teams", TeamViewSet, basename="team")
api_router.register("organizations", OrganizationViewSet, basename="organization")

# fmt: off
urlpatterns = [
    path("admin/", admin.site.urls),
    path("accounts/login/", LoginView.as_view(), name="login"),
    path("", IndexView.as_view(), name="index"),
]

urlpatterns += [
    path("api/", include(api_router.urls)),
    re_path(r"^app/(?:.*)/?$", AppView.as_view(), name="app"),  # Catch all routes starting with app/
]
