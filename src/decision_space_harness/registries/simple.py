from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass
class SimpleRegistry:
    items: dict[str, Any] = field(default_factory=dict)

    def register(self, name: str, value: Any) -> None:
        if name in self.items:
            raise ValueError(f"Registry entry already exists: {name}")
        self.items[name] = value

    def get(self, name: str) -> Any:
        if name not in self.items:
            raise KeyError(f"Unknown registry entry: {name}")
        return self.items[name]


@dataclass
class RegistrySet:
    task_families: SimpleRegistry = field(default_factory=SimpleRegistry)
    evidence_providers: SimpleRegistry = field(default_factory=SimpleRegistry)
    perturbation_operators: SimpleRegistry = field(default_factory=SimpleRegistry)
    study_protocols: SimpleRegistry = field(default_factory=SimpleRegistry)
    agents: SimpleRegistry = field(default_factory=SimpleRegistry)
    metrics: SimpleRegistry = field(default_factory=SimpleRegistry)
    normalizers: SimpleRegistry = field(default_factory=SimpleRegistry)
