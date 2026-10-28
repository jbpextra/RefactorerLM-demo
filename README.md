# RefactorerLM demo

Small Python examples for trying [RefactorerLM](https://github.com/jbpextra/RefactorerLM).
The source contains four intentional architectural smells:

- **Cyclic Dependency (checkout)**: `orders.py` and `pricing.py` import one another.
- **Cyclic Dependency (bundles)**: `bundle_demo/bundle.py` and
  `bundle_demo/manifest.py` import one another to validate names and format manifests.
- **Potential Redundant Abstractions (coordinates)**: `app/screen_coordinates.py` and
  `app/print_coordinates.py` duplicate the same `normalise`, `clamp`, and `render`
  functions. Both implementations are used by the public coordinate-label API.
- **Potential Redundant Abstractions (field parsing)**: `field_imports/paste_fields.py`
  and `field_imports/upload_fields.py` duplicate the parser used by the paste and
  upload entry points.

Included tests provide local regression checks for all examples and any generated
refactoring.

## Run the demo

1. Add an `OPENAI_API_KEY` repository secret under **Settings → Secrets and variables → Actions**.
2. Under **Settings → Actions → General → Workflow permissions**, enable
   **Allow GitHub Actions to create and approve pull requests**.
3. Open **Actions → RefactorerLM demo → Run workflow** and select `main`.

The workflow calls the standard reusable workflow at
`jbpextra/RefactorerLM/.github/workflows/refactorer.yml@main`.
It uses RefactorerLM's default Python version, models, and validation settings.
Before refactoring, it installs `requirements-dev.txt`, including pytest, so the
correctness filter can run the demo's regression tests.
Runs make OpenAI API calls and can open a refactoring pull request after validation.
The configuration selects both smell types without a proposal limit. The workflow
uses RefactorerLM's default parallelism.

This repository has a single manually triggered workflow. It contains no timing
campaign, setup probe, or experiment-specific inputs.

RefactorerLM records attempted smells on `refactor/*` branches. If a subsequent
run selects no smells, check those branches and the previous run's summary.

## Run locally

Use Python 3.11 or newer:

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements-dev.txt
python -m pytest -q
```

The application uses only the Python standard library:

```python
from checkout import render_receipt

print(render_receipt("R-1", [("pen", 2, 125)], member=True))
```

Amounts are integer cents. Member orders receive a 10% discount, and shipping is
free when the discounted subtotal reaches 5,000 cents. Empty orders have zero
totals. Receipt lines retain their input order and duplicates.

The coordinate-label example clamps each coordinate to `[0, limit]` and formats
the result as `"x,y"`. Both routes intentionally do the same work:

```python
from app.api import print_label, screen_label

assert screen_label(-2, 12, 9) == "0,9"
assert print_label(-2, 12, 9) == "0,9"
```

The bundle example exposes `bundle_demo.api.build_bundle` and `preview_manifest`
for ordered payload bundles with validated names and checksums. The field-parsing
example exposes `field_imports.api.parse_upload` and `parse_paste` for
semicolon-separated records with escaped separators and backslashes.

The checkout service and its tests come from
[jbpextra/Refactorer-timing-experiment](https://github.com/jbpextra/Refactorer-timing-experiment/tree/d51786492a5ffcf3a91bfa5bde996043202f2bb3).
The coordinate-label source and tests are copied unchanged from case **E-RA-01**
in the [RefactorerLM reproduction package](https://github.com/jbpextra/refactorerlm-reproduction-package/tree/54d74fd884c889baf4a2a54bbf8f4d238940b04b/cases/evaluation/E-RA-01/original).
The bundle and field-parsing source and tests reuse cases
[E-CD-01](https://github.com/jbpextra/refactorerlm-reproduction-package/tree/54d74fd884c889baf4a2a54bbf8f4d238940b04b/cases/evaluation/E-CD-01/original)
and [E-RA-02](https://github.com/jbpextra/refactorerlm-reproduction-package/tree/54d74fd884c889baf4a2a54bbf8f4d238940b04b/cases/evaluation/E-RA-02/original),
with package imports renamed to keep the examples independent.
