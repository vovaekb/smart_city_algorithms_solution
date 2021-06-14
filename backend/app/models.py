import datetime
import enum
import uuid
from sqlalchemy import Column, Table, Integer, ForeignKey
from sqlalchemy.types import Integer, Float, Numeric, String, DateTime, Date, UnicodeText, Boolean
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship, backref
from sqlalchemy.sql import func
from app import database



class VacancySkill(database.Base):
    __tablename__ = 'vacancy_skills'
    id = Column(UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        index=True
    )
    level = Column(UnicodeText, nullable=False)
    vacancy_id = Column(UUID(as_uuid=True), 
        ForeignKey('vacancies.id'),
        nullable=False,
        primary_key=True)
    skill_id = Column(UUID(as_uuid=True), 
        ForeignKey('skills.id'),
        nullable=False,
        primary_key=True)

class Skill(database.Base):
    __tablename__ = 'skills'
    id = Column(UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        index=True
    )
    name = Column(UnicodeText, nullable=False)
    # seeker = relationship('SeekerSkill', backref='seeker', uselist=False) # lazy=True, 
    vacancies = relationship('VacancySkill', backref='skill', primaryjoin=id == VacancySkill.skill_id, lazy='dynamic', cascade="all, delete-orphan")

class SeekerSkill(database.Base):
    __tablename__ = 'seeker_skill'
    id = Column(UUID(as_uuid=True),
        primary_key=True
    )
    form_score = Column(UnicodeText, nullable=True)
    test_score = Column(UnicodeText, nullable=True)
    # seeker_id = Column(UUID(as_uuid=True), ForeignKey('seekers.id'),
    #     nullable=False)
    skill_id = Column(UUID(as_uuid=True), ForeignKey('skills.id'))
    skill = relationship("Skill", foreign_keys=[skill_id], backref=backref("seeker_skill", uselist=False))
    # skill_id = Column(UUID(as_uuid=True), ForeignKey('skills.id'),
    #     nullable=False)

class Vacancy(database.Base):
    __tablename__ = 'vacancies'
    id = Column(UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        index=True
    )
    name = Column(UnicodeText, nullable=False)
    description = Column(UnicodeText, nullable=True)
    publication_date = Column(UnicodeText, nullable=True) # Column(DateTime(timezone=True), nullable=True) #, server_default=func.now())
    skills = relationship('VacancySkill', backref='vacancy', primaryjoin=id == VacancySkill.vacancy_id, lazy='dynamic', cascade="all, delete-orphan")



class Speciality(database.Base):
    __tablename__ = 'specialities'
    id = Column(UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        index=True
    )
    name = Column(UnicodeText, nullable=False)


class Seeker(database.Base):
    __tablename__ = 'seekers'
    id = Column(UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        index=True
    )
    name = Column(UnicodeText, nullable=False)
    # skills = relationship('SeekerSkill', backref='seeker', lazy=True)


