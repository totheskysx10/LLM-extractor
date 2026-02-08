from pathlib import Path
from typing import Optional, List, Dict

from config import Config
from db.manager import DatabaseManager
from llm.client import LLMClient
from llm.metrics import LLMMetrics
from llm.prompt import LLMPrompt
from ocr.prepare import OCRPrepare


class LLMProcessor:
    def __init__(self, config: Config):
        self.config = config
        self.db = DatabaseManager(config)

        self.llm = LLMClient(config)
        self.llm_prompt = LLMPrompt()
        self.llm_metrics = LLMMetrics()

    def run_one(self, prompt: str, system: Optional[str] = None, metrics: bool = False) -> str:
        result = self.llm.generate(prompt=prompt, system=system)

        if metrics is True:
            self.llm_metrics.add_prompt_timing(
                result["prompt_time_ms"],
                result["prompt_tokens"],
            )
            self.llm_metrics.add_eval_timing(
                result["eval_time_ms"],
                result["eval_tokens"],
            )

        return result["text"]

    def learn_field_location(self, document_type: str, field_name: str, examples: List[Dict[str, str]]) -> str:
        cached = self.db.get_learned_context(
            document_type=document_type,
            field_name=field_name,
        )

        if cached:
            print("LEARN MODE SKIPPED — loaded from DB")
            return cached

        examples_block = ""

        for i, ex in enumerate(examples, start=1):
            examples_block += f"""
        ПРИМЕР {i}
        
        ТЕКСТ ЗНАЧЕНИЯ:
        <<<
        {ex["example_value"]}
        >>>
        
        OCR-ДОКУМЕНТ (СТРОКИ):
        <<<
        {ex["example_ocr"]}
        >>>
        """

        prompt = self.llm_prompt.LEARN_PROMPT.format(
            field_name=field_name,
            examples_block=examples_block,
        )

        learned_context = self.run_one(
            prompt,
            system=self.llm_prompt.LEARN_SYSTEM,
        )

        self.db.save_learned_context(
            document_type=document_type,
            field_name=field_name,
            learned_context=learned_context,
        )

        return learned_context

    def extract_field(self, target_ocr: str, learned_context: str) -> str:
        prompt = self.llm_prompt.APPLY_PROMPT.format(
            target_ocr=target_ocr,
            learned_context=learned_context,
        )
        return self.run_one(prompt=prompt,
                            system=LLMPrompt.APPLY_SYSTEM,
                            metrics=True)

    def prepare_examples_from_files(self, example_files: List[Dict[str, str]]) -> List[Dict[str, str]]:
        ocrp = OCRPrepare()
        examples = []

        for ex in example_files:
            ocr_file = Path(ex["ocr_file"])
            ocr_text = ocr_file.read_text(encoding="utf-8")
            lines = ocrp.prepare(ocr_text)
            ocr_compact = ocrp.to_compact_text(lines)

            value = ex["value"]
            value_path = Path(value)

            if value_path.is_file():
                value = value_path.read_text(encoding="utf-8").strip()

            examples.append({
                "example_value": value,
                "example_ocr": ocr_compact,
            })

        return examples