from datetime import datetime, timezone
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from marshmallow_sqlalchemy import fields
from app import app
from app.models import Vacancy, Skill, Speciality, Seeker, SeekerSkill, VacancySkill


class SkillSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Skill
        include_fk = True
        include_relationships = True

class VacancySchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Vacancy
        include_relationships = True
        include_fk = True

class SpecialitySchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Speciality
        include_fk = True

class SeekerSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Seeker
        include_relationships = True
        include_fk = True

class SeekerSkillSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = SeekerSkill
        include_fk = True
        #include_relationships = True

class VacancySkillSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = VacancySkill
        include_fk = True