import json
from typing import List, Dict


class OCRPrepare:
    def parse(self, ocr_json: str) -> List[Dict]:
        data = json.loads(ocr_json)
        words = []

        def walk(node):
            if isinstance(node, dict):
                if node.get("@type") == "RIL_WORD" and "#text" in node:
                    words.append({
                        "x": int(node["@X"]),
                        "y": int(node["@Y"]),
                        "w": int(node["@W"]),
                        "h": int(node["@H"]),
                        "text": node["#text"],
                    })
                for v in node.values():
                    walk(v)
            elif isinstance(node, list):
                for v in node:
                    walk(v)

        walk(data)
        return words

    def to_compact_text(self, words: List[Dict]) -> str:
        return "\n".join(
            f'X={w["x"]} Y={w["y"]} W={w["w"]} H={w["h"]} TEXT={w["text"]}'
            for w in words
        )