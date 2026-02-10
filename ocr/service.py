import base64
import uuid
from typing import Sequence

from ocr.processor import OCRProcessor
from s3.client import S3Client


class OCRService:
    def __init__(self):
        self.processor = OCRProcessor()
        self.s3 = S3Client()

    @staticmethod
    def encode_image(img_bytes: bytes) -> str:
        return base64.b64encode(img_bytes).decode("utf-8")

    @staticmethod
    def decode_result(data: str) -> bytes:
        return base64.b64decode(data)

    def recognize_images(self, images: list[bytes]) -> str:
        for idx, img in enumerate(images):
            print(f"\nобработка изображения {idx}")
            task_id = self.processor.create_task(self.encode_image(img))

            status = self.processor.wait_for_task(task_id)
            if status == "success":
                data = self.processor.fetch_result(task_id)
                decoded = [self.decode_result(elem) for elem in data.pages]

                for i, page in enumerate(decoded):
                    random_uuid = uuid.uuid4()
                    return self.s3.upload(page, f"{random_uuid}.json")
            else:
                print(f"распознавание изображения {idx} завершилось ошибкой")
