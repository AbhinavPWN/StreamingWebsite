import json
import subprocess
import asyncio
from channels.generic.websocket import AsyncWebsocketConsumer


class VideoStreamConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        print('Video stream connected')
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = "chat_%s" % self.room_name

        # Join room group
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)

        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data):
        # Start the video streaming process
        video_file_path = 'media/video/Test.mp4'
        ffmpeg_command = f'ffmpeg -re -i {video_file_path} -f mpegts -codec:v mpeg1video -s 640x480 -b:v 800k -bf 0 -codec:a mp2 -b:a 128k -muxdelay 0.001 -'

        process = await asyncio.create_subprocess_shell(
            ffmpeg_command,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )

        while True:
            chunk = await process.stdout.read(4096)

            if len(chunk) == 0:
                break

            await self.send(chunk)

        await process.wait()

    # async def send(self, chunk):
    #     await self.send_bytes(chunk)
    async def send(self, text_data):
        await self.send_bytes(text_data.encode('utf-8'))

    async def chat_message(self, event):
        message = event["message"]

        # Send message to WebSocket
        await self.send(text_data=json.dumps({"message": message}))


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = "chat_%s" % self.room_name

        # Join room group
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)

        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]

        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name, {"type": "chat_message", "message": message}
        )

    # Receive message from room group
    async def chat_message(self, event):
        message = event["message"]

        # Send message to WebSocket
        await self.send(text_data=json.dumps({"message": message}))
