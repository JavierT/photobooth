from tornado import websocket
import asyncio

class ActionsWebSocket(websocket.WebSocketHandler):

    NONE = 0
    NEW = 1
    BACK = 2
    NEXT = 3

    def open(self):
        try:
            print("WebSocket opened")

            self.application.new_collage.subscribe(self.send_new_pic)
            self.application.action.subscribe(self.send_action)
        except Exception as e:
            print('exception ', e)

    def check_origin(self, origin):
        return True

    def on_message(self, message):
        self.write_message(u"You said: " + message)

    def on_close(self):
        self.application.new_collage.unsubscribe(self.send_new_pic)
        self.application.action.unsubscribe(self.send_action)
        print("WebSocket closed")

    def write_message(self, *args, **kwargs):
        try:
            super().write_message(*args, **kwargs)
        except websocket.WebSocketClosedError:
            raise websocket.WebSocketClosedError

    def send_new_pic(self, message):
        print('writing action new pic')
        self.write_message(
            {
                'action': ActionsWebSocket.NEW,
                'img': message
            }
        )

    def send_action(self, action):
        try:
            #TODO: if the loops of the thread wont work
            # asyncio.set_event_loop(asyncio.new_event_loop())
            msg = {
                'action': action
            }
            print('writing action ', msg)
            self.write_message(msg)
        except Exception as e:
            print('exception send_action ', e)