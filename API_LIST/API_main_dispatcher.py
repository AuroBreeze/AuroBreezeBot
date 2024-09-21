
import asyncio

from API_LIST.basic_QQapi import Msg_process_api,Msg_answer_api
from basic_api.Share_data import Raw_data,Processed_data

class Msg_dispatcher:
    def __init__(self,websocket):
        self.websocket = websocket

    async def dispatch(self): # 接收消息并分发给相应的处理函数,此处只进行消息的简单处理
        while True:
            msg = await Raw_data.get()
            await Msg_process_api.Msg_process(msg).Message_processor()

    async def msg_dispatch_task(self): # 接收处理后的消息并进行处理，此处注册需要用到的处理函数
        while True:
            msg = await Processed_data.get()
            answer_msg = asyncio.create_task(Msg_answer_api.Answer_api(self.websocket,msg).msg_answer_all())



    async def dispatch_task_main(self):
        msg_dispatch_task_1 = asyncio.create_task(self.dispatch())
        msg_dispatch_task_2 = asyncio.create_task(self.msg_dispatch_task())





