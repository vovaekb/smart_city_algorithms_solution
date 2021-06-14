import os
import json
from flask import abort
import pandas as pd
from app import app, APP_ROOT
from app.models import Skill
from app.serializers import SkillSchema
from app.services.scraper import HHScraper

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

    def get_by_speciality(speciality):
        print('SkillService.get_by_speciality()')

        # data_file = os.path.join()
        scraper = HHScraper(keyword = speciality)
        vacancies_data = scraper.process_data()

        # Save to JSON file
        json_file = os.path.join(APP_ROOT, 'vacancies.json')

        with open(json_file, 'w') as fp:
            json.dump(vacancies_data, fp)
        
        top_skills = SkillService.get_top_common_skills(vacancies_data)
        return top_skills

    def get_top_common_skills(vacancies_data):
        skills_vac = [] # Список идентификаторов вакансий
        skills_name = [] # Список названий навыков
        for vacancy in vacancies_data:
            # Т.к. навыки хранятся в виде массива, то проходимся по нему циклом
            for skl in vacancy['vacancy_skills']:
                skills_vac.append(vacancy['id'])
                skills_name.append(skl)

        df = pd.DataFrame({'vacancy': skills_vac, 'skill': skills_name})
        dfs = df['skill'].value_counts()
        dfs = dfs.to_frame().reset_index()[:11]
        # for col in dfs.columns:
        #     print(col)

        skill_names = dfs['index'].tolist()
        return skill_names

    
