from ... import Base, statusBase, meta
from ...objects import userBase

from typing import List, Dict

class guildEmojiBase(Base):
    name: str
    id: str
    user_info: userBase

class guildEmojiListHandler(statusBase):
    class Data:
        items: List[guildEmojiBase]
        meta: meta
    
    data: Data

class guildEmojiCreateHandler(statusBase):
    data: guildEmojiBase

class guildEmojiHandlerBase(statusBase):
    data: Dict
