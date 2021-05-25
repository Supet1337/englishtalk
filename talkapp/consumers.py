import datetime

from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
import json
from .models import *


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name
        # print(self.scope["user"])

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        room = text_data_json['room']
        time = text_data_json['time']
        # print(message)
        await self.save_chat(message, room,time)
        # print(text_data_json,self.scope["user"])

        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'username': self.scope["user"].first_name,
                'email': self.scope["user"].email,
                'time': time
            }
        )

    # Receive message from room group
    async def chat_message(self, event):
        message = event['message']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message,
            'time': event['time'],
            'email': event['email'],
            'user': event['username']
        }))

    @database_sync_to_async
    def save_chat(self, message, room, time):
        if 'AnonymousUser' != str(self.scope["user"]):
            r = ChatRoom.objects.get(name=room)
            ChatMessage.objects.create(room=r, user=self.scope["user"], message=message, timestamp=time)
        return True
