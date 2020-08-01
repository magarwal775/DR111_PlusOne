import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from chat.models import Messages, Group
from accounts.models import User


class ChatConsumer(WebsocketConsumer):
    def __init__(self, *args, **kwargs):
        return super().__init__(*args, **kwargs)

    def fetch_messages(self, data):
        roomName = data["roomName"]
        messages = Messages.last_messages(roomName)
        content = {"command": "messages", "messages": self.messages_to_json(messages)}
        self.send_message(content)

    def new_message(self, data):
        author = data["from"]
        parent_user = User.objects.get(username=author)
        message = Messages.objects.create(
            parent_user=parent_user,
            group=Group.objects.get_or_create(group_id=data["roomName"])[0],
            message_text=data["message"],
        )
        content = {"command": "new_message", "message": self.message_to_json(message)}
        return self.send_chat_message(content)

    commands = {
        "fetch_messages": fetch_messages,
        "new_message": new_message,
    }

    def messages_to_json(self, messages):
        result = []
        for message in messages:
            result.append(self.message_to_json(message))
        return result

    def message_to_json(self, message):
        return {
            "author": message.parent_user.first_name,
            "author_profile_img": message.parent_user.profile_photo.url,
            "content": message.message_text,
            "timestamp": str(message.date_posted),
        }

    def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = "chat_%s" % self.room_name

        async_to_sync(self.channel_layer.group_add)(self.room_group_name, self.channel_name)

        self.accept()

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(self.room_group_name, self.channel_name)

    def receive(self, text_data):
        data = json.loads(text_data)
        self.commands[data["command"]](self, data)

    def chat_message(self, event):
        message = event["message"]
        self.send(text_data=json.dumps({"message": message, 'command': message['command']}))

    def send_chat_message(self, message):
        print("message sent")
        async_to_sync(self.channel_layer.group_send)(self.room_group_name, {"type": "chat_message", "message": message})

    def send_message(self, message):
        self.send(text_data=json.dumps(message))
