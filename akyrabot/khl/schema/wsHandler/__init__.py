from typing import Optional, Union

from .. import Base
from ..objects import userBase

class EventHandler(Base):
    class Main(Base):
        class EXTRA(Base):
            type: Union[int, str]
            guild_id: Optional[str]
            channel_name: Optional[str]
            mention: Optional[list]
            mention_all: Optional[bool]
            mention_roles: Optional[list]
            mention_here: Optional[bool]
            author: Optional[userBase]
            # 这个Body不知道是啥
            body: Optional[dict]

        channel_type: Optional[str]
        type: Optional[int]
        target_id: Optional[str]
        author_id: Optional[str]
        content: Optional[str]
        msg_id: Optional[str]
        msg_timestamp: Optional[int]
        nonce: Optional[str]
        extra: Optional[EXTRA]
        code: Optional[int]
        session_id: Optional[str]
        
    s: int
    d: Optional[Main]
    sn: Optional[int]
    