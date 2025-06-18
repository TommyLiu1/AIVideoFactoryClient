import hashlib
import json
import time
import uuid

from api.user_session import UserSession


def get_signed_header(body_dict: dict|list|str) -> dict:
    """
    获取签名的请求头
    :return: dict, 包含签名的请求头
    """
    token = UserSession.get_token()
    secret = UserSession.get_secret()
    timestamp = str(int(time.time()))
    nonce = uuid.uuid4().hex
    body = json.dumps(body_dict, ensure_ascii=False) if isinstance(body_dict, (dict, list)) else body_dict
    sign_str = token + timestamp + nonce + body + secret
    signature = hashlib.sha256(sign_str.encode()).hexdigest()
    headers = {
        "X-Token": UserSession.get_token(),
        "X-Timestamp": timestamp,
        "X-Nonce": nonce,
        "X-Signature": signature,
        "Content-Type": "application/json"
    }
    return headers
