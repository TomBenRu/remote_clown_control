import asyncio
import json
import time

import websockets
from PySide6.QtCore import QObject, QThread, Signal
from PySide6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QPushButton, QLabel, QApplication, QDialog,
                               QInputDialog, QLineEdit)
from PySide6.QtCore import Qt


# Step 1: Create a worker class
class Worker(QObject):
    finished = Signal()
    progress = Signal(int)

    question = Signal()
    answer = Signal(str)

    def __init__(self, parent: 'Window'):
        super().__init__()
        self.parent = parent

        self.parent.send_message.connect(lambda m: self.set_message(m))

        self.message = None

    def set_message(self, message: str):
        self.message = message

    async def hello(self):
        uri = "ws://localhost:8000/ws/notifications/ "
        cookie = 'ws-cookie=clown-team-token'

        while True:
            try:
                async with websockets.connect(uri, extra_headers={'Cookie': cookie}) as websocket:
                    print(f'{websocket.ping_interval=}')

                    while True:
                        # name = input("What's your name? ")

                        while not self.message:
                            continue
                        data = json.dumps({'Message': self.message})

                        await websocket.send(data)
                        print(f">>> {self.message}")
                        self.message = None

                        greeting = await websocket.recv()
                        print(f"<<< {greeting}")
                        print(f'{websocket.pings=}')
            except websockets.exceptions.ConnectionClosed:
                print("Connection closed. Reconnecting...")
                await asyncio.sleep(5)

    def run(self):
        asyncio.run(self.hello())

class Window(QMainWindow):

    send_message = Signal(str)
    def __init__(self):
        super().__init__()

        self.main_widget = QWidget()
        self.setCentralWidget(self.main_widget)
        self.layout = QVBoxLayout()
        self.layout.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        self.main_widget.setLayout(self.layout)

        self.bt_count = QPushButton('count')
        self.lb_count = QLabel('0')
        self.bt_multicount = QPushButton('multicount')
        self.lb_multicount = QLabel('0')
        self.bt_count.clicked.connect(lambda: self.lb_count.setText(str(int(self.lb_count.text()) + 1)))
        self.bt_multicount.clicked.connect(self.runLongTask)

        self.layout.addWidget(self.lb_count)
        self.layout.addWidget(self.bt_count)
        self.layout.addWidget(self.lb_multicount)
        self.layout.addWidget(self.bt_multicount)

    def runLongTask(self):
        # Step 2: Create a QThread object
        self.thread = QThread()
        # Step 3: Create a worker object
        self.worker = Worker(self)
        # Step 4: Move worker to the thread
        self.worker.moveToThread(self.thread)
        # Step 5: Connect signals and slots
        self.thread.started.connect(self.worker.run)
        self.worker.finished.connect(self.thread.quit)
        self.worker.finished.connect(self.worker.deleteLater)
        self.thread.finished.connect(self.thread.deleteLater)
        # self.worker.progress.connect(lambda o: self.report_progress(o))
        # Step 6: Start the thread
        self.thread.start()

        # Final resets
        self.bt_multicount.setEnabled(False)
        while True:
            message, ok = QInputDialog.getText(self, 'Message-Text', 'Message')
            if ok:
                self.send_message.emit(message)
            else:
                break

        self.thread.finished.connect(
            lambda: self.bt_multicount.setEnabled(True)
        )

    def report_progress(self, count: int):
        self.lb_multicount.setText(str(count))


if __name__ == '__main__':
    app = QApplication()
    main_window = Window()
    main_window.show()
    app.exec()
