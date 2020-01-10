from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
import json


class WorkConsumer(WebsocketConsumer):
    def connect(self):
        self.page_name = self.scope['url_route']['kwargs']['page_name']
        self.page_group_name = f'visitors_{self.page_name}'

        try:
            self.page_id = self.scope['url_route']['kwargs']['page_id']
            self.page_group_name += f'_{self.page_id}'
        except Exception:
            pass

        print(f'connect to group: {self.page_group_name}')

        async_to_sync(self.channel_layer.group_add)(
            self.page_group_name,
            self.channel_name
        )
        self.accept()

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            self.page_group_name,
            self.channel_name
        )


    def restart_message(self, event):
        message = event['text']

        print(f'message to group: {self.page_group_name}')

        self.send(text_data=json.dumps({
            'message': message
        }))
