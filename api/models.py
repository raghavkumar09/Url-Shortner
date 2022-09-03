from sqlalchemy import Column, Integer, String
from api.database import Base


# Declare class for table
class Url(Base):
    __tablename__ = 'urls'

    id = Column(Integer, primary_key=True, index=True)
    originalUrl = Column(String, unique=True, index=True)
    shortUrl = Column(String, unique=True, index=True)
    views = Column(Integer, default=0)
