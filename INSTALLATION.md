# Impedance Agent installation for this EIS workspace

## Polarization-stage Bode plots — 9 October 2026

```powershell
./tools/impedance-agent/.venv/Scripts/python.exe skills/eis-analysis/scripts/plot_polarization_stages_impedance_agent.py --date 2026-10-09
```

The [new root-level collection](../../EIS_Polarization_Stages_PW_30mC_P1_PB_10mC_P3_2026-10-09_run01/index.md) covers **PW Amostra 0,1V 30mC P1** and **PB Amostra 0,3V 10mC P3**. It generates only the requested three polarization-stage magnitude views per specimen: b visits 01–04, c visits 04–10 and d visits 10–13. Initial 0 V stays black, other visits grey, and highlighted measured curves use dashed lines with points. All six canvases are 8 × 6 inches, exported as 600 dpi PNG plus PDF/SVG. Each specimen has a common scale across its three panels. PB insets expand b visits 03–04, c visits 04–07 and 09–10, and d visits 10–13; every main panel retains all thirteen curves.

Native `ImpedanceLoader` checks each converted input's descending sort/round trip, after which the exact signed original values are retained. The documented local extension of `PlotManager._plot_bode` accepts `experimental_data`, `unit_scale`, and `show_phase`; this uses the measurement frequencies and measured complex Z directly. `PolarizationPlotManager` supplies grouping, colors, sequence arrows, limits and inset layout. The default upstream Bode path remains compatible; measured plotting does not use a Lin-KK reconstruction or DRT time grid. The extension and the earlier Nyquist correction are recorded in [local-measured-bode.patch](local-measured-bode.patch).

Existing native circuit/Lin-KK tables are included with exact canonical-array verification and 52 CPE primary/narrower-band model/RMS/Q reconstruction checks. No new optimization, LLM/provider call or measurement upload is claimed. Stage-by-stage reports distinguish magnitude from real impedance, repeated-bias states from instantaneous voltage, and observations from switching hypotheses. The PW specimen here is **30mC**, rather than the earlier manuscript 10mC P1. Original exports and previous analyses remain unchanged. Each rerun allocates a new numbered output folder.

## All manuscript EIS spectra and zero-state diffusion comparison — 8 October 2026

```powershell
./tools/impedance-agent/.venv/Scripts/python.exe skills/eis-analysis/scripts/analyze_all_manuscript_eis_diffusion.py
```

The new [complete analysis collection](../../Images_Draft_manuscript/EIS_Analysis_PW_K50_P1_PB_K30_P3_2026-10-08/index.md) contains every EIS spectrum from PW Amostra 0,1V 10mC P1 (K/total Fe ≈ 0.50) and PB Amostra 0,3V 10mC P3 (≈ 0.30). It verifies the native loader and raw hashes, preserves and copies the 78 native RC/CPE/52 Lin-KK records with measured-array validation, and runs 78 fresh constrained native Warburg diagnostic fits. Its explicit local `FullEISPlotManager` extends the manuscript adapter with raw Bode/residual/component-check panels, using native PlotManager for measured Nyquist data. All 26 individual spectra have reports and equal-sized PNG/PDF/SVG figures; the final comparison keeps initial/after-positive/after-negative zero states distinct. D_K is not physically determined for those six states, and missing values are blank rather than zero. No LLM/provider calls; original measurements and prior output files remain unchanged.

## Diffusion and artifact review — 8 October 2026

```powershell
./tools/impedance-agent/.venv/Scripts/python.exe skills/eis-analysis/scripts/analyze_manuscript_diffusion_artifacts.py
```

Reviews all 26 saved visits of the two manuscript specimens, verifies native loader/TXT/XML input equality, and uses native ECMFitter for three constrained shared-Warburg diagnostic fits. Its explicit local `LowFrequencyPlotManager` extends the manuscript adapter with component-slope and array-roughness panels; Nyquist curves still use native PlotManager with measured data. No LLM calls or physical diffusion-coefficient assignment. Two additional 8 × 6 inch PNG/PDF/SVG figures, report and numerical provenance are saved in `Images_Draft_manuscript/`; earlier plots and fitted evidence remain unchanged. Missing per-point timing prevents a verified 28 s drift analysis; fitting Re(Z) alone does not establish a K diffusion coefficient.

## Current manuscript workflow — 7 October 2026

Additional requested PB figure: spectrum **13, 0 V after negative bias**, plotted alone with its own full signed limits for inset use. Reproduce without refitting or changing the six main figures:

```powershell
./tools/impedance-agent/.venv/Scripts/python.exe skills/eis-analysis/scripts/plot_pb13_manuscript_inset.py
```

It uses the same native plotting adapter and 8 × 6 inch canvas; PNG/PDF/SVG and its own provenance record are saved in `Images_Draft_manuscript/`.

Approved EIS formatting: all curves use dashed lines with point markers (circles for initial/forward visits; squares for reverse/after-sweep visits). Refresh only the four existing EIS figures, preserving analysis, C-AFM figures, dimensions and limits:

```powershell
./tools/impedance-agent/.venv/Scripts/python.exe skills/eis-analysis/scripts/redo_manuscript_with_impedance_agent.py --eis-plots-only
```

The user now requires impedance-agent for plotting and analysis. Run the fresh, numerical-only six-figure PW/PB workflow:

```powershell
./tools/impedance-agent/.venv/Scripts/python.exe skills/eis-analysis/scripts/redo_manuscript_with_impedance_agent.py
```

It reparses raw TXT/XML measurements, verifies native loader sorting, runs fresh `ECMFitter` RC/CPE fits and `LinKKFitter` diagnostics, and calls the native `PlotManager` through the local [manuscript adapter](impedance_agent/core/manuscript.py). There is no LLM provider configured at the current check; numerical-only mode makes no provider call. The standard CLI still uses `./impedance-agent.ps1`.

The explicit local adapter adds multi-spectrum overlays and raw finite-amplitude C-AFM plots with descriptive branch areas; it does not pretend C-AFM is impedance or claim upstream C-AFM model fitting. A plotting correction adds optional `experimental_data`/`unit_scale` arguments to `_plot_nyquist`: experimental points come from measured complex data, while a fallback `linkk_fit.Z_fit` is correctly labeled a Lin-KK reconstruction. These changes are saved in [local-manuscript.patch](local-manuscript.patch). Preserve this module and plotting correction when updating the checkout, alongside the import-time credentials patch below.

Current outputs: `Images_Draft_manuscript/`, exactly six requested figures in PNG/PDF/SVG, identical 8 × 6 inch canvases and 600 dpi PNG. Sample-specific linear ranges prevent curve compression; units and formatting match across PW/PB. Native fit objects, inputs, masks, seeds, residuals and provenance are under `agent_analysis/`. The previously rejected manuscript sets and their standalone plotting scripts were removed at the user's request; original measurements and saved selections were preserved.

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
