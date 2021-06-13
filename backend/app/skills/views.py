import os
from flask import render_template, abort, Blueprint, request, Response, jsonify, send_file, send_from_directory
from app import app
from app.serializers import SkillSchema
from app.skills.services import SkillService

# CONFIG
skills_blueprint = Blueprint('skills', __name__) #, template_folder='templates')
skill_schema = SkillSchema()
skills_schema = SkillSchema(many=True)



# ROUTES
@skills_blueprint.route('/skills', methods=['GET'])
def skills_index():
    skills = SkillService.get_all()
    data = {
        'rows': skills,
        'count': len(skills)
    }
    return jsonify(data)
