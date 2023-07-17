import asyncio
import time
import zlib
from abc import ABC, abstractmethod
from typing import Dict

from aiohttp import ClientWebSocketResponse, ClientSession, web, WSMessage

from .cert import Cert
from .interface import AsyncRunnable
from .schema.wsHandler import EventHandler
from ..handle import msgHandler

from .log import logger

log = logger

__name__ = "Khl.receiver"

API = 'https://www.kaiheila.cn/api/v3'


class Receiver(AsyncRunnable, ABC):
    """
    1. receive raw data from khl server
    2. decrypt & parse raw data into pkg
    3. put pkg into the pkg_queue() for others to use
    """

    @property
    def type(self) -> str:
        """the network type used by the receiver"""
        raise NotImplementedError

    @abstractmethod
    async def start(self):
        """run self"""
        raise NotImplementedError


class WebsocketReceiver(Receiver):
    """receive data in websocket mode"""

    def __init__(self, cert: Cert, compress: bool):
        super().__init__()
        self._cert = cert
        self.compress = compress

        self._NEWEST_SN = 0
        self._RAW_GATEWAY = ''

    @property
    def type(self) -> str:
        return 'websocket'

    async def heartbeat(self, ws_conn: ClientWebSocketResponse):
        """khl customized heartbeat scheme"""
        while True:
            try:
                await asyncio.sleep(26)
                await ws_conn.send_json({'s': 2, 'sn': self._NEWEST_SN})
            except ConnectionResetError:
                return
            except Exception as e:
                log.exception('error raised during websocket heartbeat',
                              exc_info=e)

    async def _get_gateway(self, cs: ClientSession):
        headers = {
            'Authorization': f'Bot {self._cert.token}',
            'Content-type': 'application/json'
        }
        params = {'compress': 1 if self.compress else 0}
        async with cs.get(f"{API}/gateway/index",
                          headers=headers,
                          params=params) as res:
            res_json = await res.json()
            if res_json['code'] != 0:
                log.error(f'getting gateway: {res_json}')
                return

            self._RAW_GATEWAY = res_json['data']['url']

    async def _connect_gateway_and_handle_msg(self, cs: ClientSession):
        async with cs.ws_connect(self._RAW_GATEWAY) as ws_conn:
            asyncio.ensure_future(self.heartbeat(ws_conn), loop=self.loop)

            log.info('[ init ] Khl模块启动')
            try:
                async for raw in ws_conn:
                    raw: WSMessage
                    await self._handle_raw(raw)
            except Exception:
                log.exception(
                    'error raised during websocket receive, reconnect automatically'
                )

    async def start(self):
        async with ClientSession(loop=self.loop) as cs:
            while True:
                await self._get_gateway(cs)
                await self._connect_gateway_and_handle_msg(cs)

    async def _handle_raw(self, raw: WSMessage):
        try:
            data = raw.data
            data = zlib.decompress(data) if self.compress else data
            pkg: Dict = self._cert.decode_raw(data)
            log.debug(f'upcoming raw: {pkg}')
            pkg_handled = EventHandler(**pkg)
            if pkg_handled.s != 0:
                return
            self._NEWEST_SN = pkg_handled.sn
            data_ = pkg_handled.d
            type = int(data_.type)  # 消息类型
            channel_type = data_.channel_type  # 消息通道类型
            user_name = data_.extra.author.username  # 用户名
            identify_num = data_.extra.author.identify_num  # 用户名的认证数字
            guild_id = data_.extra.guild_id  # 服务器ID
            content = data_.content  # 消息内容
            msg_id = data_.msg_id  # 消息ID
            msg_timestamp = time.strftime("%m-%d %H:%M:%S", time.localtime(data_.msg_timestamp / 1000))  # 发送时间
            if channel_type == "GROUP":
                msg = f"{msg_timestamp} 服务器({guild_id})接收到消息: 通道类型: {channel_type}, 消息类型: {type}, 发送者: {user_name}#{identify_num}, 内容: \"{content}\" - {msg_id}"
            elif channel_type == "PERSON":
                msg = f"{msg_timestamp} 接收到@{user_name}#{identify_num}私信消息: 通道类型: {channel_type}, 消息类型: {type}, 内容: \"{content}\" - {msg_id}"
            log.info(msg)
            # 这里后面接接口
            await msgHandler(pkg['d']).handle()
        except Exception as e:
            log.exception(e)
