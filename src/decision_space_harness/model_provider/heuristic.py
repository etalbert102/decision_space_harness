from __future__ import annotations

import json
from dataclasses import dataclass

from decision_space_harness.schemas.core import GenerationConfig, ModelResponse


@dataclass
class HeuristicModelProvider:
    model_name: str = "local_model"

    def generate(self, messages: list[dict], config: GenerationConfig) -> ModelResponse:
        payload = json.loads(messages[-1]["content"])
        agent_name = payload.get("agent_name", "baseline_direct")
        prompt_variant = payload.get("prompt_variant", "default")
        candidate_option_ids = payload["candidate_option_ids"]
        if agent_name == "baseline_direct":
            generated_options = candidate_option_ids[:1]
        elif agent_name == "retrieve_then_synthesize":
            generated_options = candidate_option_ids[:1]
        elif agent_name == "option_generation":
            generated_options = candidate_option_ids[:]
        else:
            generated_options = candidate_option_ids[:]

        selected_option_id = generated_options[0]
        represented_frames = payload["relevant_frame_ids"][:2]
        if prompt_variant == "disagreement_preserving":
            preserved_conflicts = payload["expected_conflict_ids"][:]
        elif agent_name == "structured_conflict_preserving":
            preserved_conflicts = payload["expected_conflict_ids"][:]
        else:
            preserved_conflicts = payload["expected_conflict_ids"][:1]
        cited_evidence = payload["evidence_ids"][:2]
        text = "\n".join(
            [
                f"FINAL_ANSWER: Recommend {selected_option_id} while preserving key disagreement.",
                f"SELECTED_OPTION: {selected_option_id}",
                f"REPRESENTED_FRAMES: {','.join(represented_frames)}",
                f"PRESERVED_CONFLICTS: {','.join(preserved_conflicts)}",
                f"GENERATED_OPTIONS: {','.join(generated_options)}",
                f"CITED_EVIDENCE: {','.join(cited_evidence)}",
            ]
        )
        return ModelResponse(
            text=text,
            model=self.model_name,
            tokens_used=max(1, len(text.split())),
            generation_params={
                "temperature": config.temperature,
                "top_p": config.top_p,
                "top_k": config.top_k,
                "seed": config.seed,
                "max_tokens": config.max_tokens,
                "format": config.format,
            },
        )
