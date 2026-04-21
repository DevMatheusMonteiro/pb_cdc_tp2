from random import randint
import asyncio
from utils import print_timestamp

SENTINEL = None

async def extract(to_transform: asyncio.Queue, data: list[str]):
    for item in data:
        await asyncio.sleep(randint(1, 3) * 0.1)
        print_timestamp(f"Coletando -> {item}")
        await to_transform.put(item)
    await to_transform.put(SENTINEL)

async def transform(to_transform: asyncio.Queue, to_load: asyncio.Queue):
    while True:
        item = await to_transform.get()
        if item is SENTINEL:
            await to_load.put(SENTINEL)
            break
        await asyncio.sleep(randint(1, 3) * 0.1)
        transformed = item.upper()
        print_timestamp(f"Transformando -> {item} => {transformed}")
        await to_load.put(transformed)

async def load(to_load: asyncio.Queue):
    while True:
        item = await to_load.get()
        if item is SENTINEL:
            break
        await asyncio.sleep(randint(1, 3) * 0.1)
        print_timestamp(f"Enviando -> {item}")

async def main():
    data = ["item1", "item2", "item3", "item4", "item5"]

    to_transform = asyncio.Queue()
    to_load = asyncio.Queue()

    await asyncio.gather(
        extract(to_transform, data),
        transform(to_transform, to_load),
        load(to_load),
    )

asyncio.run(main())
