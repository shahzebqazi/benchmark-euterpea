# Run Provenance

Run provenance is the evidence trail that lets a score be debugged. A pass rate without provenance is only a claim; a run artifact with prompt, model, options, raw answer, verifier result, and source path is inspectable data.

## Raw Run Fields

Each raw run in `data/runs/` should preserve:

- schema version
- UTC run timestamp
- batch id
- sample index
- task id and task source path
- task metadata snapshot
- model name
- harness name
- Ollama base URL
- Ollama authentication source, if an authenticated host is used
- Ollama generation options
- exact prompt shown to the model
- raw model answer
- pass/fail result
- failure reason when failed
- latency and Ollama timing metrics when available

## Derived Report Fields

Each derived report row should preserve:

- task id
- model
- run count
- pass/fail counts
- pass rate
- answer distribution
- failure distribution
- latency average
- batch ids
- source run files
- model option samples

## Policy

Raw local runs are source data. Public reports and GitHub Pages output are derived artifacts. Derived reports may be curated by batch id, but they should never erase the fact that they came from raw run files.
