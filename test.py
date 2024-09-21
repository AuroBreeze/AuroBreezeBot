import asyncio

import websockets

url = "ws://localhost:8080"

async def hello():
    try:
    #async with websockets.connect(url) as websocket:
        #await websocket.send("Hello, world!")
        print("1")
    except Exception as e:
        print(f"Error: {e}")

async def main():
    await hello()

if __name__ == "__main__":
    asyncio.run(main())