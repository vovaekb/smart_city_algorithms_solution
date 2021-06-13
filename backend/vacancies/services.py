import os
import numpy as np
from app import app, CustomError
from app.models import Vacancy, Skill
from app.serializers import VacancySchema, SkillSchema

vacancies_schema = VacancySchema(many=True)


# User service class
class VacanciesService:
    def get_all():
        print('VacanciesService.get_all()')
        vacancies = app.session.query(Vacancy)
        #users = users.order_by(Users.email.asc()).all()
        print(vacancies)
        vacancies_dict = vacancies_schema.dump(vacancies)
        #print(users_dict)
        return vacancies_dict
    
    def get_best():
        print('VacanciesService.get_best()')
        vacancies = app.session.query(Vacancy)
        #for 
        #users = users.order_by(Users.email.asc()).all()
        print(vacancies)
        vacancies_dict = vacancies_schema.dump(vacancies)
        vacancies_number = len(vacancies_dict)
        print(len(vacancies_dict))
        scores = np.random.random(vacancies_number)
        print(scores)
        scores = sorted(scores, reverse=True)
        print(scores)
        for i in range(vacancies_number):
            vacancies_dict[i]['score'] = scores[i]
        #print(users_dict)
        return vacancies_dict
