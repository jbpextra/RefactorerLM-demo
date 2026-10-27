# RefactorerLM demo

A small Python checkout service for trying [RefactorerLM](https://github.com/jbpextra/RefactorerLM).
The intentional cyclic dependency between `orders.py` and `pricing.py` gives the tool
a concrete architectural smell to detect and refactor. Included tests provide
local regression checks for the service and any generated refactoring.

## Run the demo

1. Add an `OPENAI_API_KEY` repository secret under **Settings → Secrets and variables → Actions**.
2. Under **Settings → Actions → General → Workflow permissions**, enable
   **Allow GitHub Actions to create and approve pull requests**.
3. Open **Actions → RefactorerLM demo → Run workflow** and select `main`.

The workflow calls the standard reusable workflow at
`jbpextra/RefactorerLM/.github/workflows/refactorer.yml@main`.
It uses RefactorerLM's default Python version, models, and validation settings.
Runs make OpenAI API calls and can open a refactoring pull request after validation.
The configuration selects at most one cyclic dependency per run.

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

The example service and tests come from
[jbpextra/Refactorer-timing-experiment](https://github.com/jbpextra/Refactorer-timing-experiment/tree/d51786492a5ffcf3a91bfa5bde996043202f2bb3).
