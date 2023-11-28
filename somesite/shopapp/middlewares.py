from django.http import HttpRequest


def set_useragent_on_request_middlewares(get_response):
    print('initial coll')

    def middleware(request: HttpRequest):
        print('before get_response')
        response = get_response(request)
        print('after get_response')
        return response

    return middleware
