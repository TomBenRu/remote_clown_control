#!/usr/bin/env python

import asyncio
import json

import websockets


async def hello():
    uri = "ws://localhost:8000/ws/notifications/ "
    cookie = 'ws-cookie=clown-team-token'
    async with websockets.connect(uri, extra_headers={'Cookie': cookie}) as websocket:
        name = input("What's your name? ")
        data = json.dumps({'name': name})

        await websocket.send(data)
        print(f">>> {name}")

        greeting = await websocket.recv()
        print(f"<<< {greeting}")

if __name__ == "__main__":
    asyncio.run(hello())
