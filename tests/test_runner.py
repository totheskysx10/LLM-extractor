from __future__ import annotations

from typing import Dict

from config import Config
from llm.processor import LLMProcessor
from tests.test_data import TestData


class TestRunner:
    def __init__(self, config: Config):
        self.config = config
        self.llm = LLMProcessor(config)
        self.test_data = TestData()

    def run(self) -> int:
        errors = 0

        for test in self.test_data.tests_definition():
            success = self.run_single_test(test)
            if not success:
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

        examples = self.llm.prepare_examples_from_files(test["learn_examples"])

        learned_context = self.llm.learn_field_location(
            document_type=document_type,
            field_name=field_name,
            examples=examples,
        )

        print("APPLY MODE")

        success = True

        for target in test["apply_examples"]:
            target_example = self.llm.prepare_examples_from_files([target])
            target_ocr = target_example[0]["example_ocr"]
            gt_value = target.get("value", "").strip()

            pred_value = self.llm.extract_field(
                target_ocr=target_ocr,
                learned_context=learned_context
            )

            print(f"OCR: {target['ocr_file']}")
            print("PRED:", pred_value)
            print("GT:", gt_value)

            self.llm.llm_metrics.add(pred=pred_value.lower(), gt=gt_value.lower())

            if not pred_value.strip():
                success = False

        return success