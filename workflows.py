# workflows.py
from datetime import timedelta

from temporalio import workflow

# Workflow code runs in a sandbox; this lets us import the activity safely
with workflow.unsafe.imports_passed_through():
    from activities import embed_chunk


@workflow.defn
class IngestWorkflow:
    @workflow.run
    async def run(self, chunks: list[str]) -> list[str]:
        embeddings = []
        for chunk in chunks:
            result = await workflow.execute_activity(
                embed_chunk,
                chunk,
                start_to_close_timeout=timedelta(seconds=10),
            )
            embeddings.append(result)
        return embeddings
