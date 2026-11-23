# # DEFAULT WORKFLOWS.PY
# # workflows.py
# from datetime import timedelta

# from temporalio import workflow
# from temporalio.common import RetryPolicy

# # Workflow code runs in a sandbox; this lets us import the activity safely
# with workflow.unsafe.imports_passed_through():
#     from activities import embed_chunk


# @workflow.defn
# class IngestWorkflow:
#     @workflow.run
#     async def run(self, chunks: list[str]) -> list[str]:
#         embeddings = []
#         for chunk in chunks:
#             result = await workflow.execute_activity(
#                 embed_chunk,
#                 chunk,
#                 start_to_close_timeout=timedelta(seconds=10),
#                 retry_policy=RetryPolicy(
#                     initial_interval=timedelta(seconds=1),
#                     backoff_coefficient=2.0,
#                     maximum_interval=timedelta(seconds=10),
#                     maximum_attempts=3,
#                 ),
#             )
#             embeddings.append(result)
#         return embeddings


# # FAULT-TOLERANT WORKFLOWS.PY
# workflows.py
from datetime import timedelta

from temporalio import workflow
from temporalio.common import RetryPolicy
from temporalio.exceptions import ActivityError

with workflow.unsafe.imports_passed_through():
    from activities import embed_chunk


@workflow.defn
class IngestWorkflow:
    @workflow.run
    async def run(self, chunks: list[str]) -> dict:
        embedded, failed = [], []
        for chunk in chunks:
            try:
                result = await workflow.execute_activity(
                    embed_chunk,
                    chunk,
                    start_to_close_timeout=timedelta(seconds=10),
                    retry_policy=RetryPolicy(
                        initial_interval=timedelta(seconds=1),
                        backoff_coefficient=2.0,
                        maximum_interval=timedelta(seconds=10),
                        maximum_attempts=3,
                    ),
                )
                embedded.append(result)
            except ActivityError:
                workflow.logger.warning(f"Giving up on {chunk} for now")
                failed.append(chunk)
        return {"embedded": embedded, "failed": failed}
