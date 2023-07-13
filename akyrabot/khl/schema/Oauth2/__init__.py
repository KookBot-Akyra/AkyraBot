from ...schema import Base


class oault2TokenHandler(Base):
    access_token: str
    expires_in: int
    token_type: str
    scope: str
