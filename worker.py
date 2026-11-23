# worker.py
import asyncio

from temporalio.client import Client
from temporalio.worker import Worker

from activities import embed_chunk
from workflows import IngestWorkflow


async def main():
    client = await Client.connect("localhost:7233")
    worker = Worker(
        client,
        task_queue="ingest-queue",
        workflows=[IngestWorkflow],
        activities=[embed_chunk],
    )
    print("Worker running... Ctrl+C to stop")
    await worker.run()


if __name__ == "__main__":
    asyncio.run(main())
