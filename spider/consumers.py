from channels.generic.websocket import WebsocketConsumer
import json
from spider.ticket.using import main_main

class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.accept()

    def disconnect(self, close_code):
        pass

    def receive(self, text_data):
        main_main(text_data)
        # print("fp_dm"+str(fp_dm))
        # fp_dm = text_data_json['fp_dm']
        # self.send(text_data=json.dumps({
        #     'fp_dm': fp_dm,
        # }),)