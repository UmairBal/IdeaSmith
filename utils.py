"""
utils.py — Shared helpers for IdeaSmith.
"""

import re
import json


def extract_json(raw: str):
    """
    Robustly extract JSON from a model response that may contain:
    - Bare JSON
    - ```json ... ``` fences
    - ``` ... ``` fences (no language tag)
    - Leading/trailing prose around a JSON block

    Raises json.JSONDecodeError if no valid JSON is found.
    """
    # 1. Strip code fences (```json ... ``` or ``` ... ```)
    fenced = re.search(r"```(?:json)?\s*([\s\S]*?)```", raw)
    if fenced:
        candidate = fenced.group(1).strip()
        return json.loads(candidate)

    # 2. Try to find the first JSON array or object in the text
    for pattern in (r"(\[[\s\S]*\])", r"(\{[\s\S]*\})"):
        match = re.search(pattern, raw)
        if match:
            return json.loads(match.group(1))

    # 3. Last resort: parse the whole stripped string
    return json.loads(raw.strip())
