

import json # 把获取到的原始数据转换为json格式
import re # 正则表达式模块
import yaml # 读取配置文件模块

from basic_api.Logger_owner import Logger
from basic_api.Share_data import Processed_data
# 读取配置文件
with open('_config.yml', 'r', encoding='utf-8') as f:
    config = yaml.load(f.read(), Loader=yaml.FullLoader)


class Msg_process:

    def __init__(self,Raw_msg):
        self.test_config = config["test_settings"]["test_enable"]

        self.Logger = Logger()
        self.Raw_msg = Raw_msg
    # 处理消息队列中的数据,使用正则表达式进行解析，获取消息内容
    async def Message_processor(self):
        # logger.info(f"接收到消息:{message}")
        data = json.loads(self.Raw_msg)  # 把获取到的原始数据转换为json格式
        #print("1")

        # 正则表达式解析消息内容
        try:
            if data["post_type"]:  # 判断消息类型

                if data["post_type"] == "message":
                    message_type = data["message_type"]  # 判断私聊还是群聊

                    message_id = data["message_id"]  # 消息ID
                    message_sender_id = data["sender"]["user_id"]  # 消息发送者ID
                    message_name = data["sender"]["nickname"]  # 消息发送者昵称

                    message_content = data["raw_message"]
                    message_content_at = re.findall(r'\[CQ:(.*?),qq=(.*?),name=(.*?)\] (.*)', str(message_content))

                    judgement_at_other = False
                    QQbot_num = config["basic_settings"]["QQbot_account"]
                    if message_content_at != []:  # 判断是否为空
                        message_content_at = message_content_at[0]
                        if message_content_at[0] == "at" and message_content_at[1] == str(QQbot_num):  # 判断是否@机器人
                            message_content = message_content_at[3]
                            judgement_at = True
                        else:
                            message_content = message_content_at[3]
                            judgement_at = False
                            judgement_at_other = True
                    else:
                        judgement_at = False

                    if message_type == "group":
                        message_group = data["group_id"]
                    else:
                        message_group = None

                    message_data = {"message_id": message_id, "message_sender_id": message_sender_id,
                                    "message_name": message_name, "message_content": message_content,
                                    "message_group": message_group, "judgement_at": judgement_at,
                                    "judgement_at_other": judgement_at_other}


                    await Processed_data.put(message_data)  # 把解析后的消息内容放入队列



                elif data["post_type"] == "meta_event":
                    if self.test_config == True:
                        self.Logger.warning(f"原始消息内容为{data}")



            else:
                self.Logger.error(f"未知错误,消息类型为{data['post_type']}")
        except:
            if data["status"] == "ok":
                pass

            else:
                self.Logger.error(f"消息错误,消息内容为{self.Raw_msg}")

            # self.Logger.error(f"解析消息内容出错，消息内容为{message}")

        if self.test_config == True:  # 判断是否开启测试模式
            self.Logger.warning(f"测试模式开启，原始消息内容为{data}")
            self.Logger.warning(f"解析后的消息内容为{message_data}" if "message_data" in locals() else "")
        else:
            self.Logger.info(
                f"消息类型:{data['post_type']}，消息内容:{message_content}，消息发送者:{message_name}，消息ID:{message_id}，消息发送者ID:{message_sender_id}，消息群组ID:{message_group},是否@:{judgement_at},是否@其他人:{judgement_at_other}" if "message_content" in locals() else "")










