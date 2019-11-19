from utils.baseResponse import baseResponse


def jwt_response_payload_handler(token, user=None, request=None):
    """
    Returns the response data for both the login and refresh views.
    Override to return a custom response such as including the
    serialized representation of the User.

    Example:

    def jwt_response_payload_handler(token, user=None, request=None):
        return {
            'token': token,
            'user': UserSerializer(user, context={'request': request}).data
        }

    """
    return baseResponse(success="登录成功", data={
        'token': token,
        'name': user.name
    })


def jwt_response_payload_error_handler(serializer, request=None):
    return baseResponse(error="密码错误", data={
        'token': None,
        'name': None
    })
