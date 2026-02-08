class LLMMetrics:
    def __init__(self):
        self.f1_scores = []
        self.accuracies = []

        self.prompt_time_ms = 0.0
        self.eval_time_ms = 0.0
        self.prompt_tokens = 0
        self.eval_tokens = 0

    @staticmethod
    def char_f1(pred: str, gt: str) -> float:
        if not pred and not gt:
            return 1.0
        if not pred or not gt:
            return 0.0

        tp = sum(1 for p, g in zip(pred, gt) if p == g)
        fp = max(0, len(pred) - tp)
        fn = max(0, len(gt) - tp)

        precision = tp / (tp + fp) if (tp + fp) > 0 else 0.0
        recall = tp / (tp + fn) if (tp + fn) > 0 else 0.0

        if precision + recall == 0:
            return 0.0

        return 2 * precision * recall / (precision + recall)

    @staticmethod
    def char_accuracy(pred: str, gt: str) -> float:
        if not pred and not gt:
            return 100.0
        if not pred or not gt:
            return 0.0

        matches = sum(1 for p, g in zip(pred, gt) if p == g)
        return matches / max(len(pred), len(gt)) * 100

    def add(self, pred: str, gt: str):
        self.f1_scores.append(self.char_f1(pred, gt))
        self.accuracies.append(self.char_accuracy(pred, gt))

    def add_prompt_timing(self, time_ms: float, tokens: int):
        self.prompt_time_ms += time_ms
        self.prompt_tokens += tokens

    def add_eval_timing(self, time_ms: float, tokens: int):
        self.eval_time_ms += time_ms
        self.eval_tokens += tokens

    @staticmethod
    def _speed_stats(time_ms: float, tokens: int) -> dict:
        if tokens == 0:
            return {
                "time_ms": round(time_ms, 2),
                "tokens": 0,
                "ms_per_token": 0.0,
                "tokens_per_second": 0.0
            }

        ms_per_token = time_ms / tokens
        tps = 1000 / ms_per_token

        return {
            "time_ms": round(time_ms, 2),
            "tokens": tokens,
            "ms_per_token": round(ms_per_token, 2),
            "tokens_per_second": round(tps, 2)
        }

    def mean(self) -> dict:
        samples = len(self.f1_scores)
        if samples == 0:
            return {
                "mean_char_f1": 0.0,
                "mean_char_accuracy_percent": 0.0,
                "success_rate_percent": 0.0,
                "samples": 0
            }

        return {
            "mean_char_f1": round(sum(self.f1_scores) / samples, 4),
            "mean_char_accuracy_percent": round(sum(self.accuracies) / samples, 2),
            "samples": samples
        }

    def performance_report(self) -> dict:
        total_time = self.prompt_time_ms + self.eval_time_ms
        total_tokens = self.prompt_tokens + self.eval_tokens

        return {
            "prompt_eval": self._speed_stats(
                self.prompt_time_ms, self.prompt_tokens
            ),
            "eval": self._speed_stats(
                self.eval_time_ms, self.eval_tokens
            ),
            "total": self._speed_stats(
                total_time, total_tokens
            )
        }