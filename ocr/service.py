import base64
import pathlib
from ocr.processor import OCRProcessor


class OCRService:
    def __init__(self, processor: OCRProcessor):
        self.processor = processor

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
        for idx, img in enumerate(images):
            print(f"\nобработка изображения {idx}")
            task_id = self.processor.create_task(self.encode_image(img))

            status = self.processor.wait_for_task(task_id)
            if status == "success":
                data = self.processor.fetch_result(task_id)
                decoded = [self.decode_result(elem) for elem in data.pages]

                for i, page in enumerate(decoded):
                    self.save_result(page, f"{img}.json")
            else:
                print(f"распознавание изображения {idx} завершилось ошибкой")
