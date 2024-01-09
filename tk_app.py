import asyncio
import json
import threading
import tkinter as tk
import tkinter.ttk as ttk

import websockets


class MainWindow(ttk.Frame):
    def __init__(self, parent):
        super().__init__(master=parent)

        self.uri = "ws://localhost:8000/ws/notifications/ "
        self.cookie = 'ws-cookie=clown-team-token'

        self.lb_user_password = tk.Label(self, text='Username, Password')
        self.entry_username = tk.Entry(self)
        self.entry_password = tk.Entry(self)
        self.bt_commit = tk.Button(self, text='Commit', command=self.start_connect_thread)
        self.lb_chat = tk.Label(self, text='Chat')
        self.text_chat = tk.Text(self)
        self.lb_message = tk.Label(self, text='Message')
        self.entry_message = tk.Entry(self)
        self.bt_send = tk.Button(self, text='Send')

        self.lb_user_password.grid(row=0, column=0, padx=5, pady=5)
        self.entry_username.grid(row=0, column=1, padx=5, pady=5)
        self.entry_password.grid(row=0, column=2, padx=5, pady=5)
        self.bt_commit.grid(row=1, column=1, padx=5, pady=5)
        self.lb_chat.grid(row=2, column=0, padx=5, pady=5)
        self.text_chat.grid(row=2, column=1, padx=5, pady=5, columnspan=2)
        self.lb_message.grid(row=3, column=0, padx=5, pady=5)
        self.entry_message.grid(row=3, column=1, padx=5, pady=5)
        self.bt_send.grid(row=3, column=2, padx=5, pady=5)

        self.thread = None

    async def connect_to_server(self):
        try:
            async with websockets.connect(self.uri, extra_headers={'Cookie': self.cookie}) as ws:
                while True:
                    msg = input('Message: ')
                    await ws.send(json.dumps({'message': msg}))
                    print(await ws.recv())
        except Exception as e:
            print(f"Error connecting to server: {e}")

    def connect(self):
        asyncio.run(self.connect_to_server())

    def start_connect_thread(self):
        self.thread = threading.Thread(target=asyncio.run, args=[self.connect_to_server()])
        self.thread.run()

    # async def consumer_handler(self, websocket):
    #     async for message in websocket:
    #         await consumer(message)
    #
    # async def producer_handler(self, websocket):
    #     while True:
    #         message = await producer()
    #         await websocket.send(message)
    #
    # async def handler(self, websocket):
    #     await asyncio.gather(
    #         self.consumer_handler(websocket),
    #         self.producer_handler(websocket),
    #     )


if __name__ == '__main__':
    root = tk.Tk()
    root.title('ChatApp')
    MainWindow(root).pack()
    root.mainloop()
