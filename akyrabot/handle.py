from typing import Dict

from .khl.log import logger

__name__ = "Handler"

class msgHandler:
    _pkg = Dict
    command_handle_list = []

    def __init__(self, pkg) -> None:
        self._pkg = pkg

    async def handle(self):
        ...
