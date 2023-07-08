# from channels.generic.websocket import WebsocketConsumer
# import json
# from asgiref.sync import async_to_sync

import json
from channels.generic.websocket import AsyncWebsocketConsumer

# consumers have method to connect a chatbox from client to server, process messages like saving the, and other methods


class Chatconsumer(AsyncWebsocketConsumer):
    async def connect(self):
        print("connect method running")
        self.chat_box_name = self.scope["url_route"]["kwargs"]["chat_box_name"]
        self.group_name = "chat_%s" % self.chat_box_name
        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.group_name, self.channel_name)

    # This function received messages from WebSocket.
    async def receive(self, text_data):
        print("Receive method running")
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]
        username = text_data_json["username"]

        await self.channel_layer.group_send(
            self.group_name,
            {
                "type": "chatbox_message",
                "message": message,
                "username": username,
            },
        )

    # Receive message from room group.
    async def chatbox_message(self, event):
        print("chatbox_message method running")
        message = event["message"]
        username = event["username"]
        # send message and username of sender to websocket
        await self.send(
            text_data=json.dumps(
                {
                    "message": message,
                    "username": username,
                }
            )
        )

# class ChatConsumer(WebsocketConsumer):
#     def connect(self):
#         self.room_name=self.scope['url_route']['kwargs']['room_code']
#         self.group_name=f'room_{self.room_name}'
#         async_to_sync(self.channel_layer)(
#             self.group_name,
#             self.channel_name
#         )
#         self.accept()
#         # async_to_sync(self.channel_layer.group_send)(
#         #     f'room_{self.room_name}',{
#         #         'value':json.dumps({'status':'online'})
#         #     }
#         # )
        
#         data={'type':'connected'}
#         self.send(text_data=json.dumps({
#             'payload':'connected'
#         }))
        
#     def receive(self, text_data):
#         data=json.loads(text_data)
#         payload={'message':data.get('message'),'sender':data.get('sender')}
        
#         async_to_sync(self.channel_layer.group_send)(
#             f'room_{self.room_name}',{
#                 'type':'send_message',
#                 'value':json.dumps(payload)
#             }
#         )
        
#         # return super().receive(text_data, bytes_data)
        
#     def disconnect(self, close_code):
#         pass
#         # return super().disconnect(code)
        
#     def send_message(self,text_data):
#         data=text_data.get('value')
        
#         self.send(text_data=json.dumps({
#             "payload": data
# #         }))
# import json
# from channels.generic.websocket import WebsocketConsumer
# from asgiref.sync import async_to_sync
# class Chating(WebsocketConsumer):
#     def connect(self):
#         self.room_name = self.scope['url_route']['kwargs']['room_name']
#         async_to_sync(self.channel_layer.group_add)(
#             self.room_name,self.channel_name
#         )
#         self.accept()
    
#     def disconnect(self, code):
#         async_to_sync(self.channel_layer.group_discard)(
#             self.room_name,self.channel_name
#         )
    
#     def receive(self, text_data=None, bytes_data=None):
#         data = json.loads(text_data)
#         msg = data["message"]
#         async_to_sync(self.channel_layer.group_send)(
#             self.room_name,{"type":"chat_messages","messages":msg ,"user": str(self.scope['user'])}
#         )
#     def chat_messages(self,event):
#         msg = event["messages"]
#         self.send(text_data=json.dumps({"message": msg,"user":event["user"]}))