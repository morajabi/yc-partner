# YC Company Directory

- Type: directory dataset
- Status: public YC directory capture
- URL: https://www.ycombinator.com/companies
- Captured: 2026-06-16
- Method: public YC directory Algolia index plus public company page `primary_group_partner` fields

## Summary

- `companies.json` contains 5960 parsed public company directory entries.
- Each company includes name, batch, YC directory URL, group partner when published, industry, sectors, tags, one-liner, status, stage, regions, location, team size, and website.
- `companies.csv` is a compact spreadsheet-friendly export of company, batch, group partner, industry, sectors, tags, URL, one-liner, status, and stage.
- `group-partner-profiles.json` and `group-partner-profiles.md` summarize 17 group partners from 2789 companies with published primary group partner values.
- Company page enrichment errors: 0. See `capture-errors.json` when non-empty.
- Partner areas are inferred from assigned companies in the public directory, not from stated YC partner preferences.
- Older company pages often have no `primary_group_partner`; those companies remain in the directory with `group_partner: null`.

## Content

- `companies.json`
- `companies.csv`
- `group-partner-profiles.json`
- `group-partner-profiles.md`
- `capture-errors.json`
