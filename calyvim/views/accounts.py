from django.views import View
from django.shortcuts import render


class LoginView(View):
    def get(self, request, *args, **kwargs):
        return render(request, "accounts/login.html")
