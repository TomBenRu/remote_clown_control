import websocket
import ssl
import json
import threading

def on_message(ws, message):
    print(f"Received: {message}")

def on_error(ws, error):
    print(f"Error: {error}")

def on_close(ws, close_status_code, close_msg):
    print(f"Connection closed with status code: {close_status_code} and message: {close_msg}")

def on_open(ws):
    print("Connection opened")
    def run(*args):
        while True:
            user_input = input("Enter your message: ")
            data = {"message": user_input}
            json_data = json.dumps(data)
            ws.send(json_data)
    thread = threading.Thread(target=run)
    thread.start()

if __name__ == "__main__":
    cookie = 'ws-cookie=clown-team-token'
    headers = [f'Cookie: {cookie}']
    ws_address = "ws://localhost:8000/ws/notifications/"

    ws = websocket.WebSocketApp(ws_address,
                                 on_message=on_message,
                                 on_error=on_error,
                                 on_close=on_close,
                                 header=headers)
    ws.on_open = on_open

    # Enable debug mode
    websocket.enableTrace(True)

    ws.run_forever(sslopt={"cert_reqs": ssl.CERT_NONE})
