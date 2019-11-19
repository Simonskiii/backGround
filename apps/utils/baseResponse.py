from rest_framework import status


def baseResponse(success=None, error=None, data=None):
    base = {"code": status.HTTP_200_OK, "msg": "OK"}
    if success:
        base.update({"success": success})
    if error:
        base.update({"error": error})
    if data:
        base.update({"data": data})
    return base
