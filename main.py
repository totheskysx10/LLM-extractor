from ocr.processor import OCRProcessor
from ocr.service import OCRService


def main():
    images = [
        "test1.jpg"
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
