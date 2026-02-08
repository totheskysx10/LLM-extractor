import time
from typing import Literal

import requests

from config import Config
from ocr.model import OCRResult

POLL_INTERVAL_S = 0.5
MAX_POLLS = 10

class OCRProcessor:
    def __init__(self):
        self.base_url = Config.OCR_BASE_URL
        self.headers = {"X-Api-Key": Config.OCR_API_KEY}

    def create_task(self, image_b64: str) -> str:
        resp = requests.post(
            f"{self.base_url}/tasks",
            headers=self.headers,
            json={"image": image_b64, "return_type": "json"},
            timeout=30,
        )
        resp.raise_for_status()
        data = resp.json()

        if data.get("code") != 0:
            raise RuntimeError(f"ошибка создания задачи: {data}")

        task_id = data.get("task_id")
        if not task_id:
            raise RuntimeError(f"не удалось получить task_id: {data}")

        print(f"создана задача: {task_id}")
        return task_id

    def wait_for_task(self, task_id: str, max_polls: int = MAX_POLLS, interval_s: float = POLL_INTERVAL_S) -> Literal["success", "error"]:
        for _ in range(max_polls):
            status_resp = requests.get(
                f"{self.base_url}/tasks/{task_id}/status",
                headers=self.headers,
                timeout=10,
            )
            status_resp.raise_for_status()
            status = status_resp.json().get("task_status", "unknown")
            print(f"статус: {status}")

            if status in ("pending"):
                time.sleep(interval_s)
            elif status in ("success", "error"):
                return status
            else:
                raise RuntimeError(f"{status}")
        raise TimeoutError("Лимит ожидания статуса исчерпан")

    def fetch_result(self, task_id: str) -> OCRResult:
        resp = requests.get(
            f"{self.base_url}/tasks/{task_id}/result",
            headers=self.headers,
            timeout=30,
        )
        resp.raise_for_status()

        result_json = resp.json()
        pages = result_json.get("recognition_result", [])
        return OCRResult(pages=pages)