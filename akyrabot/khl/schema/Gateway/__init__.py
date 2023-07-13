from ...schema import Base

class gatewayHandler(Base):
    class gateway(Base):
        url: str
        
    code: int
    message: str
    data: gateway