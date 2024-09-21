import yaml
from basic_api.Logger_owner import Logger

with open('./_config.yml', 'r', encoding='utf-8') as f:
    config = yaml.load(f.read(), Loader=yaml.FullLoader)
'''

简单的入口输出，展示了配置文件的基本信息。

'''

class Introductory_message:
    def __init__(self):
        self.account = config['basic_settings']['QQbot_account']
        self.answer_judgement = config['bot_api_settings']['answer_enable']
        self.random_judgement = config['bot_api_settings']['random_answer']['enable']
        self.random_answer_num = config['bot_api_settings']['random_answer']['random_num']
        self.test_config = config['test_settings']['test_enable']


    def show_introduction(self):
        account = config['basic_settings']['QQbot_account']
        answer_judgement = config['bot_api_settings']['answer_enable']
        Logger().info("Starting...")
        Logger().info(f"QQbot账号：{account},自动回复功能：{answer_judgement}")
        if self.answer_judgement == True:
            Logger().info(f"随机回复功能：{self.random_judgement},随机回复设定数字：{self.random_answer_num}")

        Logger().warning(f"测试功能：{self.test_config}" + "\n")


if __name__ == '__main__':
    Introductory_message().show_introduction()
