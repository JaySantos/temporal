# # STANDARD ACTIVITIES.PY
# # activities.py
# from temporalio import activity


# @activity.defn
# async def embed_chunk(text: str) -> str:
#     # Stand-in for a real embedding API call (slow, can fail)
#     activity.logger.info(f"Embedding chunk: {text}")
#     return f"embedding-of-{text}"

# # FAILURE ACTIVITIES.PY
# activities.py
import random

from temporalio import activity


@activity.defn
async def embed_chunk(text: str) -> str:
    attempt = activity.info().attempt
    activity.logger.info(f"Embedding {text}, attempt {attempt}")
    if random.random() < 0.7:
        raise RuntimeError(f"Embedding API timeout on {text}")
    return f"embedding-of-{text}"


# # LONG TIME ACTIVITIES.PY (for worker shutdown tests)
# # activities.py
# import asyncio

# from temporalio import activity


# @activity.defn
# async def embed_chunk(text: str) -> str:
#     activity.logger.info(f"Embedding {text}")
#     await asyncio.sleep(2)  # slow embedding API
#     print(f"embedding-of-{text}")
#     return f"embedding-of-{text}"
