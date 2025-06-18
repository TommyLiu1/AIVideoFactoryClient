import requests
from api.user_session import UserSession

API_BASE_URL = "http://8.148.225.115:8090/api/v1"

def login(username, password):
    """
    用户登录API请求
    :param username: 用户名
    :param password: 密码
    :return: dict, 服务器返回的json数据
    """
    try:
        response = requests.post(
            f"{API_BASE_URL}/login",
            json={"username": username, "password": password},
            timeout=5
        )
        if response.status_code == 200:
            data = response.json()
            if data.get("status") == 200 and data.get("data", {}).get("token"):
                UserSession.set_user_id(data["data"]["user_id"])
                UserSession.set_token(data["data"]["token"])
                UserSession.set_secret(data["data"]["secret_key"])
                return {"success": True, "msg": data.get("message", "登录成功"), "data": data["data"]}
            else:
                return {"success": False, "msg": data.get("message", "用户名或密码错误！")}
        else:
            return {"success": False, "msg": f"服务器错误: {response.status_code}"}
    except Exception as e:
        return {"success": False, "msg": f"请求服务器失败: {e}"}

def logout():
    """
    用户登出API请求
    :return: dict, 服务器返回的json数据
    """
    global token
    try:
        response = requests.post(
            f"{API_BASE_URL}/logout",
            json={"user_id": UserSession.get_user_id(), "token": UserSession.get_token()},
            timeout=5
        )
        if response.status_code == 200:
            data = response.json()
            if data.get("status") == 200:
                UserSession.clear()
                return {"success": True, "msg": data.get("message", "登出成功")}
            else:
                return {"success": False, "msg": data.get("message", "登出失败")}
        else:
            return {"success": False, "msg": f"服务器错误: {response.status_code}"}
    except Exception as e:
        return {"success": False, "msg": f"请求服务器失败: {e}"}
