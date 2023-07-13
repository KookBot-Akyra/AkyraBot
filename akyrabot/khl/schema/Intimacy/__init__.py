from ...schema import Base, statusBase
from typing import List


class intimacyIndexHandler(statusBase):
    class index(Base):
        class imgListStruct(Base):
            id: int
            url: str

        img_url: str
        social_info: str
        last_read: int
        score: int
        img_list: List[imgListStruct]

    data: index


class intimacyUpdateHandler(statusBase):
    data: dict
