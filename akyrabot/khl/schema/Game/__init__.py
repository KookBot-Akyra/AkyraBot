from .. import statusBase
from ..objects import gameBase

from typing import Dict

class gameHandlerBase(statusBase):
    data: gameBase

class gameBase(statusBase):
    data: Dict
