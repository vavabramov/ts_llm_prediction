from contextlib import asynccontextmanager

import aiohttp


class AsyncHTTPClient:
    def __init__(self, headers):
        self.session = aiohttp.ClientSession(headers=headers)

    async def post(self, url, data, headers):
        async with self.session.get(url, json=data, headers=headers) as response:
            return await response.json(), response.status
        
    async def get(self, url, headers):
        async with self.session.get(url, headers=headers) as response:
            return await response.json(), response.status

    async def close(self):
        await self.session.close()


@asynccontextmanager
async def get_http_client(headers):
    client = AsyncHTTPClient(headers)
    try:
        yield client
    finally:
        await client.close()


async def make_post_request(client, url, headers, data) -> dict | None:
    response, status = await client.post(url, data, headers)
    if status == 200:
        return response
    return None

async def make_get_request(client, url, headers) -> dict | None:
    response, status = await client.get(url, headers)
    if status == 200:
        return response
    return None