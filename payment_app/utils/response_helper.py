from utils import messages


def create_response(status, message, payload):
    return {
               "status": status,
               "message": message,
               "payload": payload
           }, status


def method_not_allowed():
    return create_response(405, messages.METHOD_NOT_ALLOWED, {})


def success(message, data=None):
    return create_response(200, message, data)


def server_error():
    return create_response(500, messages.SERVER_ERROR, {})


def parameter_missing(parameter):
    return create_response(400, messages.PARAMETER_MISSING.format(parameter), {})


def parameter_invalid(message):
    return create_response(400, message, {})
