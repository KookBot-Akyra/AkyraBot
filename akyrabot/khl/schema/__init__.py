from pydantic import BaseModel


class Base(BaseModel):
    class Config:
        extra = "ignore"

class meta(Base):
    page: int
    page_total: int
    page_size: int
    total: int

class statusBase(Base):
    code: int
    message: str
