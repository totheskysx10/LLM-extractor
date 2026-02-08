import os

from ocr.processor import OCRProcessor
from ocr.service import OCRService


def main():
    dataset_dir = "d1"

    images = [
        os.path.join(dataset_dir, f)
        for f in os.listdir(dataset_dir)
        if os.path.isfile(os.path.join(dataset_dir, f))
    ]

    ocr_processor = OCRProcessor()
    ocr_service = OCRService(ocr_processor)

    results = ocr_service.recognize_images(images)

    print("\nOCR Результат")
    for i, page in enumerate(results, start=1):
        print(f"\nстраница {i}")
        print(page)

if __name__ == "__main__":
    main()
