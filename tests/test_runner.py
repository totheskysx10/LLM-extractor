from typing import Dict
from pathlib import Path

from config import Config
from llm.service import LLMService
from tests.test_data import TestData


class TestRunner:
    def __init__(self, config: Config):
        self.config = config
        self.llm = LLMService(config)
        self.test_data = TestData()

    def run(self) -> int:
        errors = 0

        for test in self.test_data.tests_definition():
            if not self.run_single_test(test):
                errors += 1

        print("\nQUALITY METRICS")
        print(self.llm.llm_metrics.mean())

        print("\nPERFORMANCE METRICS")
        print(self.llm.llm_metrics.performance_report())

        return 0 if errors == 0 else 1

    def run_single_test(self, test: Dict) -> bool:
        document_type = test["document_type"]
        field_name = test["field_name"]

        print(f"\nDOCUMENT: {document_type}, FIELD: {field_name}")
        print("LEARN MODE")

        learn_examples = []
        for ex in test["learn_examples"]:
            ocr_json = Path(ex["ocr_file"]).read_text(encoding="utf-8")
            value = Path(ex["value"]).read_text().strip() if Path(ex["value"]).is_file() else ex["value"]

            learn_examples.append({
                "value": value,
                "ocr_json": ocr_json,
            })

        self.llm.learn_field_location(
            document_type=document_type,
            field_name=field_name,
            examples=learn_examples,
            force=False,
        )

        print("APPLY MODE")

        success = True

        for target in test["apply_values"]:
            ocr_json = Path(target["ocr_file"]).read_text(encoding="utf-8")
            gt_value = Path(target["value"]).read_text().strip() if Path(target["value"]).is_file() else target["value"]

            pred_value = self.llm.extract_field(
                target_ocr_json=ocr_json,
                document_type=document_type,
                field_name=field_name,
            )

            print(f"OCR: {target['ocr_file']}")
            print("PRED:", pred_value)
            print("GT:", gt_value)

            self.llm.llm_metrics.add(pred=pred_value.lower(), gt=gt_value.lower())

            if not pred_value.strip():
                success = False

        return success