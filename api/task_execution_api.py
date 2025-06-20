import requests

from utils.api_helper import get_signed_header

API_BASE_URL = "http://8.148.225.115:8090/api/v1"

def get_user_tasks(user_id):
    """
    获取用户的任务列表
    :param user_id: 用户ID
    :return: dict, 服务器返回的json数据
    """
    try:
        headers = get_signed_header("")
        response = requests.get(
            f"{API_BASE_URL}/tasks",
            headers=headers,
            params={"user_id": user_id},
            timeout=10
        )
        if response.status_code == 200:
            data = response.json()
            if data.get("status") == 200:
                return {"success": True, "msg": data.get("message", "获取任务列表成功"), "data": data["data"]}
            elif data.get("status") == 1004:
                return {"success": True, "msg": "没有任务", "data": []}
            else:
                return {"success": False, "msg": data.get("message", "获取任务列表失败")}
        else:
            return {"success": False, "msg": f"服务器错误: {response.status_code}"}
    except Exception as e:
        return {"success": False, "msg": f"请求服务器失败: {e}"}

def create_task(user_id: int, task_setting: dict):
    """
    运行指定的任务
    """
    try:
        headers = get_signed_header(task_setting)
        response = requests.post(
            f"{API_BASE_URL}/tasks/create",
            headers=headers,
            json=task_setting,
            params={"user_id": user_id},
            timeout=10
        )
        if response.status_code == 200:
            data = response.json()
            if data.get("status") == 200:
                return {"success": True, "msg": data.get("message", "创建任务成功"), "data": data["data"]["job_id"]}
            else:
                return {"success": False, "msg": data.get("message", "创建任务失败")}
        else:
            return {"success": False, "msg": f"服务器错误: {response.status_code}"}
    except Exception as e:
        return {"success": False, "msg": f"请求服务器失败: {e}"}

def update_task(user_id: int, task_id: str, task_setting: dict):
    """
    更新指定的任务
    """
    try:
        headers = get_signed_header(task_setting)
        response = requests.post(
            f"{API_BASE_URL}/tasks/{task_id}/update",
            headers=headers,
            json=task_setting,
            params={"user_id": user_id},
            timeout=10
        )
        if response.status_code == 200:
            data = response.json()
            if data.get("status") == 200:
                return {"success": True, "msg": data.get("message", "更新任务成功"), "data": data["data"]["task_id"]}
            else:
                return {"success": False, "msg": data.get("message", "更新任务失败")}
        else:
            return {"success": False, "msg": f"服务器错误: {response.status_code}"}
    except Exception as e:
        return {"success": False, "msg": f"请求服务器失败: {e}"}
def batch_run_tasks(user_id: int, task_ids: list):
    """
    批量运行指定的任务
    """
    try:
        playload = {
            "task_ids": task_ids,
            "user_id": user_id
        }
        headers = get_signed_header(playload)
        response = requests.post(
            f"{API_BASE_URL}/tasks/batch_run",
            headers=headers,
            json=playload,
            params={"user_id": user_id},
            timeout=10
        )
        if response.status_code == 200:
            data = response.json()
            if data.get("status") == 200:
                return {"success": True, "msg": data.get("message", "批量任务运行成功"), "data": data["data"]["task_ids"]}
            else:
                return {"success": False, "msg": data.get("message", "批量任务运行失败")}
        else:
            return {"success": False, "msg": f"服务器错误: {response.status_code}"}
    except Exception as e:
        return {"success": False, "msg": f"请求服务器失败: {e}"}

def run_task(user_id: int, task_id: str):
    """
    运行指定的任务
    """
    try:
        headers = get_signed_header("")
        response = requests.get(
            f"{API_BASE_URL}/tasks/{task_id}/run",
            headers=headers,
            params={"user_id": user_id},
            timeout=10
        )
        if response.status_code == 200:
            data = response.json()
            if data.get("status") == 200:
                return {"success": True, "msg": data.get("message", "任务运行成功"), "data": data["data"]["job_id"]}
            else:
                return {"success": False, "msg": data.get("message", "任务运行失败")}
        else:
            return {"success": False, "msg": f"服务器错误: {response.status_code}"}
    except Exception as e:
        return {"success": False, "msg": f"请求服务器失败: {e}"}

def batch_run_task(user_id: int, task_ids: list):
    """
    运行指定的任务
    """
    try:
        play_load = {
            "task_ids": task_ids,
            "user_id": user_id
        }
        headers = get_signed_header(play_load)
        response = requests.post(
            f"{API_BASE_URL}/task/batch_run",
            headers=headers,
            json=play_load,
            params={"user_id": user_id},
            timeout=10
        )
        if response.status_code == 200:
            data = response.json()
            if data.get("status") == 200:
                return {"success": True, "msg": data.get("message", "批量任务运行成功"), "data": data["data"]["job_ids"]}
            else:
                return {"success": False, "msg": data.get("message", "批量任务运行失败")}
        else:
            return {"success": False, "msg": f"服务器错误: {response.status_code}"}
    except Exception as e:
        return {"success": False, "msg": f"请求服务器失败: {e}"}

def cancel_task(user_id: int, task_id: str):
    """
    取消指定的任务
    """
    try:
        headers = get_signed_header("")
        response = requests.get(
            f"{API_BASE_URL}/tasks/{task_id}/cancel",
            headers=headers,
            params={"user_id": user_id},
            timeout=10
        )
        if response.status_code == 200:
            data = response.json()
            if data.get("status") == 200:
                return {"success": True, "msg": data.get("message", "任务取消成功"), "data": data["data"]["task_id"]}
            else:
                return {"success": False, "msg": data.get("message", "任务取消失败")}
        else:
            return {"success": False, "msg": f"服务器错误: {response.status_code}"}
    except Exception as e:
        return {"success": False, "msg": f"请求服务器失败: {e}"}

def batch_cancel_task(user_id: int, task_ids: list):
    """
    批量取消指定的任务
    """
    try:
        playload = {
            "task_ids": task_ids,
            "user_id": user_id
        }
        headers = get_signed_header(playload)
        response = requests.post(
            f"{API_BASE_URL}/tasks/batch_cancel",
            headers=headers,
            json=playload,
            params={"user_id": user_id},
            timeout=10
        )
        if response.status_code == 200:
            data = response.json()
            if data.get("status") == 200:
                return {"success": True, "msg": data.get("message", "批量任务取消成功"), "data": data["data"]["task_ids"]}
            else:
                return {"success": False, "msg": data.get("message", "批量任务取消失败")}
        else:
            return {"success": False, "msg": f"服务器错误: {response.status_code}"}
    except Exception as e:
        return {"success": False, "msg": f"请求服务器失败: {e}"}

def delete_task(user_id: int, task_id: str):
    """
    删除指定的任务
    """
    try:
        headers = get_signed_header("")
        response = requests.delete(
            f"{API_BASE_URL}/tasks/{task_id}/delete",
            headers=headers,
            params={"user_id": user_id},
            timeout=10
        )
        if response.status_code == 200:
            data = response.json()
            if data.get("status") == 200:
                return {"success": True, "msg": data.get("message", "任务删除成功"), "data": data["data"]["task_id"]}
            else:
                return {"success": False, "msg": data.get("message", "任务删除失败")}
        else:
            return {"success": False, "msg": f"服务器错误: {response.status_code}"}
    except Exception as e:
        return {"success": False, "msg": f"请求服务器失败: {e}"}
def batch_delete_tasks(user_id: int, task_ids: list):
    """
    批量删除指定的任务
    """
    try:
        playload = {
            "task_ids": task_ids,
            "user_id": user_id
        }
        headers = get_signed_header(playload)
        response = requests.delete(
            f"{API_BASE_URL}/tasks/batch_delete",
            headers=headers,
            json=playload,
            params={"user_id": user_id},
            timeout=10
        )
        if response.status_code == 200:
            data = response.json()
            if data.get("status") == 200:
                return {"success": True, "msg": data.get("message", "批量任务删除成功"), "data": data["data"]}
            elif data.get("status") == 207:
                return {"success": True, "msg": "部分任务删除失败", "data":data["data"]}
            else:
                return {"success": False, "msg": data.get("message", "批量任务删除失败")}
        else:
            return {"success": False, "msg": f"服务器错误: {response.status_code}"}
    except Exception as e:
        return {"success": False, "msg": f"请求服务器失败: {e}"}

def get_task_detail(user_id: int, task_id: str):
    """
    获取指定任务的状态
    """
    try:
        headers = get_signed_header("")
        response = requests.get(
            f"{API_BASE_URL}/tasks/{task_id}/query",
            headers=headers,
            params={"user_id": user_id},
            timeout=10
        )
        if response.status_code == 200:
            data = response.json()
            if data.get("status") == 200:
                return {"success": True, "msg": data.get("message", "获取任务状态成功"), "data": data["data"]}
            else:
                return {"success": False, "msg": data.get("message", "获取任务状态失败")}
        else:
            return {"success": False, "msg": f"服务器错误: {response.status_code}"}
    except Exception as e:
        return {"success": False, "msg": f"请求服务器失败: {e}"}

def rerun_task(user_id: int, task_id: str):
    """
    重新运行指定的任务
    """
    try:
        headers = get_signed_header("")
        response = requests.get(
            f"{API_BASE_URL}/tasks/{task_id}/retry",
            headers=headers,
            params={"user_id": user_id},
            timeout=10
        )
        if response.status_code == 200:
            data = response.json()
            if data.get("status") == 200:
                return {"success": True, "msg": data.get("message", "任务重新运行成功"), "data": data["data"]["task_id"]}
            else:
                return {"success": False, "msg": data.get("message", "任务重新运行失败")}
        else:
            return {"success": False, "msg": f"服务器错误: {response.status_code}"}
    except Exception as e:
        return {"success": False, "msg": f"请求服务器失败: {e}"}


def download_task_artifact(user_id: int, task_id: str):
    """
    下载指定任务的artifact
    """
    try:
        headers = get_signed_header("")
        response = requests.get(
            f"{API_BASE_URL}/tasks/{task_id}/download",
            headers=headers,
            params={"user_id": user_id},
            timeout=10
        )
        if response.status_code == 200:
            data = response.json()
            if data.get("status") == 200:
                return {"success": True, "msg": data.get("message", "获取下载视频成功"), "data": data["data"]}
            else:
                return {"success": False, "msg": data.get("message", "获取下载视频失败")}
        else:
            return {"success": False, "msg": f"服务器错误: {response.status_code}"}
    except Exception as e:
        return {"success": False, "msg": f"请求服务器失败: {e}"}