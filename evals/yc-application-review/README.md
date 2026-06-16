# YC Application Review Evals

JSONL fixtures for testing whether the `yc-partner` skill can review YC applications with useful, source-grounded, myth-safe feedback, separate written application strength from interview likelihood, and roughly calibrate text-only interview likelihood.

## Fixture Source

Most `fixtures.jsonl` rows are generated from public Get into YC company application pages by:

```sh
python3 scripts/capture_getintoyc_examples.py
```

The Lago successful-example row is generated from the Lago blog by:

```sh
python3 scripts/capture_lago_yc_application.py
```

The model-facing fields are `prompt` and `application_markdown`. The hidden `expected` object contains the historical acceptance outcome label from the public source.

Do not treat `unsuccessful` as a clean "did not deserve an interview" label. Some unsuccessful public applications may still have received an interview and then been rejected. A high score on an unsuccessful application can be a reasonable review if the application text has strong interview-worthy evidence.

## Runner

Run a local deterministic baseline over all fixtures. This checks response shape, leakage, source grounding, myth checks, context probes, and ghostwriting rules, and reports calibration metrics without failing on score separation unless `--strict-calibration` is passed:

```sh
python3 evals/yc-application-review/runner.py --mode heuristic
```

Run a live Codex candidate over a small stratified smoke sample:

```sh
python3 evals/yc-application-review/runner.py --mode codex --limit 4
```

The live candidate uses `codex exec` in read-only, ephemeral mode and asks for structured JSON matching `response.schema.json`. It does not read `.env` files and it does not receive the hidden `expected.known_outcome` label. It may read captured yc-partner resources in this repository to ground YC-specific guidance.

Run a normal-user output smoke test with the exact prompt shape `review my application` and no structured output schema:

```sh
python3 evals/yc-application-review/runner.py --mode codex-markdown --fixture-id getintoyc-dropbox
```

This mode checks whether the founder-facing Markdown stays compact and scannable: short generic section titles, dense bullet lists, `Office Hours`, a compact `Score` after the main risks/fixes, no old verbose section names, and a demo/founder-video ask when the application hinges on proof of work. It reports timeouts separately from parse failures because Markdown mode has no JSON parse step.

Receipts are written to:

```text
evals/yc-application-review/receipts/
```

## Scoring Intent

Successful examples should generally receive a higher interview-likelihood score than unsuccessful examples in aggregate, but this is only a diagnostic. Individual unsuccessful examples may still be strong interview cases. A good response:

- Reviews only the application text, not external knowledge of the company.
- Scores `application_strength` as the strength of the written case and `interview_likelihood` as the text-only odds of earning an interview. These can diverge when founder signal is strong but the company wedge, retention, switching reason, or source-grounded proof is still thin.
- Uses verdict bands conservatively: `likely` at `0.72+`, `borderline` above `0.40` and below `0.72`, and `unlikely` at `0.40` or below.
- Applies fixture-specific regression expectations for key public examples: GitLab should stay `likely`, Streamplate should stay `unlikely`, Buffer should stay `borderline`, and Dropbox should stay in a plausible but not overconfident interview-likelihood range.
- Separates concrete evidence from inference.
- Does not over-reward high usage or revenue without active/retained users, organic or efficient acquisition, monetization quality, clear denominators, distribution, defensibility, and market-path analysis.
- Treats impressive-sounding metrics skeptically when they are cumulative signups, vague "users", waitlists, GMV without take rate, pilots without payment, one-off or pass-through revenue, paid acquisition without CAC/payback/retention, or growth percentages without a baseline.
- Splits founder signal, company signal, and application-writing signal when they diverge.
- Names concrete facts that would move the score up or down instead of presenting the score as a prediction.
- Does not punish low revenue, pre-revenue, pre-product, or idea stage when the application shows user insight, founder-market fit, speed, domain expertise, or a strong next experiment.
- References captured reputable resources for YC-specific claims, myths, and problem-space risks.
- Uses sector and landscape context: adjacent YC companies, RFSes, common failure paths, substitutes, incumbents, sales cycle, marketplace liquidity, regulatory risk, buyer/user split, technical proof, or data advantage where relevant.
- Calls out missing specifics and vague answers directly.
- Gives directional improvements without ghostwriting final application copy.

These are calibration fixtures, not proof that historical successful applications are perfect examples or that historical unsuccessful applications have no merit.

## Pass Criteria

The runner always gates on:

- All candidate responses parse as JSON.
- `application_strength` and `interview_likelihood` are in the `0..1` range.
- Codex runs do not time out. Timeout failures are reported separately from parse failures.
- No hidden-label or historical-outcome leakage appears in the response.
- No obvious ghostwritten final application rewrite appears.
- Fixture-specific regression expectations pass for configured live Codex fixtures.
- Captured source grounding is present.
- Myth checks and context probes are present.
- The average deterministic response-quality score is at least `0.75`.
- No extreme score mismatch appears: historically successful applications below `0.25`, or historically unsuccessful applications above `0.95`.

Runs with `--strict-calibration` also gate on aggregate historical-outcome diagnostics:

- Successful examples score at least `0.12` higher on average than unsuccessful examples.
- Pairwise AUC is at least `0.65`.

The calibration metrics are deliberately soft. They test whether the reviewer is directionally skeptical and useful, not whether historical YC decisions are perfectly predictable from public application text.
