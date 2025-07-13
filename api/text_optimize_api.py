import requests

from utils.api_helper import get_signed_header

API_BASE_URL = "http://8.148.225.115:8090/api/v1"

def get_optimize_text(user_prompt: str):
    """
    获取优化后的文本提示
    :param user_prompt:
    :return:
    """
    try:
        headers = get_signed_header("")
        response = requests.get(
            f"{API_BASE_URL}/text/optimize",
            params={"user_prompt": user_prompt},
            headers=headers,
            timeout=30
        )
        if response.status_code == 200:
            data = response.json()
            if data.get("status") == 200:
                return {"success": True, "msg": "优化成功", "data": data.get("data", {})}
            else:
                return {"success": False, "msg": data.get("message", "优化失败")}
        else:
            return {"success": False, "msg": f"服务器错误: {response.status_code}"}
    except Exception as e:
        return {"success": False, "msg": f"请求服务器失败: {e}"}

def send_message(user_prompt: str):
    """
       获取优化后的文本提示
       :param user_prompt:
       :return:
       """
    try:
        headers = get_signed_header("")
        response = requests.get(
            f"{API_BASE_URL}/text/send",
            params={"user_prompt": user_prompt},
            headers=headers,
            timeout=120
        )
        if response.status_code == 200:
            data = response.json()
            if data.get("status") == 200:
                return {"success": True, "msg": "发送消息成功", "data": data.get("data", {})}
            else:
                return {"success": False, "msg": data.get("message", "发送消息失败")}
        else:
            return {"success": False, "msg": f"服务器错误: {response.status_code}"}
    except Exception as e:
        return {"success": False, "msg": f"请求服务器失败: {e}"}