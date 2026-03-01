import json
from dataclasses import dataclass
from typing import Optional, Literal, Any, Dict
from openai import OpenAI

from loopback.config import settings

DepartmentId = Literal["CTA_OPS", "CITY_311", "SECURITY", "COMMUNITY"]

@dataclass(frozen=True)
class LLMTriageResult:
    final_severity_1to5: int
    reason: str
    department: DepartmentId
    complaint_draft: str
    meta: Dict[str, Any]

_PROMPT = """You are a civic operations triage assistant for a city.
Return STRICT JSON only (no extra text).

Goal:
Given an aggregated city issue (category + location + crowd signal + avg priority),
1) produce a severity rating (1..5),
2) choose the department,
3) write a professional complaint draft that can be sent to that department.

Rules:
- Severity should primarily follow base_severity, but you may adjust by at most +/- 1.
- You must consider TWO factors in your reasoning:
  (a) avg_user_priority and (b) unique_user_count.
- The complaint draft must include the location_text, category, and what action is requested.
- If immediate danger is mentioned, add: "If this is an emergency or someone is in immediate danger, call 911."

Output JSON schema:
{
  "final_severity_1to5": 1..5,
  "reason": "string",
  "department": "CTA_OPS|CITY_311|SECURITY|COMMUNITY",
  "complaint_draft": "string",
  "meta": { ... }
}
"""

def _clamp_llm_severity(base: int, llm: int) -> int:
    base = max(1, min(5, base))
    llm = max(1, min(5, llm))
    delta = llm - base
    if delta > settings.MAX_LLM_SEVERITY_ADJUST:
        return base + settings.MAX_LLM_SEVERITY_ADJUST
    if delta < -settings.MAX_LLM_SEVERITY_ADJUST:
        return base - settings.MAX_LLM_SEVERITY_ADJUST
    return llm

def triage_with_llm(
    *,
    category: str,
    location_text: str,
    report_count: int,
    unique_user_count: int,
    avg_user_priority: float,
    base_severity_1to5: int,
    proposed_department: str,
    sample_reports: list[str],
) -> Optional[LLMTriageResult]:
    if not settings.OPENAI_API_KEY:
        return None

    client = OpenAI(api_key=settings.OPENAI_API_KEY)

    payload = {
        "category": category,
        "location_text": location_text,
        "aggregates": {
            "report_count": report_count,
            "unique_user_count": unique_user_count,
            "avg_user_priority": round(avg_user_priority, 2),
            "base_severity_1to5": base_severity_1to5,
            "proposed_department": proposed_department,
        },
        "sample_reports": sample_reports[:5],
    }

    resp = client.responses.create(
        model=settings.OPENAI_MODEL,
        input=[
            {"role": "system", "content": _PROMPT},
            {"role": "user", "content": json.dumps(payload, ensure_ascii=False)},
        ],
    )

    # Best-effort parse
    text = resp.output_text
    data = json.loads(text)

    llm_sev = int(data.get("final_severity_1to5", base_severity_1to5))
    final_sev = _clamp_llm_severity(base_severity_1to5, llm_sev)

    dept = str(data.get("department", proposed_department)).upper()
    if dept not in {"CTA_OPS", "CITY_311", "SECURITY", "COMMUNITY"}:
        dept = proposed_department

    reason = str(data.get("reason", "")).strip()[:800] or "LLM triage result."
    draft = str(data.get("complaint_draft", "")).strip()[:2000] or f"Please investigate {category} at {location_text}."

    meta = data.get("meta", {})
    if not isinstance(meta, dict):
        meta = {"raw_meta": meta}

    return LLMTriageResult(
        final_severity_1to5=final_sev,
        reason=reason,
        department=dept,  # type: ignore
        complaint_draft=draft,
        meta=meta,
    )