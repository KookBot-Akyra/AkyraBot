from ...schema import Base, statusBase, meta
from ...schema.objects import userBase
from typing import List

class Data(Base):
    class Item(Base):
        channel_id: str
        guild_id: str
        url_code: str
        url: str
        user: userBase

    items: List[Item]
    meta: meta

class inviteListHandler(statusBase):
    data: Data


class inviteCreateHandler(statusBase):
    class Data(Base):
        url: str

    data: Data


class inviteDeleteHandler(statusBase):
    data: dict
