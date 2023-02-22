from rest_framework.exceptions import APIException


class RestaurantNotFound(APIException):
    status_code = 404
    default_detail = "The requested restaurant does not exist"
