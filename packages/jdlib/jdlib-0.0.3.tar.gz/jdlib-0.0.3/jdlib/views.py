from django.views.generic import View as BaseView

from jdlib.exceptions import MethodNotAllowed


class View(BaseView):
    def get(self, request, *args, **kwargs):
        return MethodNotAllowed('GET').get_response()

    def post(self, request, *args, **kwargs):
        return MethodNotAllowed('POST').get_response()

    def put(self, request, *args, **kwargs):
        return MethodNotAllowed('PUT').get_response()

    def patch(self, request, *args, **kwargs):
        return MethodNotAllowed('PATCH').get_response()

    def delete(self, request, *args, **kwargs):
        return MethodNotAllowed('DELETE').get_response()

    def head(self, request, *args, **kwargs):
        return MethodNotAllowed('HEAD').get_response()

    def options(self, request, *args, **kwargs):
        return MethodNotAllowed('OPTIONS').get_response()

    def trace(self, request, *args, **kwargs):
        return MethodNotAllowed('TRACE').get_response()
