import random
import threading
import tkinter as tk
import asyncio


class ControlWindow(tk.Frame):

    def __init__(self, window=None):
        super().__init__()

        self.window = window

        tk.Button(window, text="Stop", command=self.stop).pack()
        tk.Button(window, text='Reaction...').pack()

        self.thread = None
        self.tasks = None
        self.flag = False
        self.run()
        # self.window.mainloop()

    def schedule_check(self):
        self.window.after(811, self.check)

    def check(self):
        if self.thread.is_alive():
            self.schedule_check()

    def run(self):
        self.thread = threading.Thread(target=asyncio.run, args=[self.main_runner()])
        self.thread.start()
        self.schedule_check()

    async def main_runner(self):
        queue = asyncio.Queue()
        self.tasks = [asyncio.create_task(self.code(queue)), asyncio.create_task(self.handle_code(queue))]

        try:
            await asyncio.gather(*self.tasks)
        except asyncio.CancelledError:
            print("Gather was cancelled and you can cleanup the things here")

    async def code(self, queue):
        while not self.flag:
            ran = random.randint(0, 5)
            queue.put_nowait(ran)
            await asyncio.sleep(1)

    async def handle_code(self, queue):
        while True:
            res = await queue.get()
            print(res)

    def stop(self):
        self.flag = True
        for task in self.tasks:
            task.cancel()

        self.thread.join()
        self.window.quit()


if __name__ == "__main__":
    root = tk.Tk()
    ControlWindow(root)
    root.mainloop()