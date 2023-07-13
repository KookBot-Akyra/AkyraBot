from .. import Base, statusBase, meta
from ..objects import *
from typing import Optional, Union, Dict, List

class channelVauleError(Exception):
    pass

class channelListHandler(statusBase):
    class Data(Base):
        class Items(Base):
            id: str
            user_id: str
            parent_id: str
            name: str
            type: int
            level: int
            limit_amount: int
            is_category: bool
        items: List[Items]
        meta: meta
    data: Data
    
class channelViewHandler(statusBase):
    class Data(channelBase):
        limit_amount: int
        voice_quality: str
        server_url: str
        children: Optional[List[str]]
    data: Data

class channelCreateHandler(statusBase):
    data: channelViewHandler.Data

class channelUpdateHandler(statusBase):
    data: channelBase

class channelDeleteHandler(statusBase):
    data: Dict

class channelUserListHandler(statusBase):
    data: List[userBase]

class channelMoveUserHandler(statusBase):
    data: List

class channel_role:
    class channelRoleIndexHandler(statusBase):
        permission_sync: int
        permission_overwrites: List[Union[permissionOverwrites, None]]
        permission_users: List[Union[permissionUsers, None]]
    
    class channelRoleCreateHandler(statusBase):
        data: Union[permissionOverwrites, permissionUser]

    class channelRoleUpdateHandler(statusBase):
        data: Union[permissionOverwrites, permissionUser]

    class channelRoleSyncHandler(statusBase):
        class Data:
            permission_overwrites: List[Union[permissionOverwrites, None]]
            permission_users: List[Union[permissionUsers, None]]
        data: Data
    
    class channelRoleDeleteHandler(statusBase):
        data: Dict
