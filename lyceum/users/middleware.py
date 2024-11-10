import users.models

__all__ = "ProxyUserMiddleware"


class ProxyUserMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.id:
            request.user = users.models.User.objects.get(
                id=request.user.id,
            )

        return self.get_response(request)
