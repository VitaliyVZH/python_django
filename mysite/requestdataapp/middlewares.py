from django.http import HttpRequest
from time import time

from requestdataapp.views import raise_error_frequent_call


def set_useragent_on_request_middleware(get_response):

    def middleware(request: HttpRequest):
        response = get_response(request)
        # print(request.META['TERM_SESSION_ID'])
        return response
    return middleware


class ThrottlingMiddleware:
    data = {}

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request: HttpRequest):
        # Ограничиваем скорость вызовов пользователем
        # Устанавливаем предел вызова в сек
        min_time_request = 5
        # Если в словаре нет искомого ключа, добавляем его, значением ключа является время вызова, далее делаем вызов
        # if not self.data.get(request.META['TERM_SESSION_ID']):
        #     self.data[request.META['TERM_SESSION_ID']] = round(time())
        #     response = self.get_response(request)
        #     return response
            # raise Exception
        # Если значение ключа (время предыдущего вызова в секундах) минус текущее время в секундах меньше
        # установленного ограничением -> возвращаем пустой ответ
        # if (round(time()) - self.data[request.META['TERM_SESSION_ID']]) < min_time_request:
        #     # raise Exception
        #     response = self.get_response(request)
        #     return response
        # Если все условия выполнены,
        # self.data[request.META['TERM_SESSION_ID']] = round(time())
        response = self.get_response(request)
        return response
