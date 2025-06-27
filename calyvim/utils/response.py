import re
from rest_framework.parsers import JSONParser
from rest_framework.renderers import JSONRenderer


def api_response_template():
    return dict(
        detail=None,
        result=None,
        error=None,
    )


def camel_to_snake(name):
    s1 = re.sub(r"(.)([A-Z][a-z]+)", r"\1_\2", name)
    return re.sub(r"([a-z0-9])([A-Z])", r"\1_\2", s1).lower()


def snake_to_camel(snake_str):
    components = snake_str.split("_")
    return components[0] + "".join(x.title() for x in components[1:])


def convert_keys(obj, convert_func):
    if isinstance(obj, dict):
        return {convert_func(k): convert_keys(v, convert_func) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [convert_keys(i, convert_func) for i in obj]
    return obj


class CamelCaseJSONParser(JSONParser):
    """
    Converts incoming camelCase keys to snake_case only if media_type is JSON.
    """

    def parse(self, stream, media_type=None, parser_context=None):
        data = super().parse(
            stream, media_type=media_type, parser_context=parser_context
        )

        if media_type == "application/json":
            return convert_keys(data, camel_to_snake)
        return data


class CamelCaseJSONRenderer(JSONRenderer):
    """
    Converts outgoing snake_case keys to camelCase only if media_type is JSON.
    """

    def render(self, data, accepted_media_type=None, renderer_context=None):
        if accepted_media_type == "application/json":
            data = convert_keys(data, snake_to_camel)
        return super().render(data, accepted_media_type, renderer_context)
