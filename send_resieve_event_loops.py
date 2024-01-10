import asyncio
import websockets


#Use this for debugging
SEND_TASK_NAME = "send_function"
RECV_TASK_NAME = "recv_function"
MAX_FAILURES = 3
WS_URL = "ws://localhost:8000/ws/notifications/"


async def send_data(websocket, data) -> bool:
    try:
        await websocket.send(data)
        return True
    except websockets.exceptions.ConnectionClosed as connection_closed:
        # Do closed connection handling
        return False
    except Exception as e:
        # Do generic error handling
        return False


async def send_task_func(websocket) -> bool:
    block = "SOME DATA TO SEND, COULD BE BINARY, JSON, ..., could be read/retrieved from somewhere else"
    if block:
        res = await send_data(websocket, block)
        if res:
            # Do some handling if needed
            pass
        else:
            # Do some handling if needed
            pass

    else:
        # Handle error case where you were unable to have data to send if applicable
        await asyncio.sleep(1)
        return False  # May not be an error case

    return True


async def recv_task_func(websocket) -> None:

    m = await websocket.recv()

    # Do something with the message, if receiving requires error handling then monitor the result in the loop
    return


async def send_and_receive_loop():
    async with websockets.connect(WS_URL, ping_timeout=None, close_timeout=1) as websocket:
        try:
            send_task = asyncio.create_task(send_task_func(websocket), name=SEND_TASK_NAME)
            recv_task = asyncio.create_task(recv_task_func(websocket), name=RECV_TASK_NAME)
            tasks = [send_task, recv_task]
            done_tasks, pending_tasks = await asyncio.wait(tasks, return_when=asyncio.FIRST_COMPLETED)

            failed_to_send_data = 0
            while True:
                tasks = []
                for done_task in done_tasks:
                    if done_task.get_name() == SEND_TASK_NAME:
                        if done_task.result is False:
                            failed_to_send_data += 1
                        else:
                            failed_to_send_data = 0

                        send_task = asyncio.create_task(send_task_func(websocket), name=SEND_TASK_NAME)
                        tasks.append(send_task)
                    elif done_task.get_name() == RECV_TASK_NAME:
                        recv_task = asyncio.create_task(recv_task_func(websocket), name=RECV_TASK_NAME)
                        tasks.append(recv_task)

                for pending_task in pending_tasks:
                    tasks.append(pending_task)

                if failed_to_send_data > MAX_FAILURES:
                    print("Aborting websocket")
                    break

                if len(tasks) > 0:
                    done_tasks, pending_tasks = await asyncio.wait(tasks, return_when=asyncio.FIRST_COMPLETED)
                else:
                    print("No tasks are going to be scheduled")
        except Exception as e:
            print(f"Exception while sending/receiving data through WS {e}.  Terminating WS connection")


        # If we are here, we need to cancel any pending tasks before the websocket gets closed
        for pending_task in pending_tasks:
            try:
                print(f"Cancelling pending tasks as we exited loop: {pending_task.get_name()}")
                pending_task.cancel()
            except Exception as e:
                print(f"Exception cancelling task: {e}")

        print("StreamClientNew::main_loop: Closing Websocket")
        await websocket.close()
        print("Done closing websocket")
        print("All done, exiting function")
        return

loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)
loop.run_until_complete(send_and_receive_loop())
#loop.close()
