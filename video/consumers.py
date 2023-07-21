from asgiref.sync import async_to_sync
from channels.generic.websocket import AsyncWebsocketConsumer
import asyncio
from .models import Video
from channels.db import database_sync_to_async
import aiofiles


class VideoConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.video_id = self.scope['url_route']['kwargs']['video_id']
        self.video = await self.get_video(self.video_id)

        if self.video:
            await self.accept()
        else:
            await self.close()

    async def receive(self, text_data):
        if text_data == 'start':
            await self.start_streaming()
        elif text_data == 'stop':
            await self.stop_streaming()

    async def start_streaming(self):
        try:
            file_path = self.video.file.path
            async with aiofiles.open(file_path, mode='rb') as file:
                while True:
                    chunk = await file.read(65536)  # 64KB
                    if not chunk:
                        break
                    await self.send(chunk)
                    # await self.send(text_data=chunk.decode('latin-1'))
                    await asyncio.sleep(0.1)  # Adjust sleep time as needed
        except FileNotFoundError:
            await self.close()

    async def stop_streaming(self):
        await self.close()

    @database_sync_to_async
    def get_video(self, video_id):
        return Video.objects.get(pk=video_id)
