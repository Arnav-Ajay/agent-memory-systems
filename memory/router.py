# memory/router.py
from __future__ import annotations

import json
import os
import time
from dataclasses import dataclass, asdict
from typing import Any, Dict, List, Optional


# -------------------------
# Data contracts
# -------------------------

@dataclass
class MemoryEvent:
    ts_utc: float
    event_type: str  # "read" | "write"
    store: str       # "episodic" | "semantic"
    key: str
    payload: Dict[str, Any]


# -------------------------
# File-backed stores (Week-8 minimal)
# -------------------------

class EpisodicStore:
    """
    Append-only event memory. Decay policy can be added later via policies/.
    """
    def __init__(self, path: str):
        self.path = path
        os.makedirs(os.path.dirname(path), exist_ok=True)

    def append(self, record: Dict[str, Any]) -> None:
        with open(self.path, "a", encoding="utf-8") as f:
            f.write(json.dumps(record, ensure_ascii=False) + "\n")

    def tail(self, n: int = 50) -> List[Dict[str, Any]]:
        if not os.path.exists(self.path):
            return []
        # Simple tail: read all then slice (fine for Week-8 scale)
        with open(self.path, "r", encoding="utf-8") as f:
            lines = [ln.strip() for ln in f.readlines() if ln.strip()]
        out = []
        for ln in lines[-n:]:
            try:
                out.append(json.loads(ln))
            except Exception:
                continue
        return out


class SemanticStore:
    """
    Small JSON dict store. Gating/dedup can be added later via policies/.
    """
    def __init__(self, path: str):
        self.path = path
        os.makedirs(os.path.dirname(path), exist_ok=True)

    def load(self) -> Dict[str, Any]:
        if not os.path.exists(self.path):
            return {}
        try:
            with open(self.path, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return {}

    def save(self, data: Dict[str, Any]) -> None:
        with open(self.path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    def get(self, key: str) -> Optional[Any]:
        data = self.load()
        return data.get(key)

    def set(self, key: str, value: Any) -> None:
        data = self.load()
        data[key] = value
        self.save(data)


# -------------------------
# Memory Router (single authority)
# -------------------------

class MemoryRouter:
    """
    The only place allowed to touch persisted memory.
    Runtime calls this. Planner/Executor do not.
    """

    def __init__(
        self,
        episodic_path: str = "artifacts/memory/episodic.jsonl",
        semantic_path: str = "artifacts/memory/semantic.json",
        events_path: str = "artifacts/memory/events.jsonl",
    ):
        self.episodic = EpisodicStore(episodic_path)
        self.semantic = SemanticStore(semantic_path)
        self.events_path = events_path
        os.makedirs(os.path.dirname(events_path), exist_ok=True)

    def _log_event(self, ev: MemoryEvent) -> None:
        with open(self.events_path, "a", encoding="utf-8") as f:
            f.write(json.dumps(asdict(ev), ensure_ascii=False) + "\n")

    # ---- Reads ----
    def read_semantic(self, key: str) -> Optional[Any]:
        val = self.semantic.get(key)
        self._log_event(MemoryEvent(
            ts_utc=time.time(),
            event_type="read",
            store="semantic",
            key=key,
            payload={"found": val is not None},
        ))
        return val

    def read_recent_episodic(self, n: int = 25) -> List[Dict[str, Any]]:
        rows = self.episodic.tail(n=n)
        self._log_event(MemoryEvent(
            ts_utc=time.time(),
            event_type="read",
            store="episodic",
            key=f"tail:{n}",
            payload={"returned": len(rows)},
        ))
        return rows

    # ---- Writes ----
    def write_episodic(self, record: Dict[str, Any]) -> None:
        self.episodic.append(record)
        self._log_event(MemoryEvent(
            ts_utc=time.time(),
            event_type="write",
            store="episodic",
            key="append",
            payload={"keys": sorted(list(record.keys()))[:25]},
        ))

    def write_semantic(self, key: str, value: Any) -> None:
        self.semantic.set(key, value)
        self._log_event(MemoryEvent(
            ts_utc=time.time(),
            event_type="write",
            store="semantic",
            key=key,
            payload={"type": type(value).__name__},
        ))
