from django.http import HttpRequest


def set_useragent_on_request_middlewares(get_response):
    def middleware(request: HttpRequest):
        response = get_response(request)
        return response

    return middleware
