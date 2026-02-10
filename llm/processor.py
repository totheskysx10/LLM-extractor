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
        self.ocrp = OCRPrepare()

    def run_prompt(self, prompt: str, system: Optional[str] = None, metrics: bool = False) -> str:
        result = self.llm.generate(prompt=prompt, system=system)

        if metrics:
            self.llm_metrics.add_prompt_timing(
                result["prompt_time_ms"],
                result["prompt_tokens"],
            )
            self.llm_metrics.add_eval_timing(
                result["eval_time_ms"],
                result["eval_tokens"],
            )

        return result["text"]

    def _prepare_ocr(self, ocr_json: str) -> str:
        words = self.ocrp.parse(ocr_json)
        return self.ocrp.to_compact_text(words)

    def learn_field_location(self, document_type: str, field_name: str, examples: List[Dict[str, str]], force: bool = False) -> str:
        if not force:
            cached = self.db.get_learned_context(document_type, field_name)
            if cached:
                print("LEARN MODE SKIPPED — loaded from DB")
                return cached

        examples_block = ""

        for i, ex in enumerate(examples, 1):
            ocr_compact = self._prepare_ocr(ex["ocr_json"])

            examples_block += self.llm_prompt.EXAMPLES_PATTERN.format(
                index=i,
                example_value=ex["value"],
                example_ocr=ocr_compact,
            )

        prompt = self.llm_prompt.LEARN_PROMPT.format(
            field_name=field_name,
            examples_block=examples_block,
        )

        learned_context = self.run_prompt(
            prompt,
            system=self.llm_prompt.LEARN_SYSTEM,
        )

        self.db.save_learned_context(
            document_type=document_type,
            field_name=field_name,
            learned_context=learned_context,
        )

        return learned_context

    def extract_field(self, target_ocr_json: str, document_type: str, field_name: str) -> str:
        learned_context = self.db.get_learned_context(document_type, field_name)
        if not learned_context:
            raise KeyError("No learned context for this field!")

        ocr_compact = self._prepare_ocr(target_ocr_json)

        prompt = self.llm_prompt.APPLY_PROMPT.format(
            target_ocr=ocr_compact,
            learned_context=learned_context,
        )

        return self.run_prompt(
            prompt=prompt,
            system=LLMPrompt.APPLY_SYSTEM,
            metrics=True,
        )