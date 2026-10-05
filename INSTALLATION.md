# Impedance Agent installation for this EIS workspace

Installed on 2026-10-05 from [richinex/impedance-agent](https://github.com/richinex/impedance-agent), commit `0294d732c97f824a9cabb4945c523955b5d75d01`, package version **0.1.0**.

The repository is a Python CLI with numerical Lin-KK, equivalent-circuit and DRT fitters and optional LLM orchestration. Its Python package is installed editable in `.venv/`. The compatible Python 3.12.14 runtime and download cache are inside this workspace under `.cache/`; existing Python environments and EIS analyses are preserved.

## Run from the workspace root

```powershell
./impedance-agent.ps1 --help
./impedance-agent.ps1 version
./impedance-agent.ps1 list-providers
./impedance-agent.ps1 analyze --help
```

The launcher resolves the installed executable automatically. Activation is optional:

```powershell
./tools/impedance-agent/.venv/Scripts/Activate.ps1
impedance-agent --help
```

## Enable LLM analysis

Edit the local, git-ignored [.env](.env). Set either `DEEPSEEK_API_KEY`, or `OPENAI_API_KEY` together with `OPENAI_MODEL` set to a model available to your API account. Unused provider keys can remain empty. The upstream OpenAI model default is not used as a verified account/model selection here. Do not put credentials into chat, reports or version control.

The package can import and display CLI help/version without credentials. Its `analyze` command requires a configured provider. No provider request, paid API operation, or transmission of experimental measurements was made during installation. Credentials and provider access have not been verified.

Once a provider is configured, an upstream sample command is:

```powershell
./impedance-agent.ps1 analyze tools/impedance-agent/examples/data/randles_circuit.txt --provider deepseek --ecm tools/impedance-agent/examples/models/randles.yaml --output-path EIS_analysis/impedance_agent/example/analysis.json
```

This command uses the selected external LLM service. For OpenAI, specify `--provider openai` after configuring its key and model.

## Use with this project's files

The loader expects one spectrum per input file, with three columns in this order: frequency in Hz, signed Re(Z) in ohms, signed Im(Z) in ohms. It sorts points into descending frequency. The original 4294A TXT/XML exports have instrument headers and duplicate trace blocks; they require the existing audited project parser first. The canonical `spectra.csv` files also contain metadata columns and multiple acquisitions, so do not pass a whole canonical CSV directly as one spectrum.

Export each saved acquisition separately, preserving its specimen, DC bias, visit index and history in a sidecar or filename. Keep original exports unchanged, retain all signed values in raw views, and record any analysis mask. Generate scientific plots in PNG, PDF and SVG; the upstream CLI accepts a single `--plot-format` per invocation, so a project integration must explicitly supply all three formats without repeating paid analysis unnecessarily.

Use the installed package's outputs as numerical descriptions reviewed alongside `skills/eis-analysis/SKILL.md`, `EIS.md` and Maria_Luiza where relevant. DRT peaks, fit-quality labels and parameter correlations do not independently identify microscopic mechanisms. Passing Lin-KK on a chosen interval does not substitute for the project's missing amplitude/stationarity checks.

## Local compatibility patch

`impedance_agent/core/env.py` uses `Environment(validate=False)` for its global settings object. The original code required an API key at import time, including for `--help`, `version` and numerical-only imports. The `Environment` constructor still validates by default, and the CLI validates configured providers before analysis. No API-validation bypass or fabricated key is introduced.

The change is recorded in [local-compatibility.patch](local-compatibility.patch) and can be inspected with `git diff`. Preserve it when updating this checkout.

## Verification and reproducibility

- CLI help, version and analysis help worked with both provider keys empty.
- `uv pip check` confirmed compatible installed dependencies.
- Fifteen distinct selected upstream tests passed: seven loader tests, six Lin-KK tests, one synthetic Randles circuit fit and one synthetic DRT fit. These check installation behavior, not validity on the experimental PBA spectra.
- Early loader test attempts encountered Windows sandbox temporary-directory permissions; the seven loader tests were rerun successfully outside that sandbox. The original attempt is retained separately for provenance.

See [installation_record.json](installation_record.json), [resolved dependencies](installed-requirements.txt), and the XML reports under `verification/`.

To reinstall the same dependency versions after creating a Python 3.12 environment:

```powershell
uv --cache-dir .cache/uv pip install --python tools/impedance-agent/.venv/Scripts/python.exe -r tools/impedance-agent/installed-requirements.txt
uv --cache-dir .cache/uv pip check --python tools/impedance-agent/.venv/Scripts/python.exe
```

The editable checkout path in the dependency file is workspace-specific. Restore the saved compatibility patch if a fresh checkout is used.
