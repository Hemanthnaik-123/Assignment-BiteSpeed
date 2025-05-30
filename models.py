from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.sql import func
from database import Base

class Contact(Base):
    __tablename__ = "details"

    id = Column(Integer, primary_key=True, index=True)
    phonenumber = Column(String(10))
    email = Column(String(255))
    linkedid = Column(Integer, ForeignKey("details.id"))
    linkprecedence = Column(String(10))
    createdat = Column(DateTime(timezone=True), server_default=func.now())
    updatedat = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    deletedat = Column(DateTime(timezone=True), nullable=True)
