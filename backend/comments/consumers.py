from channels.generic.websocket import AsyncWebsocketConsumer, WebsocketConsumer
import json

class CommentConsumer(WebsocketConsumer):

    def connect(self):
        # Called on connection.
        # To accept the connection call:
        self.accept()

        self.send(text_data=json.dumps({
            'status':'success',
            'type': 'Connection Stablished',
            'message': 'Hello world!'
        }))
        # Or accept the connection and specify a chosen subprotocol.
        # A list of subprotocols specified by the connecting client
        # will be available in self.scope['subprotocols']
        # await self.accept("subprotocol")
        # To reject the connection, call:
        # await self.close()

    # async def receive(self, text_data=None, bytes_data=None):
    #     # Called with either text_data or bytes_data for each frame
    #     # You can call:
    #     await self.send(text_data="Hello world!")
    #     # Or, to send a binary frame:
    #     await self.send(bytes_data="Hello world!")
    #     # Want to force-close the connection? Call:
    #     await self.close()
    #     # Or add a custom WebSocket error code!
    #     await self.close(code=4123)

    # async def disconnect(self, close_code):
    #     # Called when the socket close