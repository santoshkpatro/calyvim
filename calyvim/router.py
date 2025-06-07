import re
from contextlib import contextmanager


class Router:
    def __init__(self):
        self.routes = []
        self.prefix_stack = [""]  # for scoped nesting

    @contextmanager
    def scope(self, prefix: str):
        """Temporarily extend the route prefix for nested routes"""
        self.prefix_stack.append(self._join(self.prefix_stack[-1], prefix))
        try:
            yield
        finally:
            self.prefix_stack.pop()

    def _join(self, a, b):
        return (a.rstrip("/") + "/" + b.lstrip("/")).rstrip("/")

    def _full_path(self, path):
        return self._join(self.prefix_stack[-1], path)

    def get(self, path, to):
        self._add_route("GET", self._full_path(path), to)

    def post(self, path, to):
        self._add_route("POST", self._full_path(path), to)

    def put(self, path, to):
        self._add_route("PUT", self._full_path(path), to)

    def delete(self, path, to):
        self._add_route("DELETE", self._full_path(path), to)

    def resource(self, name):
        base = f"/{name}"
        self.get(base, to=f"{name}#index")
        self.get(f"{base}/{{id}}", to=f"{name}#show")
        self.post(base, to=f"{name}#create")
        self.put(f"{base}/{{id}}", to=f"{name}#update")
        self.delete(f"{base}/{{id}}", to=f"{name}#delete")

    def _add_route(self, method, path, to):
        controller, action = to.split("#")
        regex = self._compile_path(path)
        self.routes.append(
            {
                "method": method,
                "path": path,
                "regex": regex,
                "controller": controller,
                "action": action,
            }
        )

    def _compile_path(self, path):
        param_names = set()
        for name in re.findall(r"{(\w+)}", path):
            if name in param_names:
                raise ValueError(f"Duplicate parameter name: '{name}' in path '{path}'")
            param_names.add(name)
        return re.compile("^" + re.sub(r"{(\w+)}", r"(?P<\1>[^/]+)", path) + "$")

    def resolve(self, path, method):
        format = "html"
        if path.endswith(".json"):
            path = path[:-5]
            format = "json"
        elif path.endswith(".html"):
            path = path[:-5]
            format = "html"

        for route in self.routes:
            match = route["regex"].match(path)
            if match and route["method"] == method:
                return {
                    "controller": route["controller"],
                    "action": route["action"],
                    "params": match.groupdict(),
                    "format": format,
                }
        return None
