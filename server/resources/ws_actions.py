from tornado import websocket


class ActionsWebSocket(websocket.WebSocketHandler):
    def open(self):
        print("WebSocket opened")
        self.application.maj_gpio.subscribe(self.send_action)

    def check_origin(self, origin):
        return True

    def on_message(self, message):
        self.write_message(u"You said: " + message)

    def on_close(self):
        print("WebSocket closed")

    def send_action(message):
        pass