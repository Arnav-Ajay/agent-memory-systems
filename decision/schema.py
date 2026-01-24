# decision/schema.py
from __future__ import annotations
from dataclasses import dataclass
from typing import Literal

Confidence = Literal["high", "medium", "low"]

@dataclass(frozen=True)
class RetrievalDecision:
    """
    IMPORTANT:
    - Must be computed from QUESTION ONLY.
    - Must be loggable.
    - decision_rationale is a short label (not chain-of-thought).
    """
    requires_external_evidence: bool
    decision_rationale: str
    confidence: Confidence
