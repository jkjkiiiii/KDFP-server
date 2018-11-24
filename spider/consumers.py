from channels.generic.websocket import WebsocketConsumer
import json
from spider.ticket import Before
from spider.ticket import later
import os 

class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.accept()

    def disconnect(self, close_code):
        pass

    
    def receive(self,text_data):
        jsons=json.loads(text_data)
        global invo
        global invo_later
        if jsons['command1']=='ask_no_verity':
            invo=Before.invoice()
            invo_later=later.confirm()
            invo_dict=invo.main(jsons)
            invo_dict['command1']='answer_no_verity'
            self.send(text_data=json.dumps(invo_dict))
        elif jsons['command1']=='ask_with_verity':
            invo_dict=invo_later.send_yz(invo.browser,jsons['verity_code'])
            if invo_dict['error']=='None':
                invo_dict['command1']='answer_snip'
                self.send(text_data=json.dumps(invo_dict))
            else:
                invo_dict['command1']='answer_no_verity'
                self.send(text_data=json.dumps(invo_dict))
        elif jsons['command1']=='ask_change_verity':
            verity_dict={}
            verity_dict['command1']='answer_with_verity'
            verity_dict['verity_code_link']=invo.pic()
            verity_dict['verity_code_word']=invo.color_yz()
            print(verity_dict)
            self.send(text_data=json.dumps(verity_dict))