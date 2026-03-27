from __future__ import annotations

from pathlib import Path


def _mean(scores: list[float]) -> float | None:
    return None if not scores else sum(scores) / len(scores)


def summarize_metric_results(metric_results: list[dict]) -> dict:
    overall: dict[str, dict] = {}
    by_agent: dict[tuple[str, str], dict] = {}
    by_protocol: dict[tuple[str, str], dict] = {}

    for row in metric_results:
        score = row.get("score")
        metric_id = row["metric_id"]
        agent_name = row.get("agent_config", "unknown")
        protocol_name = row.get("study_protocol", "unknown")

        overall_entry = overall.setdefault(metric_id, {"scores": [], "unassessable_count": 0})
        if score is None:
            overall_entry["unassessable_count"] += 1
        else:
            overall_entry["scores"].append(score)

        agent_entry = by_agent.setdefault(
            (metric_id, agent_name), {"scores": [], "unassessable_count": 0}
        )
        if score is None:
            agent_entry["unassessable_count"] += 1
        else:
            agent_entry["scores"].append(score)

        protocol_entry = by_protocol.setdefault(
            (metric_id, protocol_name), {"scores": [], "unassessable_count": 0}
        )
        if score is None:
            protocol_entry["unassessable_count"] += 1
        else:
            protocol_entry["scores"].append(score)

    return {
        "overall": [
            {
                "metric_id": metric_id,
                "mean_score": _mean(entry["scores"]),
                "scored_count": len(entry["scores"]),
                "unassessable_count": entry["unassessable_count"],
            }
            for metric_id, entry in sorted(overall.items())
        ],
        "by_agent": [
            {
                "metric_id": metric_id,
                "agent_config": agent_name,
                "mean_score": _mean(entry["scores"]),
                "scored_count": len(entry["scores"]),
                "unassessable_count": entry["unassessable_count"],
            }
            for (metric_id, agent_name), entry in sorted(by_agent.items())
        ],
        "by_protocol": [
            {
                "metric_id": metric_id,
                "study_protocol": protocol_name,
                "mean_score": _mean(entry["scores"]),
                "scored_count": len(entry["scores"]),
                "unassessable_count": entry["unassessable_count"],
            }
            for (metric_id, protocol_name), entry in sorted(by_protocol.items())
        ],
    }


def write_summary_table_csv(path: str | Path, summary_table: dict) -> None:
    output_path = Path(path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    rows = ["slice,metric_id,dimension_value,mean_score,scored_count,unassessable_count"]
    for row in summary_table["overall"]:
        rows.append(
            f"overall,{row['metric_id']},all,{row['mean_score']},{row['scored_count']},{row['unassessable_count']}"
        )
    for row in summary_table["by_agent"]:
        rows.append(
            f"by_agent,{row['metric_id']},{row['agent_config']},{row['mean_score']},{row['scored_count']},{row['unassessable_count']}"
        )
    for row in summary_table["by_protocol"]:
        rows.append(
            f"by_protocol,{row['metric_id']},{row['study_protocol']},{row['mean_score']},{row['scored_count']},{row['unassessable_count']}"
        )
    output_path.write_text("\n".join(rows) + "\n", encoding="utf-8")


def write_metric_figure(path: str | Path, summary_table: dict) -> None:
    output_path = Path(path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    lines = ["Metric Means", "============", ""]
    for row in summary_table["overall"]:
        mean_score = row["mean_score"] or 0.0
        bar = "#" * max(1, round(mean_score * 20)) if row["scored_count"] else ""
        lines.append(f"{row['metric_id']:<28} {mean_score:.3f} {bar}")
    output_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
