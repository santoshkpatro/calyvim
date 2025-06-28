from django.views import View
from django.shortcuts import render
from django.conf import settings


class AppView(View):
    def get(self, request, *args, **kwargs):
        if settings.DEBUG:
            return render(request, "index_dev.html")

        return render(request, "index.html")
