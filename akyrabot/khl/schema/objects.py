from . import Base
from typing import Optional, Union, List

class userBase(Base):
    "用户基础类"
    class liveInfo(Base):
        in_live: bool
        audience_count: int
        live_thumb: str
        live_start_time: int

    id: str
    username: str
    nickname: Optional[str]
    identify_num: Optional[str]
    online: bool
    bot: Optional[bool]
    status: Optional[int]
    avatar: str
    vip_avatar: Optional[str]
    mobile_verified: Optional[bool]
    roles: List[int]
    joined_at: Optional[int]
    active_time: Optional[int]
    live_info: Optional[liveInfo]

class embedBase(Base):
    "超链接解析基础类"
    type: str
    url: str
    origin_url: str
    av_no: str
    iframe_path: str
    duration: int
    title: str
    pic: str

class permissionUsers(Base):
    "用户权限组基础类"
    user: userBase
    allow: int
    deny: int

class permissionOverwrites(Base):
    role_id: int
    allow: int
    deny: int

class permissionUser(Base):
    "用户权限基础类"
    user_id: str
    allow: int
    deny: int

class channelBase(Base):
    "频道基础类"
    id: str
    guild_id: str
    user_id: str
    parent_id: str
    name: str
    topic: str
    type: int
    level: int
    slow_mode: int
    has_password: bool
    is_category: bool
    permission_sync: int
    permission_overwrites: List[Union[permissionOverwrites, None]]
    permission_users: List[Union[permissionUsers, None]]

class guildBase(Base):
    "服务器基础类"
    class Channels(Base):
        id: str
        user_id: str
        parent_id: str
        name: str
        type: int
        level: int
        limit_amount: int
        is_category: bool
    id: str
    name: str
    topic: str
    user_id: str
    icon: str
    notify_type: int
    region: str
    enable_open: bool
    open_id: str
    default_channel_id: str
    welcome_channel_id: str
    roles: str
    channels: List[Channels]
    boost_num: Optional[int]

class quoteBase(Base):
    "引用信息基础类"
    id: str
    type: int
    content: str
    create_at: int
    author: userBase

class attachmentsBase(Base):
    "附加的多媒体数据基础类"
    type: str
    url: str
    name: str
    size: int

class channelMessageBase(Base):
    "频道信息基础类"
    class Reactions(Base):
        class Emoji(Base):
            id: str
            name: str
        emoji: Emoji
        count: int
        me: bool

    class mentionInfo(Base):
        class mentionPart(Base):
            id: str
            username: str
            full_name: str
            avatar: str

        class mentionRolePart(Base):
            role_id: int
            name: str
            color: int
            position: int
            hoist: int
            mentionable: int
            permissions: int

        mention_part: List[mentionPart]
        mention_role_part: List[mentionRolePart]


    id: str
    type: int
    author: userBase
    content: str
    mention: List[str]
    mention_all: bool
    mention_roles: List[int]
    mention_here: bool
    embeds: List[embedBase]
    attachments: Optional[attachmentsBase]
    reactions: Reactions
    quote: quoteBase
    mention_info: mentionInfo

class gameBase(Base):
    "用户动态基础类"
    id: int
    name: str
    type: type
    options: str
    kmhook_admin: bool
    process_name: List[Optional[str]]
    product_name: List[Optional[str]]
    icon: str