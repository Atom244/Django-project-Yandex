import re

from django.conf import settings
from django.core.cache import cache

__all__ = ["ReverseWordMiddleware"]


class ReverseWordMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        if not cache.get("request_count"):
            cache.set("request_count", 0)

    def __call__(self, request):
        if settings.ALLOW_REVERSE:
            response = self.get_response(request)

            request_count = cache.incr("request_count")

            if request_count % 10 == 0:
                cache.set("request_count", 0)
                response.content = self.reverse_russian_words(
                    response.content.decode("utf-8"),
                )

            return response

        return self.get_response(request)

    def reverse_russian_words(self, text):
        def reverse_res(res):
            return res.group(0)[::-1]

        return re.sub(r"\b[а-яА-ЯёЁ]+\b", reverse_res, text)
