"""implementation of bot"""
import asyncio
import warnings
import json
import os
from pathlib import Path
from typing import Dict, Callable, List, Optional, Union, Coroutine, IO, Any

from .. import AsyncRunnable  # interfaces
from .. import Cert, HTTPRequester, WebsocketReceiver, Gateway, Client  # net related
from .. import MessageTypes, EventTypes, SlowModeTypes, SoftwareTypes  # types
from .. import User, Channel, PublicChannel, Guild, Event, Message  # concepts
from ..game import Game
from ..task import TaskManager

from ..log import logger

log = logger

__name__ = "Kook.Bot.bot"

TypeEventHandler = Callable[['Bot', Event], Coroutine]
TypeMessageHandler = Callable[[Message], Coroutine]
TypeStartupHandler = Callable[['Bot'], Coroutine]
TypeShutdownHandler = Callable[['Bot'], Coroutine]

default_config = {
    "token": "xxxxxx",
    "port": 5000,
    "compress": True,
    "command_prefix": ["/"],
    "super_user": ["1234567"]
}


class Config:
    @staticmethod
    async def write_default_config(path: str) -> bool:
        if os.path.exists(path) is False:
            await Config.write(path, default_config)
            return True
        else:
            return False

    @staticmethod
    async def write(path: str, obj: Any) -> None:
        with open(path, 'w', encoding='utf8') as config:
            json.dump(obj, config, ensure_ascii=False, indent=4)

    @staticmethod
    async def read(path: str) -> Dict[str, Union[str, List[str]]]:
        if os.path.exists(path) is False:
            logger.info("配置文件不存在，正在生成新的配置文件...")
            await Config.write(path, default_config)
            logger.info("配置文件初始化完成，请修改后重新启动Akyra~")
            with open(path, "r", encoding='utf8') as config:
                return json.load(config)
        else:
            with open(path, "r", encoding='utf8') as config:
                return json.load(config)


class Bot(AsyncRunnable):
    """
    Represents a entity that handles msg/events and interact with users/Kook server in manners that programmed.
    """
    # components
    client: Client
    task: TaskManager

    # flags
    _is_running: bool

    # internal containers
    _me: Optional[User]
    _event_index: Dict[EventTypes, List[TypeEventHandler]]

    _startup_index: List[TypeStartupHandler]
    _shutdown_index: List[TypeShutdownHandler]

    def __init__(self,
                 *,
                 cert: Cert = None,
                 client: Client = None,
                 gate: Gateway = None,
                 out: HTTPRequester = None,
                 route='/Kook-wh'):
        """
        The most common usage: ``Bot(token='xxxxxx')``

        That's enough.

        :param cert: used to build requester and receiver
        :param client: the bot relies on
        :param gate: the client relies on
        :param out: the gate's component
        :param compress: used to tune the receiver
        :param port: used to tune the WebhookReceiver
        :param route: used to tune the WebhookReceiver
        """

        self.cert = cert
        self.client_ = client
        self.gate = gate
        self.out = out
        self.route = route
        #self._init_client(cert or Cert(token=token), client, gate, out, compress, port, route)

        self.task = TaskManager()

        self._is_running = False
        self._event_index = {}
        self._startup_index = []
        self._shutdown_index = []

    def _init_client(self, cert: Cert, client: Client, gate: Gateway, out: HTTPRequester, compress: bool, port, route):
        """
        construct self.client from args.

        you can init client with kinds of filling ways,
        so there is a priority in the rule: client > gate > out = compress = port = route

        :param cert: used to build requester and receiver
        :param client: the bot relies on
        :param gate: the client relies on
        :param out: the gate's component
        :param compress: used to tune the receiver
        :param port: used to tune the WebhookReceiver
        :param route: used to tune the WebhookReceiver
        :return:
        """
        if client:
            self.client = client
            return
        if gate:
            self.client = Client(gate)
            return

        # client and gate not in args, build them
        _out = out if out else HTTPRequester(cert)
        if cert.type == Cert.Types.WEBSOCKET:
            _in = WebsocketReceiver(cert, compress)
        else:
            raise ValueError(f'cert type: {cert.type} not supported')

        self.client = Client(Gateway(_out, _in))

    def add_event_handler(self, type: EventTypes, handler: TypeEventHandler):
        """add an event handler function for EventTypes `type`"""
        if type not in self._event_index:
            self._event_index[type] = []
        self._event_index[type].append(handler)
        log.debug(f'event_handler {handler.__qualname__} for {type} added')
        return handler

    def add_message_handler(self, handler: TypeMessageHandler, *except_type: MessageTypes):
        """`except_type` is an exclusion list"""
        for type in MessageTypes:
            if type not in except_type:
                self.client.register(type, handler)

    def on_event(self, type: EventTypes):
        """decorator, register a function to handle events of the type"""

        def dec(func: TypeEventHandler):
            self.add_event_handler(type, func)

        return dec

    def on_message(self, *except_type: MessageTypes):
        """
        decorator, register a function to handle messages
        :param except_type: excepted types
        """

        def dec(func: TypeMessageHandler):
            self.add_message_handler(func, *set(except_type + (MessageTypes.SYS,)))

        return dec

    def on_startup(self, func: TypeStartupHandler):
        """decorator, register a function to handle bot start"""

        self._startup_index.append(func)

        return func

    def on_shutdown(self, func: TypeShutdownHandler):
        """decorator, register a function to handle bot stop"""

        self._shutdown_index.append(func)

        return func

    async def fetch_me(self, force_update: bool = False) -> User:
        """fetch detail of the bot it self as a ``User``

        .. deprecated-removed:: 0.3.0 0.4.0
            use :func:`.client.fetch_me()`"""
        warnings.warn("deprecated, alternative: bot.client.fetch_me()", DeprecationWarning, stacklevel=2)
        return await self.client.fetch_me(force_update)

    @property
    def me(self) -> User:
        """
        get bot itself data

        CAUTION: please call ``await fetch_me()`` first to load data from Kook server

        designed as 'empty-then-fetch' will break the rule 'net-related is async'

        :returns: the bot's underlying User

        .. deprecated-removed:: 0.3.0 0.4.0
            use await :func:`.client.fetch_me()`
        """
        warnings.warn("deprecated, alternative: bot.client.fetch_me(), everything else is in the same",
                      DeprecationWarning,
                      stacklevel=2)
        return self.client.me

    async def fetch_public_channel(self, channel_id: str) -> PublicChannel:
        """channel id -> :class:`PublicChannel` object(public channel only),
        fetch details of a public channel from Kook

        .. deprecated-removed:: 0.3.0 0.4.0
            use :func:`.client.fetch_public_channel()`"""
        warnings.warn("deprecated, alternative: bot.client.fetch_public_channel(), everything else is in the same",
                      DeprecationWarning,
                      stacklevel=2)
        return await self.client.fetch_public_channel(channel_id)

    async def fetch_user(self, user_id: str) -> User:
        """user id -> :class:`User` object, fetch user info from Kook

        .. deprecated-removed:: 0.3.0 0.4.0
            use :func:`.client.fetch_user()`"""
        warnings.warn("deprecated, alternative: bot.client.fetch_user(), everything else is in the same",
                      DeprecationWarning,
                      stacklevel=2)
        return await self.client.fetch_user(user_id)

    async def delete_channel(self, channel: Union[Channel, str]):
        """delete a channel, permission required

        .. deprecated-removed:: 0.3.0 0.4.0
            use :func:`.client.delete_channel()`"""
        warnings.warn("deprecated, alternative: bot.client.delete_channel(), everything else is in the same",
                      DeprecationWarning,
                      stacklevel=2)
        return await self.client.delete_channel(channel)

    async def fetch_guild(self, guild_id: str) -> Guild:
        """guild id -> :class:`Guild` object, fetch details of a guild from Kook

        .. deprecated-removed:: 0.3.0 0.4.0
            use :func:`.client.fetch_guild()`"""
        warnings.warn("deprecated, alternative: bot.client.fetch_guild(), everything else is in the same",
                      DeprecationWarning,
                      stacklevel=2)
        return await self.client.fetch_guild(guild_id)

    async def list_guild(self) -> List[Guild]:
        """list guilds the bot joined

        .. deprecated-removed:: 0.3.0 0.4.0
            use :func:`.client.fetch_guild_list()`
        """
        warnings.warn("deprecated, alternative: bot.client.fetch_guild_list(), everything else is in the same",
                      DeprecationWarning,
                      stacklevel=2)
        return await self.client.fetch_guild_list()

    async def send(self,
                   target: Channel,
                   content: Union[str, List],
                   *,
                   type: MessageTypes = None,
                   temp_target_id: str = '',
                   **kwargs):
        """
        send a msg to a channel

        ``temp_target_id`` is only available in ChannelPrivacyTypes.GROUP

        .. deprecated-removed:: 0.3.0 0.4.0
            use :func:`.client.send()`"""
        warnings.warn("deprecated, alternative: bot.client.send(), everything else is in the same",
                      DeprecationWarning,
                      stacklevel=2)
        return await self.client.send(target, content, type=type, temp_target_id=temp_target_id, **kwargs)

    async def upload_asset(self, file: Union[IO, str, Path]) -> str:
        """upload ``file`` to Kook, and return the url to the file, alias for ``create_asset``

        if ``file`` is a str or Path, ``open(file, 'rb')`` will be called to convert it into IO

        .. deprecated-removed:: 0.3.0 0.4.0
            use :func:`.client.create_asset()`"""
        warnings.warn("deprecated, alternative: bot.client.create_asset(), everything else is in the same",
                      DeprecationWarning,
                      stacklevel=2)
        return await self.create_asset(file)

    async def create_asset(self, file: Union[IO, str, Path]) -> str:
        """upload ``file`` to Kook, and return the url to the file

        if ``file`` is a str or Path, ``open(file, 'rb')`` will be called to convert it into IO

        .. deprecated-removed:: 0.3.0 0.4.0
            use :func:`.client.create_asset()`"""
        warnings.warn("deprecated, alternative: bot.client.create_asset(), everything else is in the same",
                      DeprecationWarning,
                      stacklevel=2)
        return await self.client.create_asset(file)

    async def kickout(self, guild: Union[Guild, str], user: Union[User, str]):
        """kick ``user`` out from ``guild``

        .. deprecated-removed:: 0.3.0 0.4.0
            use :func:`.client.kickout()`"""
        warnings.warn("deprecated, alternative: bot.client.kickout(), everything else is in the same",
                      DeprecationWarning,
                      stacklevel=2)
        return await self.client.kickout(guild, user)

    async def leave(self, guild: Union[Guild, str]):
        """leave from ``guild``

        .. deprecated-removed:: 0.3.0 0.4.0
            use :func:`.client.leave()`"""
        warnings.warn("deprecated, alternative: bot.client.leave(), everything else is in the same",
                      DeprecationWarning,
                      stacklevel=2)
        return await self.client.leave(guild)

    async def add_reaction(self, msg: Message, emoji: str):
        """add emoji to msg's reaction list

        wraps `Message.add_reaction`

        :param msg: accepts `Message`
        :param emoji: 😘

        .. deprecated-removed:: 0.3.0 0.4.0
            use :func:`.client.add_reaction()`
        """
        warnings.warn("deprecated, alternative: bot.client.add_reaction(), everything else is in the same",
                      DeprecationWarning,
                      stacklevel=2)
        return await self.client.add_reaction(msg, emoji)

    async def delete_reaction(self, msg: Message, emoji: str, user: User = None):
        """delete emoji from msg's reaction list

        wraps `Message.delete_reaction`

        :param msg: accepts `Message`
        :param emoji: 😘
        :param user: whose reaction, delete others added reaction requires channel msg admin permission

        .. deprecated-removed:: 0.3.0 0.4.0
            use :func:`.client.delete_reaction()`
        """
        warnings.warn("deprecated, alternative: bot.client.delete_reaction(), everything else is in the same",
                      DeprecationWarning,
                      stacklevel=2)
        return await self.client.delete_reaction(msg, emoji, user)

    async def list_game(self,
                        *,
                        begin_page: int = 1,
                        end_page: int = None,
                        page_size: int = 50,
                        sort: str = '') -> List[Game]:
        """list the games already registered at Kook server

        .. deprecated-removed:: 0.3.0 0.4.0
            use :func:`.client.fetch_game_list()`"""
        warnings.warn("deprecated, alternative: bot.client.fetch_game_list(), everything else is in the same",
                      DeprecationWarning,
                      stacklevel=2)
        return await self.client.fetch_game_list(begin_page=begin_page,
                                                 end_page=end_page,
                                                 page_size=page_size,
                                                 sort=sort)

    async def create_game(self, name: str, process_name: str = None, icon: str = None) -> Game:
        """register a new game at Kook server, can be used in profile status

        .. deprecated-removed:: 0.3.0 0.4.0
            use :func:`.client.register_game()`"""
        warnings.warn("deprecated, alternative: bot.client.register_game(), everything else is in the same",
                      DeprecationWarning,
                      stacklevel=2)
        return await self.client.register_game(name, process_name, icon)

    async def update_game(self, id: int, name: str = None, icon: str = None) -> Game:
        """update game already registered at Kook server

        .. deprecated-removed:: 0.3.0 0.4.0
            use :func:`.client.update_game()`"""
        warnings.warn("deprecated, alternative: bot.client.update_game(), everything else is in the same",
                      DeprecationWarning,
                      stacklevel=2)
        return await self.client.update_game(id, name, icon)

    async def delete_game(self, game: Union[Game, int]):
        """unregister game from Kook server

        :param game: accepts both Game object and bare game id(int type)

        .. deprecated-removed:: 0.3.0 0.4.0
            use :func:`.client.unregister_game()`"""
        warnings.warn("deprecated, alternative: bot.client.unregister_game(), everything else is in the same",
                      DeprecationWarning,
                      stacklevel=2)
        await self.client.unregister_game(game)

    async def update_playing_game(self, game: Union[Game, int]):
        """update current playing game status

        :param game: accepts both Game object and bare id(int type)

        .. deprecated-removed:: 0.3.0 0.4.0
            use :func:`.client.update_playing_game()`"""
        warnings.warn("deprecated, alternative: bot.client.update_playing_game(), everything else is in the same",
                      DeprecationWarning,
                      stacklevel=2)
        await self.client.update_playing_game(game)

    async def stop_playing_game(self):
        """clear current playing game status

        .. deprecated-removed:: 0.3.0 0.4.0
            use :func:`.client.stop_playing_game()`"""
        warnings.warn("deprecated, alternative: bot.client.stop_playing_game(), everything else is in the same",
                      DeprecationWarning,
                      stacklevel=2)
        await self.client.stop_playing_game()

    async def update_listening_music(self, music_name: str, singer: str, software: Union[str, SoftwareTypes]):
        """update current listening music status

        :param music_name: name of music
        :param singer: singer of the music
        :param software: set software to playing the music

        .. deprecated-removed:: 0.3.0 0.4.0
            use :func:`.client.update_listening_music()`"""
        warnings.warn("deprecated, alternative: bot.client.update_listening_music(), everything else is in the same",
                      DeprecationWarning,
                      stacklevel=2)
        await self.client.update_listening_music(music_name, singer, software)

    async def stop_listening_music(self):
        """clear current listening music status

        .. deprecated-removed:: 0.3.0 0.4.0
            use :func:`.client.stop_listening_music()`"""
        warnings.warn("deprecated, alternative: bot.client.stop_listening_music(), everything else is in the same",
                      DeprecationWarning,
                      stacklevel=2)
        await self.client.stop_listening_music()

    async def update_channel(self,
                             channel: Union[str, PublicChannel],
                             name: str = None,
                             topic: str = None,
                             slow_mode: Union[int, SlowModeTypes] = None):
        """update channel's settings

        .. deprecated-removed:: 0.3.0 0.4.0
            use :func:`.client.update_channel()`"""
        warnings.warn("deprecated, alternative: bot.client.update_channel(), everything else is in the same",
                      DeprecationWarning,
                      stacklevel=2)
        await self.client.update_channel(channel, name, topic, slow_mode)

    async def start(self):
        config = await Config.read("./config.json")
        self._init_client(self.cert or Cert(token=config["token"]), self.client_, self.gate, self.out, config["compress"], config["port"], self.route)

        for func in self._startup_index:
            await func(self)
        if self._is_running:
            raise RuntimeError('this bot is already running')
        self.task.schedule()
        await self.client.start()

    def run(self):
        """run the bot in blocking mode"""
        if not self.loop:
            self.loop = asyncio.get_event_loop()
        try:
            self.loop.run_until_complete(self.start())
        except KeyboardInterrupt:
            for func in self._shutdown_index:
                self.loop.run_until_complete(func(self))
            log.info('see you next time')
