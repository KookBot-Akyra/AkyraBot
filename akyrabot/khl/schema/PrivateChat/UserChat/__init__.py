from ... import Base, statusBase, meta
from ...objects import userBase

from typing import Dict, List

class userChatBase(Base):
    code: str
    last_read_time: int
    latest_msg_time: int
    unread_count: int
    target_info: userBase

class userChatListHandler(statusBase):
    class Data(Base):
        items: List[userChatBase]
        meta: meta
    
    data: Data

class userChatViewHandler(statusBase):
    data: userChatBase

class userChatCreateHandler(statusBase):
    data: userChatBase

class userChatDeleteHandler(statusBase):
    data: Dict
