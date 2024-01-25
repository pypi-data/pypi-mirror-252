from jdlib import status
from jdlib.response import Response


class APIException(Exception):
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    default_message = 'A server error occurred.'

    def __init__(self, message=None):
        if message is None:
            self.message = self.default_message

    def __str__(self):
        return self.message
    
    def get_response(self):
        return Response({
            'status': self.status_code,
            'message': self.message,
        }, status=self.status_code)
    

class MethodNotAllowed(APIException):
    status_code = status.HTTP_405_METHOD_NOT_ALLOWED
    default_message = 'Method {} not allowed.'

    def __init__(self, method, message=None):
        if message is None:
            message = self.default_message.format(method)
        super().__init__(message)
