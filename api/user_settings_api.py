import requests

from utils.api_helper import get_signed_header

API_BASE_URL = "http://8.148.225.115:8090/api/v1"

def get_user_settings(user_id: int):
    """
    获取用户设置
    :param user_id: 用户ID
    :return: dict, 用户设置数据
    """
    try:
        headers = get_signed_header("")
        response = requests.get(f"{API_BASE_URL}/settings/{user_id}/get", headers=headers, timeout=10)
        if response.status_code == 200:
            data = response.json()
            if data.get("status") == 200:
                return {"success": True, "data": data.get("data", {})}
            else:
                return {"success": False, "msg": data.get("message", "获取设置失败")}
        else:
            return {"success": False, "msg": f"服务器错误: {response.status_code}"}
    except Exception as e:
        return {"success": False, "msg": f"请求服务器失败: {e}"}


def create_or_update_user_settings(user_id: int, settings: dict):
    """
    创建用户设置
    :param user_id: 用户ID
    :param settings: 用户设置数据
    :return: dict, 服务器返回的json数据
    """
    try:
        headers = get_signed_header(settings)
        response = requests.post(f"{API_BASE_URL}/settings/{user_id}/create_or_update", json=settings,
                                 headers=headers, timeout=10)
        if response.status_code == 200:
            data = response.json()
            if data.get("status") == 200:
                return {"success": True, "msg": data.get("message", "设置更新成功"), "data": data.get("data")}
            else:
                return {"success": False, "msg": data.get("message", "设置更新失败")}
        else:
            return {"success": False, "msg": f"服务器错误: {response.status_code}"}
    except Exception as e:
        return {"success": False, "msg": f"请求服务器失败: {e}"}

