from ... import Base, statusBase, meta

from typing import List, Dict

class guildRoleBase(Base):
    role_id: int
    name: str
    color: int
    position: int
    hoist: int
    mentionable: int
    permissions: int

class guildRoleListHandler(statusBase):
    class Data(Base):
        items: List[guildRoleBase]
        meta: meta

    data: Data

class guildRoleCreateHandler(statusBase):
    data: List[guildRoleBase]

class guildRoleUpdateHandler(statusBase):
    data: List[guildRoleBase]

class guildRoleDeleteHandler(statusBase):
    data: Dict

class guildRoleUserBase(statusBase):
    class Data(Base):
        user: str
        guild_id: str
        role: List[int]

    data: Data