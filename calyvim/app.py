import importlib
from starlette.responses import PlainTextResponse, JSONResponse
from starlette.templating import Jinja2Templates
from starlette.requests import Request as StarletteRequest
from urls import router
from calyvim.request import Request  # your custom request wrapper

templates = Jinja2Templates(directory="app/views")


async def app(scope, receive, send):
    assert scope["type"] == "http"
    method = scope["method"]
    path = scope["path"]

    match = router.resolve(path, method)
    if not match:
        response = PlainTextResponse("404 Not Found", status_code=404)
        await response(scope, receive, send)
        return

    try:
        module_path = f"app.controllers.{match['controller']}_controller"
        module = importlib.import_module(module_path)

        class_name = match["controller"].capitalize() + "Controller"
        controller_class = getattr(module, class_name)
        controller_instance = controller_class()

        request = Request(scope, receive)
        request.params = match["params"]
        request.format = match["format"]

        action_method = getattr(controller_instance, match["action"])
        result = await action_method(request)

        if result is None and request.format == "html":
            template_path = f"{match['controller']}/{match['action']}.html"
            starlette_request = StarletteRequest(scope, receive=receive)
            context = {"request": starlette_request, **controller_instance.context}
            response = templates.TemplateResponse(template_path, context)
        elif result is None:
            response = JSONResponse({"error": "No content"}, status_code=204)
        else:
            response = result

        await response(scope, receive, send)

    except Exception as e:
        response = JSONResponse({"error": str(e)}, status_code=500)
        await response(scope, receive, send)
