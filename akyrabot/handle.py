from typing import Dict

from .khl.log import logger

__name__ = "Handler"

class msgHandler:
    _pkg = Dict

    def __init__(self, pkg) -> None:
        self._pkg = pkg

    async def handle(self):
        logger.info("自定义Handler模块相应")
