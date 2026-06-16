# YC Application Review Evals

JSONL fixtures for testing whether the `yc-partner` skill can review YC applications and roughly calibrate interview likelihood.

## Fixture Source

Most `fixtures.jsonl` rows are generated from public Get into YC company application pages by:

```sh
python3 scripts/capture_getintoyc_examples.py
```

The Lago successful-example row is generated from the Lago blog by:

```sh
python3 scripts/capture_lago_yc_application.py
```

The model-facing fields are `prompt` and `application_markdown`. The hidden `expected` object contains the historical outcome label from the public source.

## Runner

Run a local deterministic baseline over all fixtures. This checks response shape, leakage, and ghostwriting rules, and reports calibration metrics without failing on score separation unless `--strict-calibration` is passed:

```sh
python3 evals/yc-application-review/runner.py --mode heuristic
```

Run a live Codex candidate over a small stratified smoke sample:

```sh
python3 evals/yc-application-review/runner.py --mode codex --limit 4
```

The live candidate uses `codex exec` in read-only, ephemeral mode and asks for structured JSON matching `response.schema.json`. It does not read `.env` files and it does not receive the hidden `expected.known_outcome` label.

Receipts are written to:

```text
evals/yc-application-review/receipts/
```

## Scoring Intent

Successful examples should generally receive a higher interview-likelihood score than unsuccessful examples, but the evaluator should still reward useful critique. A good response:

- Reviews only the application text, not external knowledge of the company.
- Separates concrete evidence from inference.
- Notices traction, user insight, founder fit, speed, and clarity when present.
- Calls out missing specifics and vague answers directly.
- Gives directional improvements without ghostwriting final application copy.

These are calibration fixtures, not proof that historical successful applications are perfect examples or that historical unsuccessful applications have no merit.

## Pass Criteria

The runner always gates on:

- All candidate responses parse as JSON.
- `interview_likelihood` is in the `0..1` range.
- No hidden-label or historical-outcome leakage appears in the response.
- No obvious ghostwritten final application rewrite appears.
- The average deterministic response-quality score is at least `0.75`.

Live Codex candidate runs, and heuristic runs with `--strict-calibration`, also gate on:

- Successful examples score at least `0.12` higher on average than unsuccessful examples.
- Pairwise AUC is at least `0.65`.

The calibration metrics are deliberately soft. They test whether the reviewer is directionally skeptical and useful, not whether historical YC decisions are perfectly predictable from public application text.
