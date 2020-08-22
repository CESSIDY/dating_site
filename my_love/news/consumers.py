import asyncio
import time
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
import json
from .services import News


class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name
        self.user = self.scope["user"]
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )

        self.accept()
        self.chat_message({'message': 'Hay'})

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_names
        )

    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        username = text_data_json['username']

        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'username': username
            }
        )

    def chat_message(self, event):
        time.sleep(2.4)
        print(self.user)
        message = News(self.user).generate()
        #message = event['message']

        self.send(text_data=json.dumps({
            'event': "Send",
            'message': message,
        }))
        self.chat_message({'message': 'TEST!'})
