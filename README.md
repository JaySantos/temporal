# Temporal Ingest Workflow Example

A small [Temporal](https://temporal.io) Python example that simulates a document-ingestion pipeline: a workflow sends text chunks one at a time to an `embed_chunk` activity, which stands in for a slow, unreliable embedding API.

## Files

| File | Purpose |
|------|---------|
| `workflows.py` | `IngestWorkflow`: calls `embed_chunk` for each chunk with a retry policy (3 attempts, exponential backoff). Chunks that still fail are collected instead of failing the whole workflow. Returns `{"embedded": [...], "failed": [...]}`. |
| `activities.py` | `embed_chunk`: simulated embedding call that fails randomly 70% of the time so you can watch retries happen. |
| `worker.py` | Starts a worker on the `ingest-queue` task queue that runs the workflow and activity. |
| `starter.py` | Starts one workflow run with chunks `chunk-1` … `chunk-5` and prints the result. |

Both `activities.py` and `workflows.py` also contain commented-out variants you can swap in:

- **activities.py**: a *standard* version that always succeeds, a *failure* version (the active one), and a *long-running* version that sleeps 2s per chunk, which is useful for testing what happens when you stop the worker mid-run.
- **workflows.py**: a *default* version with a retry policy where a failed chunk fails the workflow, and a *fault-tolerant* version (the active one).

## Prerequisites

- Python 3.10+
- The [Temporal CLI](https://docs.temporal.io/cli#install). On Windows, download `temporal.exe` and put it in this folder or on your `PATH`. The binary isn't committed to this repo because it's too large.

## Setup

```bash
python -m venv .venv
# Windows
.venv\Scripts\activate
# macOS / Linux
source .venv/bin/activate

pip install -r requirements.txt
```

## Running

Use three terminals, each with the virtual environment activated.

**1. Start a local Temporal dev server**

```bash
temporal server start-dev
```

This serves Temporal on `localhost:7233` and the Web UI on http://localhost:8233.

**2. Start the worker**

```bash
python worker.py
```

**3. Start a workflow**

```bash
python starter.py
```

The starter prints something like:

```
Result: {'embedded': ['embedding-of-chunk-2', 'embedding-of-chunk-4'], 'failed': ['chunk-1', 'chunk-3', 'chunk-5']}
```

Results vary between runs because the failures are random. The worker terminal logs each attempt, and the Web UI at http://localhost:8233 shows the workflow's event history, including each activity retry.

## Things to try

- Stop the worker (Ctrl+C) while a workflow is running, then start it again. The workflow picks up where it left off.
- Switch to the long-running activity to make that easier to see.
- Change the failure rate in `activities.py` or `maximum_attempts` in `workflows.py` and see how the results change.
