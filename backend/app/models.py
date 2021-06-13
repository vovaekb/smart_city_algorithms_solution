import datetime
import enum
import uuid
# from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Table, Integer, ForeignKey, ARRAY
from sqlalchemy.types import Float, Numeric, String, DateTime, Date, Enum, UnicodeText, Boolean
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.sql import func
from app import database

# Base = declarative_base()


Role = Enum(
    value='Role',
    names = [
        ('admin', 1), ('user', 2)
    ]
)


class Skill(database.Base):
    __tablename__ = 'skills'
    id = Column(UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        index=True
    )
    name = Column(String(2083), nullable=False)
    #updatedById = Column(UUID(as_uuid=True), ForeignKey('users.id', ondelete='SET NULL'), nullable=True)
    #updatedBy = relationship("Users", foreign_keys=[updatedById], uselist=False, post_update=True)


class Vacancy(database.Base):
    __tablename__ = 'vacancies'
    id = Column(UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        index=True
    )
    name = Column(String(2083), nullable=False)
    publication_date = Column(UnicodeText, nullable=True) # # Column(DateTime(timezone=True), nullable=True) #, server_default=func.now())

class Speciality(database.Base):
    __tablename__ = 'specialities'
    id = Column(Integer,
        primary_key=True
    )
    name = Column(String(2083), nullable=False)

class Seeker(database.Base):
    __tablename__ = 'seekers'
    id = Column(Integer,
        primary_key=True
    )
    name = Column(String(2083), nullable=False)
