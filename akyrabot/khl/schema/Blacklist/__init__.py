from .. import statusBase, Base, meta
from ..objects import userBase
from typing import List, Dict

class blacklistListHandler(statusBase):
    class Data(Base):
        class Items(Base):
            user_id: str
            created_time: int
            remark: str
            user: userBase
        items: List(Items)
        meta: meta

    data: Data

class blacklistCreateHandler(statusBase):
    data: Dict

class blacklistDeleteHandler (statusBase):
    data: Dict
