import os
from flask import abort
from app import app
from app.models import Skill
from app.serializers import SkillSchema

skills_schema = SkillSchema(many=True)


class SkillService:
    def get_all():
        print('SkillService.get_all()')
        skills = app.session.query(Skill)
        #users = users.order_by(Users.email.asc()).all()
        print(skills)
        skills_dict = skills_schema.dump(skills)
        #print(users_dict)
        return skills_dict
