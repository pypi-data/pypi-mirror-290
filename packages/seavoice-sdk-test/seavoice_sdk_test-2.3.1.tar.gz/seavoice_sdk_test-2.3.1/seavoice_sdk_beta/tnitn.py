#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import json
import asyncio

import websockets


class ITNClient:
    def __init__(self, itn_url: str, lang: str):
        if lang.lower().startswith("zh"):
            self.itn_url = f"{itn_url}/zh-TW"
        elif lang.lower().startswith("en"):
            self.itn_url = f"{itn_url}/en-XX"
        else:
            raise Exception(f"{lang} not supported for ITN.")
        self.websocket = None
        self.itn_results = asyncio.Queue()

    async def connect(self):
        self.websocket = await websockets.connect(self.itn_url)
        asyncio.create_task(self._receive_results())

    async def _receive_results(self):
        async for message in self.websocket:
            itn_result = json.loads(message)
            await self.itn_results.put(itn_result)

    async def send_text(self, text: str, is_final: bool, is_batch: bool = False):
        await self.websocket.send(json.dumps({"text": text, "is_final": is_final, "is_batch": is_batch}))

    async def get_oldest_itn_result(self) -> str:
        result = await asyncio.wait_for(self.itn_results.get(), timeout=int(os.getenv("ITN_TIMEOUT", 10)))
        return result

    async def close(self):
        await self.websocket.close()
