from .. import Base

class assetsCreateHandler(Base):
    class Data:
        url: str
    code: int
    message: str
    data: Data