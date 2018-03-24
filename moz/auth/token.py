from itsdangerous import URLSafeTimedSerializer


def generate_token(email):
    from moz import app
    serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])
    return serializer.dumps(email, salt=app.config['SECURITY_PASSWORD_SALT'])


def confirm_token(token, expiration=3600):
    from moz import app
    serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])
    
    return serializer.loads(
        token,
        salt=app.config['SECURITY_PASSWORD_SALT'],
        max_age=expiration
    )
