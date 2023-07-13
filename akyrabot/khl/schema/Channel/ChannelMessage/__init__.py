from ... import statusBase, Base
from ...objects import channelMessageBase, userBase

from typing import Union, List

class channelMessageListHandler(statusBase):
    class Data(Base):
        items: List[channelMessageBase]
    data: Data

class channelMessageViewHandler(statusBase):
    data: channelMessageBase

class channelMessageCreateHandler(statusBase):
    class Data(Base):
        msg_id: str
        msg_timestamp: int
        nonce: str

    data: Data

class channelMessageUpdateHandler(statusBase):
    data: List

class channelMessageDeleteHandler(statusBase):
    data: List

class channelMessageReactionListHandler(statusBase):
    class Data(userBase):
        class tagInfo(Base):
            color: str
            text: str
        tag_info: tagInfo
        reaction_time: int

    data: Union[Data, List[Data]]

class channelMessageAddReactionHandler(statusBase):
    data: List

class channelMessageDeleteReactionHandler(statusBase):
    data: List