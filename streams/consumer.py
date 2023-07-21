import json

from channels.generic.websocket import AsyncWebsocketConsumer


# Defining the consumer class
def validate_data(parsed_data):
    # Perform validation on the received data
    if 'stream_id' not in parsed_data:
        raise ValueError('Invalid data: stream_id is required')


class StreamConsumer(AsyncWebsocketConsumer):
    print('WebSocket connected')

    def __init__(self, *args, **kwargs):
        super().__init__(args, kwargs)
        self.stream_group_name = 'video_stream_group'
        self.stream_id = 7

    async def connect(self):
        if not self.scope['user'].is_authenticated:
            await self.close(403)  # Unauthorized
            return

        self.stream_id = self.scope['url_route']['kwargs']['stream_id']
        self.stream_group_name = 'stream_%s' % self.stream_id

        # Join the stream group
        await self.channel_layer.group_add(
            self.stream_group_name,
            self.channel_name
        )

        # Connection accept
        await self.accept()

        # Notify others
        await self.channel_layer.group_send(self.stream_group_name, {
            'type': 'send_update',
            'message': f'User {self.scope["user"].username} has joined the stream.'
        })

    async def disconnect(self, close_code):
        print('WebSocket disconnected')
        # Leave the stream group
        await self.channel_layer.group_discard(
            self.stream_group_name,
            self.channel_name
        )

        # Notify others
        await self.channel_layer.group_send(self.stream_group_name, {
            'type': 'send_update',
            'message': f'User {self.scope["user"].username} has left the stream.'
        })

    async def receive(self, text_data=None, bytes_data=None):
        print('WebSocket message received')
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]

        # Send message to room group
        await self.channel_layer.group_send(
            self.stream_group_name, {"type": "chat_message", "message": message}
        )
        # parsed_data = json.loads(text_data)
        # validate_data(parsed_data)
        #
        # # Broadcast the data to other clients in the stream group
        # await self.channel_layer.group_send(self.stream_group_name, {
        #     'type': 'send_update',
        #     'data': parsed_data
        # })
        # Receive message from room group

    async def chat_message(self, event):
        message = event["message"]
        # Send message to WebSocket
        await self.send(text_data=json.dumps({"message": message}))

    async def send_update(self, event):
        # Access the data from the event parameters
        data = event['data']

        # Send the update to the client
        await self.send(text_data=json.dumps(data))
