from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST


class MyResponse:
    @staticmethod
    def success(data=None, message="", status_code=HTTP_200_OK, *args, **kwargs):
        return Response(
            data={"success": True, "data": data, "message": message, **kwargs}, status=status_code
        )

    @staticmethod
    def failure(message="", data=None, status_code=HTTP_400_BAD_REQUEST, *args, **kwargs):
        return Response(
            data={"success": False, "errors": data, "message": message, **kwargs},
            status=status_code,
        )
