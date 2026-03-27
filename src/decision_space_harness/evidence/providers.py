from __future__ import annotations

from dataclasses import dataclass

from decision_space_harness.schemas.core import Task


@dataclass
class TopKEvidenceProvider:
    name: str

    def get_base_evidence(self, task: Task, provider_config: str, seed: int) -> dict:
        suffix = "".join(ch for ch in provider_config if ch.isdigit())
        top_k = int(suffix) if suffix else len(task.evidence_items)
        items = task.evidence_items[:top_k]
        return {
            "bundle_id": f"{task.task_id}_{provider_config}_seed{seed}",
            "items": items,
            "order_sensitive": True,
            "permutation_id": "identity",
            "base_bundle_id": f"{task.task_id}_{provider_config}_base",
        }
