from api.models import User


def check_login(token):
    """
    根据token验证用户
    """
    user = User.objects.filter(token=token).first()
    if user:
        return True
    return False
