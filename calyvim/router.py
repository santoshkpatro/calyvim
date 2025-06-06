# calyvim/router.py

import re


class Router:
    def __init__(self):
        self.routes = []

    def get(self, path, to):
        self._add_route("GET", path, to)

    def post(self, path, to):
        self._add_route("POST", path, to)

    def put(self, path, to):
        self._add_route("PUT", path, to)

    def delete(self, path, to):
        self._add_route("DELETE", path, to)

    def resource(self, name):
        """Auto-generate RESTful routes for a resource"""
        self.get(f"/{name}", to=f"{name}#index")
        self.get(f"/{name}/{{id}}", to=f"{name}#show")
        self.post(f"/{name}", to=f"{name}#create")
        self.put(f"/{name}/{{id}}", to=f"{name}#update")
        self.delete(f"/{name}/{{id}}", to=f"{name}#delete")

    def _add_route(self, method, path, to):
        controller_name, action = to.split("#")
        pattern = self._compile_path(path)
        self.routes.append(
            {
                "method": method,
                "path": path,
                "regex": pattern,
                "controller": controller_name,
                "action": action,
            }
        )

    def _compile_path(self, path):
        # Converts /users/{id} to regex pattern
        return re.compile("^" + re.sub(r"{(\w+)}", r"(?P<\1>[^/]+)", path) + "$")

    def resolve(self, path, method):
        format = "html"

        # Detect format via .json or .html suffix
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
                    "format": format,
                    "params": match.groupdict(),
                }

        return None
