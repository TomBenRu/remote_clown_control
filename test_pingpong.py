import asyncio
import json
import time

import websockets

async def ping_pong(websocket, path):
    while True:
        # 接收客户端发来的消息
        message = await websocket.recv()
        print(f"收到消息: {message}")
        # 将消息发回客户端
        await websocket.send(message)

# start_server = websockets.serve(ping_pong, "localhost", 8765)
#
# asyncio.get_event_loop().run_until_complete(start_server)
# asyncio.get_event_loop().run_forever()

# 客户端
import asyncio
import websockets

import logging
logger = logging.getLogger('websockets')
logger.setLevel(logging.DEBUG)
logger.addHandler(logging.StreamHandler())


async def ping():
    async with websockets.connect("ws://localhost:8000/ws/notifications/",
                                  extra_headers={'Cookie': 'ws-cookie=clown-team-token'}, ping_interval=20) as websocket:
        while True:
            t0 = time.time()
            # 向服务器发送消息
            input('pause')
            await websocket.send(json.dumps({'was': 'geht'}))
#             接收服务器返回的消息
            message = await websocket.recv()
            print(f"收到消息: {message}")
            print(f'Delta: {time.time()-t0}')

asyncio.get_event_loop().run_until_complete(ping())
