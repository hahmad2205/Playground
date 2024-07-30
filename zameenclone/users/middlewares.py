from rest_framework import status
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response


class BlockedUserMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        if request.user.is_authenticated and request.user.is_blocked:
            response = Response(
                data={"detail": "User is blocked"},
                status=status.HTTP_401_UNAUTHORIZED
            )

        response.accepted_renderer = JSONRenderer()
        response.accepted_media_type = "application/json"
        response.renderer_context = {}
        response.render()

        return response
