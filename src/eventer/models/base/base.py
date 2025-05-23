from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.ext.declarative import declared_attr


class Base(DeclarativeBase):
    __abstract__ = True
    
    @declared_attr
    def __tablename__(cls):
        return f"{cls.__name__.lower()}s"