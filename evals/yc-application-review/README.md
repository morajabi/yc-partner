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

## Scoring Intent

Successful examples should generally receive a higher interview-likelihood score than unsuccessful examples, but the evaluator should still reward useful critique. A good response:

- Reviews only the application text, not external knowledge of the company.
- Separates concrete evidence from inference.
- Notices traction, user insight, founder fit, speed, and clarity when present.
- Calls out missing specifics and vague answers directly.
- Gives directional improvements without ghostwriting final application copy.

These are calibration fixtures, not proof that historical successful applications are perfect examples or that historical unsuccessful applications have no merit.
