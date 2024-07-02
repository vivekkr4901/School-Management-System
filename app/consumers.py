import json
from channels.generic.websocket import AsyncWebsocketConsumer
from django.contrib.auth import get_user_model
from asgiref.sync import sync_to_async

User = get_user_model()

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.roomGroupName = "group_chat_gfg"
        self.user = self.scope["user"]

        await self.channel_layer.group_add(
            self.roomGroupName,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.roomGroupName,
            self.channel_name
        )

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]
        username = text_data_json["username"]
        recipient_username = text_data_json["recipient"]

        # Validate roles
        recipient_user = await sync_to_async(User.objects.get)(username=recipient_username) # type: ignore

        if not self._is_valid_recipient(recipient_user):
            return  # Invalid recipient, ignore message

        await self.channel_layer.group_send(
            self.roomGroupName, {
                "type": "sendMessage",
                "message": message,
                "username": username,
                "recipient": recipient_username,
            }
        )

    def _is_valid_recipient(self, recipient_user):
        if self.user.role == User.Role.STUDENT and recipient_user.role == User.Role.TEACHER:
            return True
        if self.user.role == User.Role.TEACHER and (recipient_user.role == User.Role.PRINCIPAL or recipient_user.role == User.Role.STUDENT):
            return True
        if self.user.role == User.Role.PRINCIPAL and recipient_user.role == User.Role.TEACHER:
            return True
        return False

    async def sendMessage(self, event):
        message = event["message"]
        username = event["username"]
        recipient = event["recipient"]
        await self.send(text_data=json.dumps({"message": message, "username": username, "recipient": recipient}))
