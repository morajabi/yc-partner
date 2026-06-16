#!/usr/bin/env python3
"""Run YC application review evals.

The fixture label is intentionally hidden from the candidate. The runner scores
response quality and reports historical-outcome diagnostics after the response
is produced.
"""

from __future__ import annotations

import argparse
import json
import math
import random
import re
import subprocess
import sys
import tempfile
import textwrap
import time
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
EVAL_DIR = Path(__file__).resolve().parent
DEFAULT_FIXTURES = EVAL_DIR / "fixtures.jsonl"
DEFAULT_SCHEMA = EVAL_DIR / "response.schema.json"
DEFAULT_RECEIPTS = EVAL_DIR / "receipts"

LEAK_PATTERNS = [
    re.compile(r"\bknown_outcome\b", re.IGNORECASE),
    re.compile(r"\bhistorical outcome\b", re.IGNORECASE),
    re.compile(r"\boutcome label\b", re.IGNORECASE),
    re.compile(r"\bapplication outcome\b", re.IGNORECASE),
    re.compile(r"\bgot into yc\b", re.IGNORECASE),
    re.compile(r"\baccepted (?:to|into|by) yc\b", re.IGNORECASE),
    re.compile(r"\brejected (?:by|from) yc\b", re.IGNORECASE),
    re.compile(r"\bwas rejected\b", re.IGNORECASE),
    re.compile(r"\bfamously\b", re.IGNORECASE),
    re.compile(r"\beventually became\b", re.IGNORECASE),
]

GHOSTWRITING_PATTERNS = [
    re.compile(r"\bcopy[- ]?paste this\b", re.IGNORECASE),
    re.compile(r"\bcopy and paste this\b", re.IGNORECASE),
    re.compile(r"\bready to submit\b", re.IGNORECASE),
    re.compile(r"\bfinal version\b", re.IGNORECASE),
    re.compile(r"\bhere(?:'| i)?s a rewritten\b", re.IGNORECASE),
    re.compile(r"\brewritten application\b", re.IGNORECASE),
]

NUMBER_RE = re.compile(
    r"(\$[\d,.]+|\b\d+(?:\.\d+)?\s?(?:%|k|m|b|users?|customers?|companies?|revenue|mrr|arr|months?|weeks?|days?|kloc|employees?)\b)",
    re.IGNORECASE,
)
USER_RE = re.compile(r"\b(users?|customers?|founders?|developers?|restaurants?|researchers?|students?|teams?|companies?)\b", re.IGNORECASE)
TRACTION_RE = re.compile(r"\b(revenue|mrr|arr|paid|paying|launched|beta|prototype|users?|customers?|waitlist|growth|retention|usage)\b", re.IGNORECASE)
FOUNDER_RE = re.compile(r"\b(founder|built|created|programming|engineer|technical|sold|started|launched|worked at|previously)\b", re.IGNORECASE)
LEARNING_RE = re.compile(r"\b(talked|interviewed|learned|observed|requests?|feedback|customer development|manual|discovered)\b", re.IGNORECASE)
VAGUE_RE = re.compile(r"\b(revolutionary|seamless|platform|leverage|synergy|disrupt|ai-powered|next-generation|all-in-one)\b", re.IGNORECASE)
NO_TRACTION_RE = re.compile(r"\b(no users|no revenue|not launched|idea only|haven't launched|have not launched|pre-product|pre-revenue)\b", re.IGNORECASE)


@dataclass
class Fixture:
    id: str
    company: str
    batch: str | None
    prompt: str
    application_markdown: str
    source: str
    source_url: str
    expected: dict[str, Any]


def load_fixtures(path: Path) -> list[Fixture]:
    rows: list[Fixture] = []
    for line_no, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        if not line.strip():
            continue
        raw = json.loads(line)
        rows.append(
            Fixture(
                id=raw["id"],
                company=raw["company"],
                batch=raw.get("batch"),
                prompt=raw["prompt"],
                application_markdown=raw["application_markdown"],
                source=raw["source"],
                source_url=raw["source_url"],
                expected=raw["expected"],
            )
        )
    return rows


def select_fixtures(fixtures: list[Fixture], limit: int | None, fixture_ids: list[str], seed: int) -> list[Fixture]:
    if fixture_ids:
        by_id = {fx.id: fx for fx in fixtures}
        missing = [fixture_id for fixture_id in fixture_ids if fixture_id not in by_id]
        if missing:
            raise SystemExit(f"Unknown fixture id(s): {', '.join(missing)}")
        return [by_id[fixture_id] for fixture_id in fixture_ids]

    if not limit or limit >= len(fixtures):
        return list(fixtures)

    rng = random.Random(seed)
    successful = [fx for fx in fixtures if fx.expected["known_outcome"] == "successful"]
    unsuccessful = [fx for fx in fixtures if fx.expected["known_outcome"] == "unsuccessful"]
    rng.shuffle(successful)
    rng.shuffle(unsuccessful)

    success_target = limit // 2 + (limit % 2)
    unsuccessful_target = limit // 2
    selected = successful[:success_target] + unsuccessful[:unsuccessful_target]
    if len(selected) < limit:
        remaining = [fx for fx in fixtures if fx not in selected]
        rng.shuffle(remaining)
        selected.extend(remaining[: limit - len(selected)])
    rng.shuffle(selected)
    return selected


def build_candidate_prompt(fixture: Fixture) -> str:
    return textwrap.dedent(
        f"""\
        You are running a yc-partner application-review eval.

        Review the application text below. Do not use external knowledge about
        this specific company, founders, YC outcome, later success, or the source
        website. The historical acceptance result is hidden from you on purpose.

        You may use captured yc-partner resources in this repository for general
        YC guidance, source-grounded risks, myth checks, public example patterns,
        YC company-directory context, and sector/landscape questions. Cite those
        resources by exact repo-relative path. Do not browse the web.

        Common valid source paths include:
        - skills/yc-partner/references/application-scorecard.md
        - skills/yc-partner/references/source-priority.md
        - skills/yc-partner/guides/application-review.md
        - skills/yc-partner/guides/application-hygiene.md
        - skills/yc-partner/guides/application-research.md
        - skills/yc-partner/indexes/application-questions.md
        - skills/yc-partner/indexes/source-map.md
        - skills/yc-partner/resources/yc-website/frequently-asked-questions.md
        - skills/yc-partner/resources/yc-youtube/when-is-the-right-time-to-apply-to-y-combinator-jared-friedman-EEy2MYHxAe8.md
        - skills/yc-partner/resources/yc-youtube/how-to-apply-and-succeed-at-y-combinator-startup-school-B5tU2447OK8.md
        - skills/yc-partner/resources/tweets/paul-graham-ready-to-apply-clear-application-2022-09-09.md
        - skills/yc-partner/resources/tweets/paul-graham-revenue-not-required-for-yc-2020-01-05.md
        - skills/yc-partner/resources/tweets/paul-graham-explain-what-you-learned-from-users-2022-09-12.md
        - skills/yc-partner/resources/tweets/paul-graham-hype-misconception-focus-users-2019-11-26.md
        - skills/yc-partner/resources/interviews/lessons-from-working-with-600-yc-startups-gustaf-alstrmer-y-combinator-airbnb-ZoKLofsp8u0.md
        - skills/yc-partner/resources/interviews/lessons-from-1-000-yc-startups-resilience-tar-pit-ideas-pivoting-more-dalton-caldwell-yc-m7LvNTbaqSI.md
        - skills/yc-partner/resources/yc-company-directory/README.md
        - skills/yc-partner/resources/rfs/README.md
        - skills/yc-partner/resources/external/kudu-yc-s22-rejection-email-slack-alternative-2022-06-27.md

        Source class rules:
        - `skill_reference`: paths under skills/yc-partner/references/,
          skills/yc-partner/guides/, or skills/yc-partner/indexes/
        - `official_yc`: official YC website or official YC YouTube resources
        - `yc_affiliated`: YC partner/founder essays, tweets, talks, and interviews
        - `public_example`: public application examples and application videos
        - `yc_directory`: YC company-directory resources
        - `rfs`: YC Requests for Startups resources
        - `external_context`: non-YC external context files
        - `inference`: your own inference when no captured source supports a claim

        Apply this review standard:
        - Identify what the company does in one plain sentence.
        - Build an evidence ledger before scoring: product, user, proof users
          care, progress, founder-market fit, unique insight, market path,
          distribution, and competitive context.
        - Estimate how strong the application text is as an interview case.
          This is a text-only estimate, not an admissions prediction.
        - Do not treat high usage or high revenue as automatically strong.
          Ask whether the evidence is retained, urgent, monetizable, defensible,
          and tied to a large-company path.
        - Do not reward metrics for size. Reward metrics for evidence quality:
          active users, retained users, paid or high-intent users, organic or
          efficient acquisition, rapid growth from a clear baseline, and metrics
          tied to the right first user. Be skeptical of fake-substance metrics:
          cumulative signups, vague "users", waitlists, GMV without take rate,
          pilots without payment, revenue that is consulting/pass-through/one-off,
          paid acquisition without CAC/payback/retention, growth percentages
          without denominators, and demos or LOIs without usage.
        - Do not treat low revenue, pre-revenue, pre-product, or idea stage as
          automatically weak. Look for founder insight, user learning, speed,
          domain expertise, manual work, technical proof, and a credible next
          experiment.
        - Dig into the sector and problem-space profile: marketplace liquidity,
          embedded incumbents, retention, buyer/user split, regulatory risk,
          sales cycle, data advantage, technical proof, distribution, and common
          failure paths when relevant.
        - Reward clear product description, urgent user pain, concrete evidence,
          founder insight, speed, and founder-market fit.
        - Penalize vague answers, unsupported claims, weak user learning,
          unclear differentiation, missing context, and answers that do not
          directly answer the prompt.
        - Separate evidence from inference.
        - Ground YC-specific advice in captured reputable resources and avoid
          reinforcing common myths or misconceptions.
        - Give directional improvements, but do not ghostwrite a final
          copy-paste application.

        Return only JSON matching the provided schema. Use:
        - evidence_ledger: short text for every required evidence category
        - interview_likelihood: 0.0 to 1.0
        - verdict: "likely", "borderline", or "unlikely"
        - score_caveat: one sentence explaining that this is a text-only
          estimate and naming what could move it
        - positive_evidence: short bullets grounded in the text
        - risks: short bullets grounded in the text and, where possible, a
          captured resource
        - missing_specifics: short bullets naming facts the application should add
        - improvements: short directional suggestions, not final copy
        - source_grounding: at least two captured resources with repo-relative
          paths, source classes, and why each resource matters to this review
        - myth_checks: at least one myth correction applied to this application
        - context_probes: sector/landscape/failure-path questions tailored to
          this company
        - evidence_vs_inference: one sentence separating textual evidence from your inference
        - non_ghostwriting_check: true only if your improvements are directional and not a final rewrite

        APPLICATION TEXT:
        {fixture.application_markdown}
        """
    )


def run_codex_candidate(fixture: Fixture, model: str | None, timeout: int, schema_path: Path) -> tuple[str, dict[str, Any]]:
    prompt = build_candidate_prompt(fixture)
    metadata: dict[str, Any] = {"candidate": "codex", "timeout_seconds": timeout}
    with tempfile.NamedTemporaryFile("w+", encoding="utf-8", suffix=".json", delete=False) as out:
        out_path = Path(out.name)
    cmd = [
        "codex",
        "exec",
        "--ephemeral",
        "-C",
        str(ROOT),
        "-s",
        "read-only",
        "--color",
        "never",
        "--output-schema",
        str(schema_path),
        "-o",
        str(out_path),
        "-",
    ]
    if model:
        cmd[2:2] = ["--model", model]
        metadata["model"] = model
    else:
        metadata["model"] = "codex-default"

    started = time.time()
    try:
        completed = subprocess.run(
            cmd,
            input=prompt,
            text=True,
            cwd=ROOT,
            capture_output=True,
            timeout=timeout,
            check=False,
        )
        metadata["duration_seconds"] = round(time.time() - started, 3)
        metadata["returncode"] = completed.returncode
        metadata["stderr_tail"] = completed.stderr[-2000:]
        if out_path.exists():
            output = out_path.read_text(encoding="utf-8").strip()
        else:
            output = completed.stdout.strip()
        if completed.returncode != 0 and not output:
            output = completed.stdout.strip() or completed.stderr.strip()
        return output, metadata
    except subprocess.TimeoutExpired as exc:
        metadata["duration_seconds"] = round(time.time() - started, 3)
        metadata["timeout"] = True
        stdout = exc.stdout if isinstance(exc.stdout, str) else ""
        stderr = exc.stderr if isinstance(exc.stderr, str) else ""
        return (stdout or stderr or "TIMEOUT").strip(), metadata
    finally:
        try:
            out_path.unlink()
        except FileNotFoundError:
            pass


def run_heuristic_candidate(fixture: Fixture) -> tuple[str, dict[str, Any]]:
    text = fixture.application_markdown
    lower = text.lower()
    numbers = NUMBER_RE.findall(text)
    user_terms = USER_RE.findall(text)
    traction_terms = TRACTION_RE.findall(text)
    founder_terms = FOUNDER_RE.findall(text)
    learning_terms = LEARNING_RE.findall(text)
    vague_terms = VAGUE_RE.findall(text)
    no_traction_terms = NO_TRACTION_RE.findall(text)

    score = 0.24
    score += min(len(numbers), 8) * 0.035
    score += min(len(set(term.lower() for term in user_terms)), 5) * 0.025
    score += min(len(set(term.lower() for term in traction_terms)), 8) * 0.025
    score += min(len(set(term.lower() for term in founder_terms)), 6) * 0.02
    score += min(len(set(term.lower() for term in learning_terms)), 5) * 0.025
    score -= min(len(set(term.lower() for term in vague_terms)), 5) * 0.025
    score -= min(len(set(term.lower() for term in no_traction_terms)), 3) * 0.035

    if "### progress" in lower and "### idea" in lower:
        score += 0.04
    if "competitor" in lower or "substitutes" in lower:
        score += 0.025
    if "revenue" in lower and re.search(r"\$|\bpaid|paying\b", lower):
        score += 0.05

    score = max(0.05, min(0.92, score))
    verdict = "likely" if score >= 0.66 else "unlikely" if score <= 0.4 else "borderline"

    positives = []
    if numbers:
        positives.append("The application includes concrete numbers or time/progress markers.")
    if traction_terms:
        positives.append("The text contains product, user, revenue, or launch evidence to inspect.")
    if founder_terms:
        positives.append("The founders provide some building or domain-execution signal.")
    if learning_terms:
        positives.append("There is at least some user-learning or feedback language.")
    if not positives:
        positives.append("The application gives enough product text to start a review.")

    risks = []
    if no_traction_terms or not numbers:
        risks.append("Traction, usage, or revenue evidence may be too thin or underspecified.")
    if vague_terms:
        risks.append("Some wording looks abstract or marketing-like and should be made concrete.")
    if "competitor" not in lower and "substitutes" not in lower:
        risks.append("Differentiation against substitutes or competitors is not obvious from the text.")
    if not learning_terms:
        risks.append("The application may not show enough direct learning from users.")
    if not risks:
        risks.append("The main risk is whether the strongest claims are specific enough for a quick reader.")

    response = {
        "company_description": extract_company_description(fixture),
        "evidence_ledger": {
            "product": extract_company_description(fixture),
            "user": "The likely user/customer segment must be read from the application text and narrowed in review.",
            "proof_users_care": "The application includes signal words for traction, users, revenue, launch status, or customer learning." if traction_terms or learning_terms else "The application needs clearer proof that users care.",
            "progress": "Progress is inferred from launch, prototype, beta, revenue, or time markers in the application text.",
            "founder_market_fit": "Founder-market fit is inferred from building, technical, domain, or prior-startup signals in the text." if founder_terms else "Founder-market fit needs more explicit evidence.",
            "unique_insight": "The application should be checked for a non-obvious insight beyond generic market language.",
            "market_path": "The first wedge and expansion path should be made explicit.",
            "distribution": "The application should explain how the first users are reached without assuming broad paid marketing works.",
            "competitive_context": "The review should inspect substitutes, direct competitors, adjacent YC-funded companies, and why users switch.",
        },
        "interview_likelihood": round(score, 2),
        "verdict": verdict,
        "score_caveat": "This is a text-only estimate from the application; stronger source-backed user learning, retention, founder insight, or sector context could move it up or down.",
        "positive_evidence": positives[:4],
        "risks": risks[:4],
        "missing_specifics": [
            "Add the clearest current usage, revenue, growth, or customer-conversation numbers.",
            "Name the narrow user segment with the most urgent pain.",
            "State what users do today instead and why this approach wins.",
        ],
        "improvements": [
            "Make the first product answer concrete enough that a reader can repeat it in one sentence.",
            "Replace broad claims with factual evidence from users, revenue, speed, or shipped product.",
            "Keep any rewrite directional and verify missing facts before adding them.",
        ],
        "source_grounding": [
            {
                "source_path": "skills/yc-partner/references/application-scorecard.md",
                "source_class": "skill_reference",
                "relevance": "Defines the evidence ledger, myth checks, score bands, and sector-specific review posture.",
            },
            {
                "source_path": "skills/yc-partner/guides/application-review.md",
                "source_class": "skill_reference",
                "relevance": "Captures YC-grounded review guidance on clarity, early-stage readiness, user learning, market path, and founder/team risk.",
            },
        ],
        "myth_checks": [
            {
                "myth": "Revenue or traction alone determines whether a YC application is strong.",
                "correction": "Revenue and usage are evidence, but the review should inspect urgency, retention, founder insight, user learning, and market path.",
                "source_path": "skills/yc-partner/references/application-scorecard.md",
                "applied_to_application": "The score treats traction signals as prompts for deeper inspection, not as automatic proof of application strength.",
            }
        ],
        "context_probes": [
            {
                "angle": "First wedge",
                "why_it_matters": "YC application strength depends on a narrow urgent user and credible first market, not broad category ambition.",
                "next_question": "Which exact user segment has the strongest pain and what behavior proves it?",
            },
            {
                "angle": "Switching or adoption path",
                "why_it_matters": "Usage or interest is weaker if the application cannot explain why users switch from existing substitutes.",
                "next_question": "What do users do today, and what makes this product enough better to change behavior?",
            },
        ],
        "evidence_vs_inference": "The score is based only on textual signals in the application; any interview-likelihood estimate is inference, not outside knowledge.",
        "non_ghostwriting_check": True,
    }
    return json.dumps(response), {"candidate": "heuristic", "model": "local-signal-baseline"}


def extract_company_description(fixture: Fixture) -> str:
    match = re.search(r"^- Description:\s*(.+)$", fixture.application_markdown, re.MULTILINE)
    if match:
        return match.group(1).strip()
    return f"{fixture.company} is described in the application text."


def parse_candidate_json(raw: str) -> tuple[dict[str, Any] | None, str | None]:
    stripped = raw.strip()
    if not stripped:
        return None, "empty response"
    try:
        parsed = json.loads(stripped)
        if isinstance(parsed, dict):
            return parsed, None
        return None, "json was not an object"
    except json.JSONDecodeError:
        pass

    match = re.search(r"\{[\s\S]*\}", stripped)
    if not match:
        return None, "no json object found"
    try:
        parsed = json.loads(match.group(0))
    except json.JSONDecodeError as exc:
        return None, f"json parse error: {exc}"
    if not isinstance(parsed, dict):
        return None, "json was not an object"
    return parsed, None


def has_leak(raw: str, parsed: dict[str, Any] | None) -> list[str]:
    text = raw if parsed is None else json.dumps(parsed, ensure_ascii=False)
    return [pattern.pattern for pattern in LEAK_PATTERNS if pattern.search(text)]


def has_ghostwriting(parsed: dict[str, Any] | None) -> list[str]:
    if parsed is None:
        return []
    text = json.dumps(parsed, ensure_ascii=False)
    hits = [pattern.pattern for pattern in GHOSTWRITING_PATTERNS if pattern.search(text)]
    improvements = parsed.get("improvements")
    if isinstance(improvements, list):
        long_improvements = [item for item in improvements if isinstance(item, str) and len(item) > 700]
        if long_improvements:
            hits.append("improvement item longer than 700 characters")
    if parsed.get("non_ghostwriting_check") is not True:
        hits.append("non_ghostwriting_check was not true")
    return hits


def verdict_consistent(score: float | None, verdict: Any) -> bool:
    if not isinstance(score, (int, float)) or not isinstance(verdict, str):
        return False
    if score >= 0.66:
        return verdict == "likely"
    if score <= 0.4:
        return verdict == "unlikely"
    return verdict == "borderline"


def source_path_exists(source_path: Any) -> bool:
    if not isinstance(source_path, str) or not source_path.strip():
        return False
    clean = source_path.strip().strip("`")
    clean = re.sub(r":\d+(?::\d+)?$", "", clean)
    candidates = [
        ROOT / clean,
        ROOT / "skills/yc-partner" / clean,
        ROOT / "skills/yc-partner/references" / clean,
    ]
    return any(path.exists() for path in candidates)


def source_class_plausible(item: Any) -> bool:
    if not isinstance(item, dict):
        return False
    source_path = item.get("source_path")
    source_class = item.get("source_class")
    if not isinstance(source_path, str) or not isinstance(source_class, str):
        return False
    clean = source_path.strip().strip("`")
    if "/references/" in clean or "/guides/" in clean or "/indexes/" in clean:
        return source_class == "skill_reference"
    if "/resources/yc-website/" in clean or "/resources/yc-youtube/" in clean:
        return source_class == "official_yc"
    if "/resources/yc-company-directory/" in clean:
        return source_class == "yc_directory"
    if "/resources/rfs/" in clean:
        return source_class == "rfs"
    if "/resources/examples/" in clean:
        return source_class == "public_example"
    if "/resources/external/" in clean:
        return source_class == "external_context"
    if (
        "/resources/tweets/" in clean
        or "/resources/interviews/" in clean
        or "/resources/yc-partners/" in clean
        or "/resources/pg-essays/" in clean
        or "/resources/dalton-michael/" in clean
        or "/resources/founder-stories/" in clean
    ):
        return source_class == "yc_affiliated" or ("/resources/founder-stories/" in clean and source_class == "founder_story")
    return source_class == "inference"


def response_quality(fixture: Fixture, parsed: dict[str, Any] | None, parse_error: str | None) -> tuple[float, list[str]]:
    if parsed is None:
        return 0.0, [parse_error or "parse failed"]

    checks: list[tuple[str, bool]] = []
    score = parsed.get("interview_likelihood")
    checks.append(("score_range", isinstance(score, (int, float)) and 0 <= score <= 1))
    checks.append(("verdict_consistent", verdict_consistent(float(score) if isinstance(score, (int, float)) else None, parsed.get("verdict"))))
    checks.append(("score_caveat", isinstance(parsed.get("score_caveat"), str) and len(parsed["score_caveat"].strip()) >= 30))
    ledger = parsed.get("evidence_ledger")
    ledger_keys = [
        "product",
        "user",
        "proof_users_care",
        "progress",
        "founder_market_fit",
        "unique_insight",
        "market_path",
        "distribution",
        "competitive_context",
    ]
    checks.append(
        (
            "evidence_ledger_complete",
            isinstance(ledger, dict)
            and all(isinstance(ledger.get(key), str) and ledger[key].strip() for key in ledger_keys),
        )
    )
    for key in ["positive_evidence", "risks", "missing_specifics", "improvements"]:
        value = parsed.get(key)
        checks.append((f"{key}_nonempty", isinstance(value, list) and any(isinstance(item, str) and item.strip() for item in value)))
    checks.append(("company_description", isinstance(parsed.get("company_description"), str) and len(parsed["company_description"].strip()) >= 12))
    checks.append(("evidence_vs_inference", isinstance(parsed.get("evidence_vs_inference"), str) and len(parsed["evidence_vs_inference"].strip()) >= 20))
    checks.append(("non_ghostwriting_check", parsed.get("non_ghostwriting_check") is True))
    source_grounding = parsed.get("source_grounding")
    checks.append(
        (
            "source_grounding_captured",
            isinstance(source_grounding, list)
            and len(source_grounding) >= 2
            and all(isinstance(item, dict) and source_path_exists(item.get("source_path")) for item in source_grounding[:2]),
        )
    )
    checks.append(
        (
            "source_classes_plausible",
            isinstance(source_grounding, list)
            and len(source_grounding) >= 2
            and all(source_class_plausible(item) for item in source_grounding[:2]),
        )
    )
    myth_checks = parsed.get("myth_checks")
    checks.append(
        (
            "myth_checks_present",
            isinstance(myth_checks, list)
            and any(
                isinstance(item, dict)
                and isinstance(item.get("correction"), str)
                and source_path_exists(item.get("source_path"))
                for item in myth_checks
            ),
        )
    )
    context_probes = parsed.get("context_probes")
    checks.append(
        (
            "context_probes_tailored",
            isinstance(context_probes, list)
            and len(context_probes) >= 2
            and all(
                isinstance(item, dict)
                and isinstance(item.get("angle"), str)
                and isinstance(item.get("why_it_matters"), str)
                and isinstance(item.get("next_question"), str)
                for item in context_probes[:2]
            ),
        )
    )

    app_has_numbers = bool(NUMBER_RE.search(fixture.application_markdown))
    app_has_traction = bool(TRACTION_RE.search(fixture.application_markdown))
    positives = " ".join(str(item) for item in parsed.get("positive_evidence", []) if isinstance(item, str))
    risks = " ".join(str(item) for item in parsed.get("risks", []) if isinstance(item, str))
    missing = " ".join(str(item) for item in parsed.get("missing_specifics", []) if isinstance(item, str))
    myth_text = " ".join(
        " ".join(str(item.get(key, "")) for key in ["myth", "correction", "applied_to_application"])
        for item in parsed.get("myth_checks", [])
        if isinstance(item, dict)
    )
    context_text = " ".join(
        " ".join(str(item.get(key, "")) for key in ["angle", "why_it_matters", "next_question"])
        for item in parsed.get("context_probes", [])
        if isinstance(item, dict)
    )
    risk_text = f"{risks} {missing}"
    checks.append(("mentions_numeric_evidence_when_present", not app_has_numbers or bool(re.search(r"\d|\$|revenue|users?|customers?|growth|paid", positives, re.IGNORECASE))))
    checks.append(("mentions_traction_gap_when_needed", app_has_traction or bool(re.search(r"traction|users?|customers?|revenue|usage|growth|specific", risk_text, re.IGNORECASE))))
    metric_quality_text = f"{risk_text} {myth_text} {context_text}"
    checks.append(
        (
            "metric_quality_skepticism_when_numbers_present",
            not app_has_numbers
            or bool(
                re.search(
                    r"active|retention|retained|repeat|organic|paid acquisition|cac|payback|denominator|baseline|cumulative|signup|waitlist|gmv|take rate|pilot|loi|one[- ]?off|pass[- ]?through|subsidized|vanity|conversion|willingness to pay",
                    metric_quality_text,
                    re.IGNORECASE,
                )
            ),
        )
    )

    failures = [name for name, ok in checks if not ok]
    return (len(checks) - len(failures)) / len(checks), failures


def auc(per_fixture: list[dict[str, Any]]) -> float | None:
    positives = [row for row in per_fixture if row["expected_outcome"] == "successful" and isinstance(row.get("interview_likelihood"), (int, float))]
    negatives = [row for row in per_fixture if row["expected_outcome"] == "unsuccessful" and isinstance(row.get("interview_likelihood"), (int, float))]
    if not positives or not negatives:
        return None
    wins = 0.0
    total = 0
    for pos in positives:
        for neg in negatives:
            total += 1
            if pos["interview_likelihood"] > neg["interview_likelihood"]:
                wins += 1.0
            elif pos["interview_likelihood"] == neg["interview_likelihood"]:
                wins += 0.5
    return wins / total if total else None


def mean(values: list[float]) -> float | None:
    return sum(values) / len(values) if values else None


def summarize(per_fixture: list[dict[str, Any]], thresholds: dict[str, float]) -> dict[str, Any]:
    success_scores = [
        row["interview_likelihood"]
        for row in per_fixture
        if row["expected_outcome"] == "successful" and isinstance(row.get("interview_likelihood"), (int, float))
    ]
    unsuccessful_scores = [
        row["interview_likelihood"]
        for row in per_fixture
        if row["expected_outcome"] == "unsuccessful" and isinstance(row.get("interview_likelihood"), (int, float))
    ]
    mean_success = mean(success_scores)
    mean_unsuccessful = mean(unsuccessful_scores)
    score_gap = None if mean_success is None or mean_unsuccessful is None else mean_success - mean_unsuccessful
    auc_value = auc(per_fixture)
    quality_scores = [row["quality_score"] for row in per_fixture]
    quality_mean = mean(quality_scores) or 0.0

    parse_failures = [row["id"] for row in per_fixture if row["parse_error"]]
    leak_failures = [row["id"] for row in per_fixture if row["leak_patterns"]]
    ghostwriting_failures = [row["id"] for row in per_fixture if row["ghostwriting_patterns"]]
    range_failures = [row["id"] for row in per_fixture if row["range_failure"]]
    high_historical_unsuccessful_scores = [
        row["id"]
        for row in per_fixture
        if row["expected_outcome"] == "unsuccessful" and isinstance(row.get("interview_likelihood"), (int, float)) and row["interview_likelihood"] > 0.75
    ]
    low_historical_successful_scores = [
        row["id"]
        for row in per_fixture
        if row["expected_outcome"] == "successful" and isinstance(row.get("interview_likelihood"), (int, float)) and row["interview_likelihood"] < 0.35
    ]
    extreme_score_mismatches = [
        row["id"]
        for row in per_fixture
        if (
            row["expected_outcome"] == "successful"
            and isinstance(row.get("interview_likelihood"), (int, float))
            and row["interview_likelihood"] < 0.25
        )
        or (
            row["expected_outcome"] == "unsuccessful"
            and isinstance(row.get("interview_likelihood"), (int, float))
            and row["interview_likelihood"] > 0.95
        )
    ]

    pass_checks = {
        "parse_failures": len(parse_failures) == 0,
        "leak_failures": len(leak_failures) == 0,
        "range_failures": len(range_failures) == 0,
        "ghostwriting_failures": len(ghostwriting_failures) == 0,
        "extreme_score_mismatches": len(extreme_score_mismatches) == 0,
        "quality_mean": quality_mean >= thresholds["min_quality_mean"],
    }

    return {
        "count": len(per_fixture),
        "successful_count": len([row for row in per_fixture if row["expected_outcome"] == "successful"]),
        "unsuccessful_count": len([row for row in per_fixture if row["expected_outcome"] == "unsuccessful"]),
        "mean_successful_score": round(mean_success, 4) if mean_success is not None else None,
        "mean_unsuccessful_score": round(mean_unsuccessful, 4) if mean_unsuccessful is not None else None,
        "score_gap": round(score_gap, 4) if score_gap is not None else None,
        "auc": round(auc_value, 4) if auc_value is not None else None,
        "quality_mean": round(quality_mean, 4),
        "parse_failures": parse_failures,
        "leak_failures": leak_failures,
        "range_failures": range_failures,
        "ghostwriting_failures": ghostwriting_failures,
        "high_historical_unsuccessful_scores": high_historical_unsuccessful_scores,
        "low_historical_successful_scores": low_historical_successful_scores,
        "extreme_score_mismatches": extreme_score_mismatches,
        "pass_checks": pass_checks,
        "verdict": "pass" if all(pass_checks.values()) else "fail",
    }


def run(args: argparse.Namespace) -> dict[str, Any]:
    fixtures = load_fixtures(args.fixtures)
    selected = select_fixtures(fixtures, args.limit, args.fixture_id, args.seed)
    started = datetime.now(timezone.utc)
    per_fixture: list[dict[str, Any]] = []

    for index, fixture in enumerate(selected, start=1):
        print(f"[{index}/{len(selected)}] {fixture.id}", file=sys.stderr, flush=True)
        if args.mode == "codex":
            raw, run_metadata = run_codex_candidate(fixture, args.model, args.timeout, args.schema)
        else:
            raw, run_metadata = run_heuristic_candidate(fixture)

        parsed, parse_error = parse_candidate_json(raw)
        leak_patterns = has_leak(raw, parsed)
        ghostwriting_patterns = has_ghostwriting(parsed)
        quality_score, quality_failures = response_quality(fixture, parsed, parse_error)
        score = parsed.get("interview_likelihood") if parsed else None
        range_failure = not isinstance(score, (int, float)) or not 0 <= score <= 1

        expected = fixture.expected
        row = {
            "id": fixture.id,
            "company": fixture.company,
            "source": fixture.source,
            "expected_outcome": expected["known_outcome"],
            "score_band": expected.get("score_band"),
            "interview_likelihood": round(float(score), 4) if isinstance(score, (int, float)) and math.isfinite(score) else None,
            "verdict": parsed.get("verdict") if parsed else None,
            "parse_error": parse_error,
            "range_failure": range_failure,
            "leak_patterns": leak_patterns,
            "ghostwriting_patterns": ghostwriting_patterns,
            "quality_score": round(quality_score, 4),
            "quality_failures": quality_failures,
            "candidate_response": parsed,
            "raw_response_preview": None if parsed else raw[:1200],
            "run_metadata": run_metadata,
        }
        per_fixture.append(row)

    thresholds = {
        "min_score_gap": args.min_score_gap,
        "min_auc": args.min_auc,
        "min_quality_mean": args.min_quality_mean,
    }
    aggregate = summarize(per_fixture, thresholds)
    calibration_gated = args.strict_calibration
    if calibration_gated:
        aggregate["pass_checks"]["score_gap"] = aggregate["score_gap"] is not None and aggregate["score_gap"] >= thresholds["min_score_gap"]
        aggregate["pass_checks"]["auc"] = aggregate["auc"] is not None and aggregate["auc"] >= thresholds["min_auc"]
        aggregate["verdict"] = "pass" if all(aggregate["pass_checks"].values()) else "fail"
    aggregate["calibration_gated"] = calibration_gated
    finished = datetime.now(timezone.utc)
    receipt = {
        "schema_version": 1,
        "eval": "yc-application-review",
        "mode": args.mode,
        "candidate_model": args.model if args.model else ("codex-default" if args.mode == "codex" else "local-signal-baseline"),
        "started_at": started.isoformat(),
        "finished_at": finished.isoformat(),
        "duration_seconds": round((finished - started).total_seconds(), 3),
        "fixtures_path": str(args.fixtures.relative_to(ROOT) if args.fixtures.is_relative_to(ROOT) else args.fixtures),
        "total_fixture_count": len(fixtures),
        "run_fixture_count": len(selected),
        "seed": args.seed,
        "thresholds": thresholds,
        "aggregate": aggregate,
        "per_fixture": per_fixture,
    }
    return receipt


def receipt_path_for(args: argparse.Namespace, receipt: dict[str, Any]) -> Path:
    if args.output:
        return args.output
    DEFAULT_RECEIPTS.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    model_slug = re.sub(r"[^a-zA-Z0-9_.-]+", "-", receipt["candidate_model"])
    return DEFAULT_RECEIPTS / f"{timestamp}-{args.mode}-{model_slug}-{receipt['run_fixture_count']}cases.json"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--fixtures", type=Path, default=DEFAULT_FIXTURES)
    parser.add_argument("--schema", type=Path, default=DEFAULT_SCHEMA)
    parser.add_argument("--mode", choices=["heuristic", "codex"], default="heuristic")
    parser.add_argument("--model", help="Model name passed to codex exec in --mode codex.")
    parser.add_argument("--limit", type=int, help="Run a stratified sample of N fixtures.")
    parser.add_argument("--fixture-id", action="append", default=[], help="Run a specific fixture id. Repeatable.")
    parser.add_argument("--seed", type=int, default=20260616)
    parser.add_argument("--timeout", type=int, default=240, help="Per-fixture timeout for codex mode.")
    parser.add_argument("--output", type=Path, help="Receipt path. Defaults to evals/yc-application-review/receipts/.")
    parser.add_argument("--min-score-gap", type=float, default=0.12)
    parser.add_argument("--min-auc", type=float, default=0.65)
    parser.add_argument("--min-quality-mean", type=float, default=0.75)
    parser.add_argument(
        "--strict-calibration",
        action="store_true",
        help="Also gate on aggregate historical-outcome score gap and AUC diagnostics.",
    )
    args = parser.parse_args()

    if args.limit is not None and args.limit < 1:
        parser.error("--limit must be >= 1")

    receipt = run(args)
    out_path = receipt_path_for(args, receipt)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(receipt, indent=2) + "\n", encoding="utf-8")

    aggregate = receipt["aggregate"]
    print(f"Wrote receipt to {out_path}")
    print(f"Verdict: {aggregate['verdict']}")
    print(f"Fixtures: {aggregate['count']} ({aggregate['successful_count']} successful / {aggregate['unsuccessful_count']} unsuccessful)")
    print(f"Mean scores: successful={aggregate['mean_successful_score']} unsuccessful={aggregate['mean_unsuccessful_score']} gap={aggregate['score_gap']}")
    print(f"AUC: {aggregate['auc']}")
    print(f"Calibration gated: {aggregate['calibration_gated']}")
    print(f"Quality mean: {aggregate['quality_mean']}")
    print(f"Parse failures: {len(aggregate['parse_failures'])}")
    print(f"Leak failures: {len(aggregate['leak_failures'])}")
    print(f"Ghostwriting failures: {len(aggregate['ghostwriting_failures'])}")
    return 0 if aggregate["verdict"] == "pass" else 1


if __name__ == "__main__":
    raise SystemExit(main())
