from .. import Base
from typing import Optional


class userMeHandler(Base):
    class me(Base):
        id: str
        username: str
        identify_num: str
        online: bool
        os: str
        status: int
        avatar: str
        banner: str
        bot: bool
        mobile_verified: bool
        mobile_prefix: str
        mobile: str
        invited_count: int

    code: int
    message: str
    data: me


class userViewHandler(Base):
    class view(Base):
        class BG(Base):
            background: int

        id: str
        os: Optional[str]
        username: str
        nickname: Optional[str]
        identify_num: str
        online: bool
        status: int
        bot: bool
        avatar: str
        vip_avatar: str
        is_vip: Optional[bool]
        vip_amp: Optional[bool]
        mobile_verified: Optional[bool]
        is_ai_reduce_noise: Optional[bool]
        is_personal_card_bg: Optional[bool]
        decorations_id_ma: Optional[BG]
        roles: list
        joined_at: Optional[int]
        active_time: Optional[int]
        banner: Optional[str]
        is_sys: Optional[bool]

    code: int
    message: str
    data: view


class userOfflineHandler(Base):
    code: int
    message: str
    data: dict
