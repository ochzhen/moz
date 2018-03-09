def is_user_admin(user):
    if user and user.is_authenticated and user.is_admin:
        return True
    return False
