import asyncio
from contextlib import suppress


async def process(i):
    await asyncio.sleep(i)
    print(i)
    with suppress(Exception):
        if i == 1:
            raise Exception(i)
    return i


async def run():
    ret = await asyncio.gather(*(process(i) for i in range(5)), return_exceptions=True)
    print(ret)
    print(any(map(lambda x: isinstance(x, Exception), ret)))
    print(all(map(lambda x: isinstance(x, Exception), ret)))

asyncio.run(run())
