# Copyright (C) 2022 The Qt Company Ltd.
# SPDX-License-Identifier: LicenseRef-Qt-Commercial OR BSD-3-Clause
import json

import websockets
from AsyncioPySide6 import AsyncioPySide6
from PySide6.QtCore import (Qt, QObject, Signal, Slot)
from PySide6.QtWidgets import (QApplication, QLabel, QMainWindow, QPushButton, QVBoxLayout, QWidget)

from PySide6.QtAsyncio import QAsyncioEventLoopPolicy

import asyncio
import signal
import sys


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        widget = QWidget()
        self.setCentralWidget(widget)

        layout = QVBoxLayout(widget)

        self.text = QLabel("The answer is 42.")
        layout.addWidget(self.text, alignment=Qt.AlignmentFlag.AlignCenter)

        async_trigger = QPushButton(text="What is the question?")
        async_trigger.clicked.connect(self.set_text)
        layout.addWidget(async_trigger, alignment=Qt.AlignmentFlag.AlignCenter)

    def set_text(self):
        async def async_start():
            uri = "ws://localhost:8000/ws/notifications/ "
            cookie = 'ws-cookie=clown-team-token'

            while True:
                try:
                    async with websockets.connect(uri, extra_headers={'Cookie': cookie}) as websocket:
                        while True:
                            name = input("What's your name? ")
                            data = json.dumps({'name': name})

                            await websocket.send(data)
                            print(f">>> {name}")

                            greeting = await websocket.recv()
                            print(f"<<< {greeting}")
                except websockets.exceptions.ConnectionClosed:
                    print("Connection closed. Reconnecting...")
                    await asyncio.sleep(5)
        AsyncioPySide6.runTask(async_start())


if __name__ == "__main__":
    app = QApplication(sys.argv)
    with AsyncioPySide6.use_asyncio():
        main_window = MainWindow()
        main_window.show()
        app.exec()
