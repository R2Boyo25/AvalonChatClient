import websocket
import threading
import json

#websocket.enableTrace(True)

def formatMessage(type, **kwargs):
    e = {"type":type, **kwargs}

    return json.dumps(e)

def on_open(ws):
    ws.send(formatMessage('auth', token = "abcd1234"))
    def run(*args):
        while True:
            ws.send(formatMessage('message', message = input('> ')))

    threading.Thread(target=run).start()

def on_message(ws, message):
    print(message)

def on_close(ws, close_status_code, close_msg):
    print(">>>CLOSED<<<")

wsapp = websocket.WebSocketApp("ws://0.0.0.0:8090", on_open=on_open, on_message=on_message, on_close=on_close)
wsapp.run_forever()