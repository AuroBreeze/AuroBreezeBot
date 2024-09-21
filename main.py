import asyncio

from basic_api import Brief_introduction,Logger_owner,Websocket_bot

class Main:
    def __init__(self):
        self.log = Logger_owner.Logger()
        self.intro = Brief_introduction.Introductory_message().show_introduction()

    async def run(self):
        await Websocket_bot.Websocket_receiver().msg_raw_receiver()


if __name__ == '__main__':
    asyncio.run(Main().run())