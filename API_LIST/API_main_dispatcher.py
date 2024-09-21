
import asyncio

from API_LIST.basic_QQapi import Msg_process_api
from basic_api.Share_data import Raw_data,Processed_data

class Msg_dispatcher:
    def __init__(self):
        pass
    async def dispatch(self):
        while True:
            msg = await Raw_data.get()
            #print(type(msg))
            await Msg_process_api.Msg_process(msg).Message_processor()

    async def msg_dispatch_task(self):
        while True:
            msg = await Processed_data.get()


    async def dispatch_task_main(self):
        msg_dispatch_task_1 = asyncio.create_task(self.dispatch())
        msg_dispatch_task_2 = asyncio.create_task(self.dispatch())

if __name__ == '__main__':
    msg_dispatcher = Msg_dispatcher()




