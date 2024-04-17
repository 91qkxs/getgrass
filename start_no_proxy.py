import asyncio
import json
import logging
import random
import ssl
import time
import uuid

import websockets
from faker import Faker
from websockets_proxy import Proxy, proxy_connect

# 配置日志级别
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# 存储已连接的 WebSocket 对象的列表
connected_websockets = []


async def send_message(websocket, message):
    """
    发送消息到 WebSocket 服务器
    """
    message_str = json.dumps(message)
    logging.info(f"Sending message: {message_str}")
    await websocket.send(message_str)


async def receive_message(websocket):
    """
    接收 WebSocket 服务器的消息
    """
    response = await websocket.recv()
    logging.info(f"Received response: {response}")
    return json.loads(response)


async def authenticate(websocket, auth_id, device_id, user_id, agent):
    """
    发送认证消息到 WebSocket 服务器
    """
    auth_message = {
        "id": auth_id,
        "origin_action": "AUTH",
        "result": {
            "browser_id": device_id,
            "user_id": user_id,
            "user_agent": agent,
            "timestamp": int(time.time()),
            "device_type": "extension",
            "version": "3.3.2"
        }
    }
    await send_message(websocket, auth_message)


async def run_websocket_logic(websocket, user_id, device_id, agent):
    try:
        # 第1步：接收平台auth请求响应
        auth_response = await receive_message(websocket)

        await asyncio.sleep(random.randint(10, 20) / 10)
        # 第3步：进行auth请求
        await authenticate(websocket, auth_response["id"], device_id, user_id, agent)
        await asyncio.sleep(20)

        """
        业务逻辑处理
        """
        # 第2步：发送ping请求
        message = {
            "id": str(uuid.uuid4()),
            "version": "1.0.0",
            "action": "PING",
            "data": {}
        }
        await send_message(websocket, message)

        while True:
            # 第4步：得到认证成功请求响应
            pong_response = await receive_message(websocket)
            await asyncio.sleep(random.randint(1, 9) / 10)
            pong_message = {
                "id": pong_response["id"],
                "origin_action": "PONG"
            }
            # 第5步：回复平台已得到认证成功请求响应
            await send_message(websocket, pong_message)

            await asyncio.sleep(random.randint(180, 250) / 10)

            ping_message = {
                "id": str(uuid.uuid4()),
                "version": "1.0.0",
                "action": "PING",
                "data": {}
            }
            # 第6步：发送心跳包
            await send_message(websocket, ping_message)
            await asyncio.sleep(random.randint(1, 9) / 10)

    except websockets.exceptions.ConnectionClosed as e:
        logging.error(f"Connection closed unexpectedly: {e}")
    finally:
        await websocket.close()  # 确保关闭连接


async def run_with_proxy(uri, ssl_context, custom_headers, device_id, user_id, proxy):
    """
    使用代理运行 WebSocket 连接
    """
    try:
        async with proxy_connect(uri, ssl=ssl_context, extra_headers=custom_headers, proxy=proxy,
                                 proxy_conn_timeout=10) as websocket_p:
            # 将连接加入到已连接的 WebSocket 列表中
            connected_websockets.append(websocket_p)
            await run_websocket_logic(websocket_p, user_id, device_id)
    except Exception as e:
        logging.error(f"Error occurred with proxy {proxy.proxy_host}: {proxy.proxy_port} {e}")


async def run_without_proxy(uri, ssl_context, agent, device_id, user_id):
    """
    不使用代理运行 WebSocket 连接
    """
    try:
        async with websockets.connect(uri, ssl=ssl_context, extra_headers={"User-Agent": agent}) as websocket:
            # 将连接加入到已连接的 WebSocket 列表中
            connected_websockets.append(websocket)
            await run_websocket_logic(websocket, user_id, device_id, agent)
    except Exception as e:
        logging.error(f"Error occurred without proxy  {e}")


async def close_connected_websockets():
    """
    关闭所有已连接的 WebSocket 连接
    """
    # 等待一段时间，确保之前的连接已经完全关闭
    await asyncio.sleep(5)
    for ws in connected_websockets:
        await ws.close()


async def main(user_id):
    """
    主函数
    """
    # 在运行主函数之前确保关闭之前的所有 WebSocket 连接
    await close_connected_websockets()

    device_id = str(uuid.uuid4())
    logging.info(device_id)
    uri_options = ["wss://proxy.wynd.network:4650/", "wss://proxy.wynd.network:4444"]
    agent = Faker().chrome()

    ssl_context = ssl.create_default_context()
    ssl_context.check_hostname = False
    ssl_context.verify_mode = ssl.CERT_NONE
    await run_without_proxy(random.choice(uri_options), ssl_context, agent, device_id, user_id)

if __name__ == "__main__":
    user_id = '5b62d235-273c-4707-85df-9bcca26a5306'
    asyncio.run(main(user_id))
