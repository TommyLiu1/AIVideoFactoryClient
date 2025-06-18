class UserSession:
    """
    用户会话信息，保存token和secret，供API调用使用
    """
    _token = None
    _secret = None
    _user_id = None

    @classmethod
    def set_token(cls, token):
        cls._token = token

    @classmethod
    def get_token(cls):
        return cls._token

    @classmethod
    def set_secret(cls, secret):
        cls._secret = secret

    @classmethod
    def get_secret(cls):
        return cls._secret
    @classmethod
    def set_user_id(cls, user_id):
        cls._user_id = user_id
    @classmethod
    def get_user_id(cls):
        return cls._user_id

    @classmethod
    def clear(cls):
        cls._token = None
        cls._secret = None

