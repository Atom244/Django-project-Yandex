import re

from django.conf import settings


class ReverseWordMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.count = 0

    def __call__(self, request):
        if settings.ALLOW_REVERSE:
            response = self.get_response(request)

            self.count += 1

            if self.count == 10:
                self.count = 0
                response.content = self.reverse_russian_words(
                    response.content.decode("utf-8")
                )

            return response
        else:
            response = self.get_response(request)
            return response

    def reverse_russian_words(self, text):
        def reverse_res(res):
            return res.group(0)[::-1]

        return re.sub(r"[А-Яа-яЁё]+", reverse_res, text)
