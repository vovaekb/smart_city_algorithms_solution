from datetime import datetime, timezone
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from marshmallow_sqlalchemy import fields
from app import app
from app.models import Vacancy, Skill, Speciality


class SkillSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Skill
        include_fk = True
        # include_relationships = True
        # include_fk = True

class SpecialitySchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Speciality
        include_fk = True


class VacancySchema(SQLAlchemyAutoSchema):
    # publication_date = fields.fields.Function(lambda obj: obj.createdAt.astimezone(timezone.utc).isoformat('T', timespec='milliseconds').replace('+00:00', 'Z'))
    class Meta:
        model = Vacancy
        include_fk = True
        exclude = ("publication_date",)
        #include_relationships = True
