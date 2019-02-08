import asyncio

def run_coro(coro, client):
    fut = asyncio.run_coroutine_threadsafe(coro, client.loop)