from ... import Base, statusBase
from ...objects import userBase, embedBase, attachmentsBase, quoteBase, channelMessageBase

from typing import Optional, Dict, List

class directMessageBase(Base):
    id: str
    type: int
    author_id: str
    content: str
    create_at: Optional[int]
    image_name: Optional[str]
    embeds: List[Optional[embedBase]]
    attachments: List[Optional[attachmentsBase]]
    reactions: List[channelMessageBase.Reactions]
    quote: quoteBase
    read_status: bool

class directMessageListHandler(statusBase):
    class Data(Base):
        items: directMessageBase

    data: Data

class directMessageViewHandler(statusBase):
    data: directMessageBase

class directMessageCreateHandler(statusBase):
    class Data(Base):
        msg_id: str
        msg_timestamp: int
        nonce: str
    
    data: Data

class directMessageUpdateHandler(statusBase):
    data: Dict

class directMessageDeleteHandler(statusBase):
    data: Dict

class directMessageReactionListHandler(statusBase):
    data: List[userBase]

class directMessageAddReactionHandler(statusBase):
    data: Dict

class directMessageDeleteReactionHandler(statusBase):
    data: Dict
