from random import randint
import asyncio
from utils import print_timestamp

async def extract(item: str):
    await asyncio.sleep(randint(1, 3) * 0.1)
    print_timestamp(f"Coletando -> {item}")
    return item

async def transform(item: str):
    await asyncio.sleep(randint(1, 3) * 0.1)
    transformed = item.upper()
    print_timestamp(f"Transformando -> {item} => {transformed}")
    return transformed

async def load(item: str):
    await asyncio.sleep(randint(1, 3) * 0.1)
    print_timestamp(f"Enviando -> {item}")

async def pipeline(item: str):
    extracted = await extract(item)
    transformed = await transform(extracted)
    await load(transformed)

async def main():
    data = ["item1", "item2", "item3", "item4", "item5"]
    tasks = [pipeline(item) for item in data]
    await asyncio.gather(*tasks)

asyncio.run(main())
