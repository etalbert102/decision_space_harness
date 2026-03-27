from __future__ import annotations

import random
from dataclasses import dataclass

from decision_space_harness.schemas.core import Task


@dataclass
class ShuffleEvidenceOperator:
    name: str = "shuffle_evidence/v1"

    def apply(self, task: Task, base_bundle: dict, operator_config: str, seed: int) -> dict:
        rng = random.Random(seed)
        items = list(base_bundle["items"])
        rng.shuffle(items)
        return {
            "bundle_id": f"{base_bundle['bundle_id']}_{operator_config}_seed{seed}",
            "items": items,
            "order_sensitive": True,
            "permutation_id": f"shuffle_{seed}",
            "base_bundle_id": base_bundle["bundle_id"],
            "operator_id": operator_config,
        }

    def describe_constraints(self) -> dict:
        return {"preserves_membership": True, "changes_order_only": True}
