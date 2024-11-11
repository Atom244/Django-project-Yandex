import django.utils.deprecation

import users.models


__all__ = []


class ProxyUserMiddleware(django.utils.deprecation.MiddlewareMixin):
    def __init__(self, get_response):
        self.get_response = get_response
        self.model = users.models.ProxyUser

    def __call__(self, request):
        try:
            proxy_user = users.models.ProxyUser.objects.get(
                pk=request.user.pk,
            )
            request.user = proxy_user
        except users.models.ProxyUser.DoesNotExist:
            pass

        return self.get_response(request)
