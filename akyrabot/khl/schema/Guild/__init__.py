from .. import statusBase, Base, meta
from ..objects import guildBase, userBase

from typing import List, Dict

class guildHandlerBase(statusBase):
    data: Dict

class guildListHandler(statusBase):
    class Data(Base):
        items: guildBase
        meta: meta
    
    data: Data

class guildViewHandler(statusBase):
    data: guildBase

class guildUserListHandler(statusBase):
    class Data(Base):
        items: List[userBase]
        meta: meta
        user_count: int
        online_count: int
        offline_count: int
    
    data: Data

class guildMuteListHandler(statusBase):
    class Data(Base):
        class Mic(Base):
            type: int
            user_ids: List[str]

        class Headset(Base):
            type: int
            user_ids: List[str]

        mic: Mic
        headset: Headset

    data: Data
    
class guildBoostHistoryHandler(statusBase):
    class Data(Base):
        class Items(Base):
            user_id: str
            guild_id: str
            start_time: int
            end_time: int
            user: userBase

        items: List[Items]
        meta: meta
    
    data: Data
