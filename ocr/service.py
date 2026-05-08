import base64
import pathlib
import uuid
from typing import Sequence

from ocr.processor import OCRProcessor
from s3.client import S3Client


class OCRService:
    def __init__(self):
        self.processor = OCRProcessor()
        self.s3 = S3Client()

    @staticmethod
    def encode_image(path: str | pathlib.Path) -> str:
        with open(path, "rb") as f:
            return base64.b64encode(f.read()).decode()

    @staticmethod
    def decode_result(data: str) -> bytes:
        return base64.b64decode(data)

    @staticmethod
    def save_result(data: bytes, path: str | pathlib.Path) -> None:
        with open(path, "wb") as f:
            f.write(data)

    def recognize_images(self, images: list[str]):
        all_results = []  # Собираем все результаты

        for idx, img in enumerate(images):
            print(f"\nобработка изображения {idx}")
            task_id = self.processor.create_task(self.encode_image(img))

            status = self.processor.wait_for_task(task_id)
            if status == "success":
                data = self.processor.fetch_result(task_id)
                decoded = [self.decode_result(elem) for elem in data.pages]

                all_results.extend(decoded)

                for i, page in enumerate(decoded):
                    self.save_result(page, f"{img}.json")
            else:
                print(f"распознавание изображения {idx} завершилось ошибкой")

        return all_results
