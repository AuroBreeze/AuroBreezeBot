import yaml
from random import randint
import aiohttp
import json

from basic_api.Logger_owner import Logger
from basic_api.Botapi_List import QQAPI_list

with open('_config.yml', 'r', encoding='utf-8') as f:
    config = yaml.load(f.read(), Loader=yaml.FullLoader)


class answer_api:
    def __init__(self, websocket, Raw_data_queue):

        self.Logger = Logger()

        self.Raw_data = Raw_data_queue
        self.websocket = websocket
        self.random_num = config["bot_api_settings"]["random_answer"]["random_num"]
        self.test_config = config["test_settings"]["test_enable"]
        self.judgement_api = config["bot_api_settings"]["answer_enable"]
        self.judgement_random = config['bot_api_settings']['random_answer']['enable']

    async def message_answer_api(self):

        data_processing = await self.Raw_data.get()

        answer_api_dict = await self.message_answer_logic_dict(data_processing)
        if answer_api_dict == False:
            answer_api_basic = await self.message_answer_logic_basic(data_processing)
        elif answer_api_dict == None:
            pass
        else:
            pass

    async def message_answer_logic_basic(self, data_processing):
        if self.judgement_api == False:  # 判断是否开启api接口
            return False
        if data_processing["judgement_at"] == True or data_processing["message_group"] == None:  # 判断是否@机器人
            await self.message_getanswer_random(data_processing)

        elif data_processing["judgement_at_other"] == True:  # 判断是否@其他人
            pass
        else:
            if self.judgement_random == True:  # 判断是否开启随机回复
                random_num = randint(1, 100)
                # print("随机数：", random)
                if random_num <= self.random_num:  # 随机回复
                    await self.message_getanswer_random(data_processing)
                else:
                    pass
            else:
                await self.message_getanswer_random(data_processing)
        if self.test_config == True:  # 判断是否开启测试模式
            self.Logger.warning(f"测试模式(data_processing)：{data_processing}" +
                                "\n" +
                                f"随机数：{random_num}" if "random_num" in locals() else "")

    async def message_answer_logic_dict(self, data_processing):
        judgement_dict = await self.message_dict_api(data_processing)
        if judgement_dict == False:
            return False

    async def message_getanswer_random(self, data_processing):  # 获取api接口的回复并发送消息

        # print(data_processing)
        message = data_processing['message_content']
        url = f"http://api.qingyunke.com/api.php?key=free&appid=0&msg={message}"

        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                result = await response.text()
                answer = json.loads(result)['content']

            await self.message_sendanswer_api(data_processing, answer)

    async def message_dict_api(self, data_processing):  # 指令注册，及API函数注册
        content = data_processing['message_content']
        if content == "help":
            message = ("指令列表：\n"
                       "暂无\n")
            await self.message_sendanswer_api(data_processing, message)
            pass

        else:
            return False

    async def message_sendanswer_api(self, data, answer):  # 发送消息
        if data["message_group"] == None:
            # 私聊消息
            user_id = data['message_sender_id']
            await QQAPI_list(self.websocket).send_message(user_id, answer)
            pass
        else:
            # 群聊消息
            group_id = data['message_group']
            await QQAPI_list(self.websocket).send_group_message(group_id, answer)
            pass


