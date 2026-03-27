from __future__ import annotations

import json
from dataclasses import dataclass

from decision_space_harness.schemas.core import AgentResult, GenerationConfig, Task


@dataclass
class RetrieveThenSynthesizeAgent:
    name: str = "retrieve_then_synthesize"

    def run_agent(
        self,
        *,
        task: Task,
        evidence_bundle: dict,
        prompt_variant: str,
        model_name: str,
        seed: int,
        model_provider,
    ) -> AgentResult:
        evidence_ids = [item["evidence_id"] for item in evidence_bundle["items"]]
        context = {
            "agent_name": self.name,
            "task_id": task.task_id,
            "query": task.query,
            "candidate_option_ids": task.annotations["candidate_option_ids"],
            "relevant_frame_ids": task.annotations["relevant_frame_ids"],
            "expected_conflict_ids": task.annotations["expected_conflict_ids"],
            "evidence_ids": evidence_ids,
            "prompt_variant": prompt_variant,
        }
        response = model_provider.generate(
            messages=[{"role": "user", "content": json.dumps(context, sort_keys=True)}],
            config=GenerationConfig(seed=seed),
        )
        return AgentResult(
            raw_output_text=response.text,
            artifact_schema="retrieve_then_synthesize_artifacts/v1",
            artifact_payload={
                "prompt_variant": prompt_variant,
                "retrieved_doc_ids": evidence_ids,
                "raw_output": response.text,
            },
            parse_status="valid",
            cited_evidence_ids=evidence_ids[:2],
            model_provenance={
                "model": response.model,
                "generation_params": response.generation_params,
                "tokens_used": response.tokens_used,
            },
            message_trace=[
                {
                    "sender_agent": self.name,
                    "receiver_agent": self.name,
                    "message_type": "retrieval_summary",
                    "content": f"Retrieved evidence: {','.join(evidence_ids)}",
                    "parent_message_id": None,
                    "referenced_evidence_ids": evidence_ids,
                    "referenced_option_ids": [],
                    "referenced_conflict_ids": [],
                },
                {
                    "sender_agent": self.name,
                    "receiver_agent": self.name,
                    "message_type": "final_proposal",
                    "content": response.text,
                    "parent_message_id": None,
                    "referenced_evidence_ids": evidence_ids[:2],
                    "referenced_option_ids": task.annotations["candidate_option_ids"][:1],
                    "referenced_conflict_ids": task.annotations["expected_conflict_ids"][:1],
                },
            ],
        )
