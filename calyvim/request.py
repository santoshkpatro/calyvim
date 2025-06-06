# calyvim/request.py

from starlette.requests import Request as StarletteRequest


class Request(StarletteRequest):
    def __init__(self, scope, receive):
        super().__init__(scope, receive=receive)
        self.params = {}  # path params (e.g. {id})
        self.format = "html"  # default format
        self.context = {}  # optional per-request context

    def param(self, name, default=None):
        return self.params.get(name) or self.query_params.get(name, default)
