from flask import render_template, Blueprint, request, Response, jsonify
from sqlalchemy.exc import SQLAlchemyError
from app import app
from app import CustomError
from app.models import Vacancy, Skill
from app.serializers import VacancySchema, SkillSchema
from app.vacancies.services import VacanciesService

# CONFIG
vacancies_blueprint = Blueprint('vacancies', __name__) # , template_folder='templates')
vacancy_schema = VacancySchema()
vacancies_schema = VacancySchema(many=True)
skill_schema = SkillSchema()
skills_schema = SkillSchema(many=True)


@vacancies_blueprint.errorhandler(CustomError)
def handle_error(e):
    details = e.args[0]
    return Response(details['message'], status=500, mimetype='text/plain')


# ROUTES
'''
@vacancies_blueprint.route('/vacancies', methods=['POST'])
def index_post(current_user):
    print('/users POST accepted')
    data = request.get_json()
    user_data = data['data']
    if 'disabled' in user_data and user_data['disabled'] == '':
        user_data['disabled'] = None
    if 'role' in user_data and user_data['role'] == '':
        user_data['role'] = None
    print(data)
    referrer = request.headers.get("Referer")
    # print(referrer)
    try:
        UserService.create(user_data, current_user, referrer, True)
        text = 'true'
        return Response(text, status=200)
    except SQLAlchemyError as e:
        print("Unable to add user to database.")
        app.session.rollback()
        details = e.args[0]
        return Response(details, status=555, mimetype='text/plain')
'''

@vacancies_blueprint.route('/vacancies', methods=['GET'])
def index_get():
    print('/users GET accepted')
    vacancies = VacanciesService.get_all()
    data = {
        'rows': vacancies,
        'count': len(vacancies)
    }
    return jsonify(data)

@vacancies_blueprint.route('/best_vacancies', methods=['POST'])
def index_post():
    print('/users POST accepted')
    data = request.get_json()
    print(data)
    # Find most relevant vacancies
    vacancies = VacanciesService.get_best()
    data = {
        'rows': vacancies,
        'count': len(vacancies)
    }
    return jsonify(data)
