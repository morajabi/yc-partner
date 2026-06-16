#!/usr/bin/env python3
"""Capture the public YC company directory and derive group partner profiles."""

from __future__ import annotations

import argparse
import csv
import html
import json
import re
import sys
import time
import urllib.parse
import urllib.request
from collections import Counter, defaultdict
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


DIRECTORY_URL = "https://www.ycombinator.com/companies"
ALGOLIA_RE = re.compile(r"window\.AlgoliaOpts = (\{.*?\});")
DATA_PAGE_RE = re.compile(r'data-page="([^"]+)"')
DEFAULT_OUTPUT_DIR = Path("skills/yc-partner/resources/yc-company-directory")
USER_AGENT = "yc-partner-directory-capture/1.0 (+https://www.ycombinator.com/companies)"


@dataclass(frozen=True)
class AlgoliaOptions:
    app: str
    key: str


def request_json(url: str, payload: dict[str, Any], headers: dict[str, str]) -> dict[str, Any]:
    body = json.dumps(payload).encode("utf-8")
    request = urllib.request.Request(url, data=body, headers=headers, method="POST")
    with urllib.request.urlopen(request, timeout=30) as response:
        return json.load(response)


def request_text(url: str) -> str:
    request = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(request, timeout=30) as response:
        return response.read().decode("utf-8", errors="replace")


def get_algolia_options() -> AlgoliaOptions:
    page = request_text(DIRECTORY_URL)
    match = ALGOLIA_RE.search(page)
    if not match:
        raise RuntimeError("Could not find public Algolia options on YC directory page")
    options = json.loads(match.group(1))
    return AlgoliaOptions(app=options["app"], key=options["key"])


def algolia_headers(options: AlgoliaOptions) -> dict[str, str]:
    return {
        "Content-Type": "application/json",
        "User-Agent": USER_AGENT,
        "X-Algolia-Application-Id": options.app,
        "X-Algolia-API-Key": options.key,
    }


def query_algolia(
    options: AlgoliaOptions,
    index: str,
    params: dict[str, Any],
) -> dict[str, Any]:
    encoded_params = urllib.parse.urlencode(params, doseq=False)
    url = f"https://{options.app}-dsn.algolia.net/1/indexes/{index}/query"
    return request_json(url, {"params": encoded_params}, algolia_headers(options))


def get_batches(options: AlgoliaOptions, index: str) -> list[str]:
    data = query_algolia(
        options,
        index,
        {
            "query": "",
            "hitsPerPage": 0,
            "facets": json.dumps(["batch"]),
            "maxValuesPerFacet": 250,
        },
    )
    batches = data.get("facets", {}).get("batch", {})
    if not batches:
        raise RuntimeError("Could not read batch facets from YC company index")
    return sorted(batches)


def get_companies(options: AlgoliaOptions, index: str) -> list[dict[str, Any]]:
    companies_by_id: dict[str, dict[str, Any]] = {}
    for batch in get_batches(options, index):
        data = query_algolia(
            options,
            index,
            {
                "query": "",
                "hitsPerPage": 500,
                "page": 0,
                "facetFilters": json.dumps([f"batch:{batch}"]),
            },
        )
        hits = data.get("hits", [])
        if len(hits) != data.get("nbHits"):
            raise RuntimeError(
                f"Batch {batch!r} returned {len(hits)} hits for {data.get('nbHits')} total hits"
            )
        for hit in hits:
            object_id = str(hit.get("objectID") or hit.get("id"))
            companies_by_id[object_id] = hit
    return sorted(
        companies_by_id.values(),
        key=lambda hit: (str(hit.get("batch") or ""), str(hit.get("name") or "").lower()),
    )


def parse_company_page(slug: str) -> dict[str, Any]:
    url = f"https://www.ycombinator.com/companies/{slug}"
    page = request_text(url)
    match = DATA_PAGE_RE.search(page)
    if not match:
        raise RuntimeError("missing data-page payload")
    data = json.loads(html.unescape(match.group(1)))
    company = data.get("props", {}).get("company", {})
    group_partner = company.get("primary_group_partner")
    if not group_partner:
        return {"slug": slug, "primary_group_partner": None}
    return {
        "slug": slug,
        "primary_group_partner": {
            "id": group_partner.get("id"),
            "full_name": group_partner.get("full_name"),
            "url": group_partner.get("url"),
        },
    }


def enrich_group_partners(
    companies: list[dict[str, Any]],
    workers: int,
    retries: int,
) -> tuple[dict[str, dict[str, Any]], list[dict[str, str]]]:
    enrichments: dict[str, dict[str, Any]] = {}
    errors: list[dict[str, str]] = []

    def fetch_with_retries(slug: str) -> dict[str, Any]:
        last_error: Exception | None = None
        for attempt in range(retries + 1):
            try:
                return parse_company_page(slug)
            except Exception as error:  # noqa: BLE001 - report public-page capture failures.
                last_error = error
                time.sleep(min(0.5 * (attempt + 1), 3.0))
        assert last_error is not None
        raise last_error

    with ThreadPoolExecutor(max_workers=workers) as executor:
        futures = {
            executor.submit(fetch_with_retries, str(company["slug"])): str(company["slug"])
            for company in companies
            if company.get("slug")
        }
        for i, future in enumerate(as_completed(futures), 1):
            slug = futures[future]
            try:
                enrichment = future.result()
                enrichments[slug] = enrichment
            except Exception as error:  # noqa: BLE001 - keep capture going and record misses.
                errors.append({"slug": slug, "error": str(error)})
            if i % 250 == 0:
                print(f"Enriched {i}/{len(futures)} company pages", file=sys.stderr)
    return enrichments, errors


def normalize_company(hit: dict[str, Any], enrichment: dict[str, Any] | None) -> dict[str, Any]:
    group_partner = (enrichment or {}).get("primary_group_partner")
    return {
        "id": hit.get("id"),
        "name": hit.get("name"),
        "slug": hit.get("slug"),
        "url": f"https://www.ycombinator.com/companies/{hit.get('slug')}",
        "batch": hit.get("batch"),
        "batch_code": company_batch_code(hit),
        "group_partner": group_partner,
        "industry": hit.get("industry"),
        "subindustry": hit.get("subindustry"),
        "sectors": hit.get("industries") or compact_list([hit.get("industry"), hit.get("subindustry")]),
        "tags": hit.get("tags") or [],
        "one_liner": hit.get("one_liner"),
        "status": hit.get("status"),
        "stage": hit.get("stage"),
        "regions": hit.get("regions") or [],
        "locations": hit.get("all_locations"),
        "team_size": hit.get("team_size"),
        "website": hit.get("website"),
    }


def company_batch_code(hit: dict[str, Any]) -> str | None:
    batch = hit.get("batch")
    if not isinstance(batch, str):
        return None
    match = re.match(r"^(Winter|Spring|Summer|Fall) (\d{4})$", batch)
    if not match:
        return None
    season, year = match.groups()
    return f"{season[0]}{year[-2:]}"


def compact_list(values: list[Any]) -> list[Any]:
    result = []
    for value in values:
        if value and value not in result:
            result.append(value)
    return result


def group_partner_profiles(companies: list[dict[str, Any]]) -> list[dict[str, Any]]:
    grouped: dict[str, dict[str, Any]] = {}
    for company in companies:
        partner = company.get("group_partner")
        if not partner or not partner.get("full_name"):
            continue
        key = str(partner.get("id") or partner["full_name"])
        profile = grouped.setdefault(
            key,
            {
                "group_partner": partner,
                "company_count": 0,
                "batches": Counter(),
                "industries": Counter(),
                "sectors": Counter(),
                "tags": Counter(),
                "stages": Counter(),
                "example_companies": [],
            },
        )
        profile["company_count"] += 1
        if company.get("batch"):
            profile["batches"][company["batch"]] += 1
        if company.get("industry"):
            profile["industries"][company["industry"]] += 1
        for sector in company.get("sectors", []):
            profile["sectors"][sector] += 1
        for tag in company.get("tags", []):
            profile["tags"][tag] += 1
        if company.get("stage"):
            profile["stages"][company["stage"]] += 1
        if len(profile["example_companies"]) < 12:
            profile["example_companies"].append(
                {
                    "name": company["name"],
                    "batch": company["batch"],
                    "url": company["url"],
                    "one_liner": company.get("one_liner"),
                    "sectors": company.get("sectors", []),
                    "tags": company.get("tags", []),
                }
            )

    profiles = []
    for profile in grouped.values():
        profiles.append(
            {
                "group_partner": profile["group_partner"],
                "company_count": profile["company_count"],
                "top_industries": profile["industries"].most_common(12),
                "top_sectors": profile["sectors"].most_common(15),
                "top_tags": profile["tags"].most_common(20),
                "top_batches": profile["batches"].most_common(10),
                "top_stages": profile["stages"].most_common(8),
                "example_companies": profile["example_companies"],
            }
        )
    return sorted(
        profiles,
        key=lambda profile: (-profile["company_count"], profile["group_partner"]["full_name"]),
    )


def write_json(path: Path, data: Any) -> None:
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def write_csv(path: Path, companies: list[dict[str, Any]]) -> None:
    fields = [
        "name",
        "batch",
        "group_partner",
        "industry",
        "sectors",
        "tags",
        "url",
        "one_liner",
        "status",
        "stage",
    ]
    with path.open("w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        for company in companies:
            writer.writerow(
                {
                    "name": clean_cell(company.get("name")),
                    "batch": clean_cell(company.get("batch")),
                    "group_partner": clean_cell((company.get("group_partner") or {}).get("full_name")),
                    "industry": clean_cell(company.get("industry")),
                    "sectors": clean_cell("; ".join(company.get("sectors", []))),
                    "tags": clean_cell("; ".join(company.get("tags", []))),
                    "url": clean_cell(company.get("url")),
                    "one_liner": clean_cell(company.get("one_liner")),
                    "status": clean_cell(company.get("status")),
                    "stage": clean_cell(company.get("stage")),
                }
            )


def clean_cell(value: Any) -> str:
    if value is None:
        return ""
    return str(value).strip()


def markdown_table(rows: list[tuple[str, int]], limit: int) -> str:
    if not rows:
        return "_None captured._"
    lines = ["| Item | Companies |", "| --- | ---: |"]
    for item, count in rows[:limit]:
        lines.append(f"| {escape_md(str(item))} | {count} |")
    return "\n".join(lines)


def escape_md(value: str) -> str:
    return value.replace("|", "\\|")


def write_profiles_markdown(
    path: Path,
    profiles: list[dict[str, Any]],
    captured: str,
    company_count: int,
    enriched_count: int,
    error_count: int,
) -> None:
    lines = [
        "# YC Company Directory Group Partner Profiles",
        "",
        "- Type: derived directory analysis",
        "- Status: public YC directory capture",
        f"- URL: {DIRECTORY_URL}",
        f"- Captured: {captured}",
        "- Method: public YC directory Algolia index plus public company page `primary_group_partner` fields",
        "",
        "## Summary",
        "",
        f"- Captured {company_count} public YC company directory entries.",
        f"- Found primary group partner values for {enriched_count} companies.",
        f"- Company page enrichment errors: {error_count}.",
        "- Partner interests below are inferred from public directory assignments, not stated preferences by YC or the partners.",
        "- Counts are directional because many older company pages do not publish a primary group partner value.",
        "",
        "## Profiles",
        "",
    ]
    for profile in profiles:
        partner = profile["group_partner"]
        name = partner["full_name"]
        url = partner.get("url")
        heading = f"### [{name}]({url})" if url else f"### {name}"
        lines.extend(
            [
                heading,
                "",
                f"- Companies with captured primary group partner: {profile['company_count']}",
                "",
                "Top industries:",
                "",
                markdown_table(profile["top_industries"], 8),
                "",
                "Top sectors:",
                "",
                markdown_table(profile["top_sectors"], 10),
                "",
                "Top tags:",
                "",
                markdown_table(profile["top_tags"], 12),
                "",
                "Example companies:",
                "",
            ]
        )
        for company in profile["example_companies"][:8]:
            tags = ", ".join(company.get("tags", [])[:5])
            one_liner = clean_cell(company.get("one_liner"))
            lines.append(
                f"- [{escape_md(company['name'])}]({company['url']}) ({company['batch']}): "
                f"{escape_md(one_liner)}"
                + (f" Tags: {escape_md(tags)}." if tags else "")
            )
        lines.append("")
    path.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")


def write_readme(
    path: Path,
    captured: str,
    company_count: int,
    enriched_count: int,
    profiles_count: int,
    error_count: int,
) -> None:
    path.write_text(
        "\n".join(
            [
                "# YC Company Directory",
                "",
                "- Type: directory dataset",
                "- Status: public YC directory capture",
                f"- URL: {DIRECTORY_URL}",
                f"- Captured: {captured}",
                "- Method: public YC directory Algolia index plus public company page `primary_group_partner` fields",
                "",
                "## Summary",
                "",
                f"- `companies.json` contains {company_count} parsed public company directory entries.",
                "- Each company includes name, batch, YC directory URL, group partner when published, industry, sectors, tags, one-liner, status, stage, regions, location, team size, and website.",
                "- `companies.csv` is a compact spreadsheet-friendly export of company, batch, group partner, industry, sectors, tags, URL, one-liner, status, and stage.",
                f"- `group-partner-profiles.json` and `group-partner-profiles.md` summarize {profiles_count} group partners from {enriched_count} companies with published primary group partner values.",
                f"- Company page enrichment errors: {error_count}. See `capture-errors.json` when non-empty.",
                "- Partner areas are inferred from assigned companies in the public directory, not from stated YC partner preferences.",
                "- Older company pages often have no `primary_group_partner`; those companies remain in the directory with `group_partner: null`.",
                "",
                "## Content",
                "",
                "- `companies.json`",
                "- `companies.csv`",
                "- `group-partner-profiles.json`",
                "- `group-partner-profiles.md`",
                "- `capture-errors.json`",
            ]
        )
        + "\n",
        encoding="utf-8",
    )


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    parser.add_argument("--index", default="YCCompany_production")
    parser.add_argument("--workers", type=int, default=12)
    parser.add_argument("--retries", type=int, default=2)
    parser.add_argument("--skip-page-enrichment", action="store_true")
    args = parser.parse_args()

    captured = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    args.output_dir.mkdir(parents=True, exist_ok=True)

    options = get_algolia_options()
    raw_companies = get_companies(options, args.index)
    print(f"Fetched {len(raw_companies)} companies from {args.index}", file=sys.stderr)

    enrichments: dict[str, dict[str, Any]] = {}
    errors: list[dict[str, str]] = []
    if not args.skip_page_enrichment:
        enrichments, errors = enrich_group_partners(raw_companies, args.workers, args.retries)

    companies = [
        normalize_company(hit, enrichments.get(str(hit.get("slug"))))
        for hit in raw_companies
    ]
    profiles = group_partner_profiles(companies)
    enriched_count = sum(1 for company in companies if company.get("group_partner"))

    write_json(args.output_dir / "companies.json", companies)
    write_csv(args.output_dir / "companies.csv", companies)
    write_json(args.output_dir / "group-partner-profiles.json", profiles)
    write_json(args.output_dir / "capture-errors.json", errors)
    write_profiles_markdown(
        args.output_dir / "group-partner-profiles.md",
        profiles,
        captured,
        len(companies),
        enriched_count,
        len(errors),
    )
    write_readme(
        args.output_dir / "README.md",
        captured,
        len(companies),
        enriched_count,
        len(profiles),
        len(errors),
    )
    print(
        f"Wrote {len(companies)} companies and {len(profiles)} group partner profiles to {args.output_dir}",
        file=sys.stderr,
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
