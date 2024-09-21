import yaml
from random import randint
import aiohttp
import json
import pandas as pd

from basic_api.Logger_owner import Logger
from basic_api.Botapi_List import QQAPI_list



with open('_config.yml', 'r', encoding='utf-8') as f:
    config = yaml.load(f.read(), Loader=yaml.FullLoader)


class Answer_api:
    def __init__(self,websocket,Processed_data ):

        self.Logger = Logger()

        self.Processed_data = Processed_data
        self.websocket = websocket


        self.random_num = config["bot_api_settings"]["random_answer"]["random_num"]  # 随机回复概率
        self.test_config = config["test_settings"]["test_enable"]  # 测试模式
        self.judgement_api = config["bot_api_settings"]["answer_enable"]  # 开启api接口
        self.judgement_random = config['bot_api_settings']['random_answer']['enable']  # 开启随机回复
        self.judgement_dict_answer = config["bot_api_settings"]["dict_answer"]["enable"]  # 开启词典回复

    async def msg_random_answer(self):

        if self.Processed_data["judgement_at"] == True or self.Processed_data["message_group"] == None:  # 判断是否@机器人
            await self.msg_answer_api()

        elif self.Processed_data["judgement_at_other"] == True:  # 判断是否@其他人
            pass
        else:
            if self.judgement_random == True:  # 判断是否开启随机回复
                random_num = randint(1, 100)
                print("随机数：", random_num)
                if random_num <= self.random_num:  # 随机回复
                    await self.msg_answer_api()
                else:
                    pass
            else:
                await self.msg_answer_api()
        if self.test_config == True:  # 判断是否开启测试模式
            self.Logger.warning(f"测试模式(self.Processed_data)：{self.Processed_data}" +
                            "\n" +
                            f"随机数：{random_num}" if "random_num" in locals() else "")

    async def msg_answer_api(self):
        msg = self.Processed_data["message_content"]
        url = f"http://api.qingyunke.com/api.php?key=free&appid=0&msg={msg}"
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                result = await response.text()
                result_dict = json.loads(result)
                answer = result_dict["content"]
                await self.msg_send_api(answer)

    async def msg_dict_answer(self):  # 词典回复
        if self.judgement_dict_answer == False:  # 判断是否开启api接口
            return False
        content = self.Processed_data["message_content"]
        answer = await self.dict_find_answer(content)
        if answer == None:
            return False
        else:
            await self.msg_send_api(answer)
            return True

    async def dict_find_answer(self,target_text): # 词典寻找答案
        # 读取Excel文件
        df = pd.read_csv('./resource/dict_answer.csv', encoding='GBK')
        # 假设我们要在名为'column_name'的列中查找包含特定文字的单元格
        # 并且我们想要获取该列后面一列的数据
        column_name = 'question'  # 替换为你的列名
        next_column_name = df.columns[df.columns.get_loc(column_name) + 1]  # 获取后面一列的列名
        # 找到包含特定文字的行
        filtered_df = df[df[column_name].str.contains(target_text, na=False)]
        # 获取后面一列的数据
        answers = filtered_df[next_column_name].tolist()

        if len(answers) == 0:
            #print("没有找到答案")
            return None
        else:
            #print("词典回复：" + answers[0])
            return answers[0]

    async def msg_send_api(self,answer):
        if self.Processed_data["message_group"] == None:
            # 私聊消息
            user_id = self.Processed_data['message_sender_id']
            await QQAPI_list(self.websocket).send_message(user_id, answer)
            pass
        else:
            # 群聊消息
            group_id = self.Processed_data['message_group']
            await QQAPI_list(self.websocket).send_group_message(group_id, answer)


    async def msg_answer_all(self):
        if self.judgement_api == False:  # 判断是否开启api接口
            return
        if self.judgement_dict_answer == False:  # 判断是否开启api接口
            judgement_dict = None
        else:
            judgement_dict = await self.msg_dict_answer()
            #print(judgement_dict)

        if judgement_dict == None or judgement_dict == False:
            await self.msg_random_answer()
            #print("随机回复")
        else:
            pass




