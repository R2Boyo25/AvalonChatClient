import websocket
import threading
import json
import curses
stdscr = curses.initscr()
curses.noecho()
curses.cbreak()
cols = curses.COLS
lins = curses.LINES

stdscr.clear()

wdt = int(cols/5) if (cols / 5) > 20 else 20

textWin = curses.newwin(lins-2, (cols-wdt)+1, 0, 0)
textWin.border('|', '|', '-', '-', '+', '+', '+', '+')
textBox = curses.newwin(lins-4, (cols-wdt)+1-2, 1, 1)
userWin = curses.newwin(int(lins/2)+1, wdt, 0, cols-wdt)
userWin.border('|', '|', '-', '-', '+', '+', '+', '+')
userBox = curses.newwin(int(lins/2)-1, wdt-3, 1, (cols-wdt)+2)
chanWin = curses.newwin(int(lins/2), wdt, int(lins/2), cols-wdt)
chanWin.border('|', '|', '-', '-', '+', '+', '+', '+')
chanBox = curses.newwin(int(lins/2)-2, wdt-3, int(lins/2)+1, (cols-wdt)+2)
entryWin = curses.newwin(3, (cols-wdt)+1, lins-3, 0)
entryWin.border('|', '|', '-', '-', '+', '+', '+', '+')
entryBox = curses.newwin(1, (cols-wdt)+1-2, lins-2, 1)


windows = [textWin, textBox, userBox, chanBox, chanWin, userWin, entryWin, entryBox]

username = ''

#websocket.enableTrace(True)

def formatMessage(type, **kwargs):
    e = {"type":type, **kwargs}

    return json.dumps(e)

def on_open(ws):
    global messages
    ws.send(formatMessage('auth', token = "abcd1234"))
    def run(*args):
        while True:
            curses.echo()
            gs = entryBox.getstr().decode()
            ws.send(formatMessage('message', message = gs))
            entryBox.clear()
            curses.noecho()
            messages.append({'author':username, 'message':gs})#textBox.addstr(username + ': ' + gs+ '\n')
            textBox.clear()
            for i in messages:
                try:
                    textBox.addstr(i['author'] + ': ' + i['message']+ '\n')
                except:
                    messages.pop(0)
                    textBox.clear()
                    for i in messages:
                        try:
                            textBox.addstr(i['author'] + ': ' + i['message']+ '\n')
                        except:
                            messages.pop(0)
            for i in windows:
                i.refresh()


    threading.Thread(target=run).start()

users = []
channels = []
messages=[]

def on_message(ws, message):
    global username
    global channels
    global messages
    message = json.loads(message)
    if message['type'] == 'message':
        messages.append(message)
        #try:
        #    textBox.addstr(message['author'] + ': ' + message['message']+ '\n')
    elif message['type'] == 'auth':
        username = message['username']
        if message['username'] not in i:
            users.append(message['username'])
    elif message['type'] == 'user_list':
        for i in message['users']:
            if i not in users:
                users.append(i)
    elif message['type'] == 'channel_list':
        for i in message['channels']:
            if i not in channels:
                channels.append(i)
    elif message['type'] == 'join':
        users.append(message['username'])
    elif message['type'] == 'leave':
        del users[users.index(message['username'])]
    else:
        textBox.addstr('Unknown message: ' + message + '\n')

    textBox.clear()
    for i in messages:
        try:
            textBox.addstr(i['author'] + ': ' + i['message']+ '\n')
        except:
            messages.pop(0)
            textBox.clear()
            for i in messages:
                try:
                    textBox.addstr(i['author'] + ': ' + i['message']+ '\n')
                except:
                    messages.pop(0)

    userBox.clear()
    userBox.addstr(username + '\n')
    for i in users:
        if i !='':
            userBox.addstr(i+'\n')
    
    chanBox.clear()
    for i in channels:
        if i !='':
            chanBox.addstr(i+'\n')

    for i in windows:
        i.refresh()

def on_close(ws, close_status_code, close_msg):
    print(">>>CLOSED<<<")
    curses.nocbreak()
    curses.echo()
    curses.endwin()


wsapp = websocket.WebSocketApp("ws://0.0.0.0:8090", on_open=on_open, on_message=on_message, on_close=on_close)
wsapp.run_forever()
