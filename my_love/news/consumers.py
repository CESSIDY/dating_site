import asyncio
import time
from django.contrib.auth.models import User
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
import json
from .services import News


class ChatConsumer(WebsocketConsumer):
    def connect(self):
        try:
            self.room_name = self.scope['user'].username
            if self.room_name:
                self.room_group_name = 'chat_%s' % self.room_name
                self.lang_code = self.scope['url_route']['kwargs']["lang_code"]
                self.user = self.scope['user']
                self.users_count = User.objects.count()
                async_to_sync(self.channel_layer.group_add)(
                    self.room_group_name,
                    self.channel_name
                )

                self.accept()
                self.chat_message({})
        except:
            pass

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
        time.sleep(self.time_depending_on_the_number_of_users())
        try:
            message = News(self.user, self.lang_code).generate()
        except:
            message = ''

        self.send(text_data=json.dumps({
            'event': "Send",
            'message': message,
        }))
        self.chat_message({})

    def time_depending_on_the_number_of_users(self):
        if User.objects.count() < 200:
            return (2000 / self.users_count)
        else:
            return 10
