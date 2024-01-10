import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QPushButton, QTextEdit, QWidget
from PySide6.QtCore import Slot
import websocket
import ssl
import json
import threading


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        self.setWindowTitle("WebSocket Client")

        self.output = QTextEdit()
        self.output.setReadOnly(True)

        self.input = QTextEdit()

        self.send_button = QPushButton("Send")
        self.send_button.clicked.connect(self.send_message)

        self.close_button = QPushButton("Close Connection")
        self.close_button.clicked.connect(self.close_connection)

        layout = QVBoxLayout()
        layout.addWidget(self.output)
        layout.addWidget(self.input)
        layout.addWidget(self.send_button)
        layout.addWidget(self.close_button)

        container = QWidget()
        container.setLayout(layout)

        self.setCentralWidget(container)

        self.ws = websocket.WebSocketApp("ws://localhost:8000/ws/notifications/",
                                          on_message=self.on_message,
                                          on_error=self.on_error,
                                          on_close=self.on_close,
                                          header=['Cookie: ws-cookie=clown-team-token'])
        self.ws.on_open = self.on_open

        websocket.enableTrace(True)

        threading.Thread(target=self.ws.run_forever, kwargs={"sslopt": {"cert_reqs": ssl.CERT_NONE}}).start()

    def on_message(self, ws, message):
        self.output.append(f"Received: {message}")

    def on_error(self, ws, error):
        self.output.append(f"Error: {error}")

    def on_close(self, ws, close_status_code, close_msg):
        self.output.append(f"Connection closed with status code: {close_status_code} and message: {close_msg}")

    def on_open(self, ws):
        self.output.append("Connection opened")

    @Slot()
    def send_message(self):
        user_input = self.input.toPlainText()
        data = {"message": user_input}
        json_data = json.dumps(data)
        self.ws.send(json_data)
        self.input.clear()

    @Slot()
    def close_connection(self):
        if self.ws.sock and self.ws.sock.connected:
            self.ws.close()


if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    sys.exit(app.exec())
