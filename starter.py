# starter.py
import asyncio
import uuid

from temporalio.client import Client

from workflows import IngestWorkflow


async def main():
    client = await Client.connect("localhost:7233")
    result = await client.execute_workflow(
        IngestWorkflow.run,
        [f"chunk-{i}" for i in range(1, 21)],
        id=f"ingest-{uuid.uuid4()}",
        task_queue="ingest-queue",
    )
    print("Result:", result)


if __name__ == "__main__":
    asyncio.run(main())
