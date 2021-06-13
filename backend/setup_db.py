import json
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import func
from contextlib import contextmanager
from config import DATABASE_URI
from app import app
from app.database import Base
from app.models import Skill, Vacancy, Speciality

engine = create_engine(DATABASE_URI)
Session = sessionmaker(bind=engine)


@contextmanager
def session_scope():
    session = Session()
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()

def reset_database():
    print('Reset database')
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)

def create_database():
    print('Create database')
    # Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)

def seed_vacancies():
    print('Seed vacancies')
    with session_scope() as s:
        with open('habr_vacancies.json', 'r') as f:
            vacancies_data = json.load(f)
            print(vacancies_data)
            for vacancy_dict in vacancies_data:
                vacancy = Vacancy(
                    name = vacancy_dict['title'],
                    publication_date = vacancy_dict['publish_date']
                )
                s.add(vacancy)

def seed_specialities():
    print('Seed specialities')
    with session_scope() as s:
        speciality_names = ['Бэкэнд', 'Фронтэнд', 'Дизайн']
        for speciality_name in  speciality_names:
            speciality = Speciality(
                name = speciality_name,
            )
            s.add(speciality)

    
def seed_skills():
    print('Seed skills')
    with session_scope() as s:
        skill = Skill(
            name='Git',
        )
        s.add(skill)
        # Skill 2
        skill = Skill(
            name='Flask',
        )
        s.add(skill)
        # Skill 3
        skill = Skill(
            name='Бэкенд',
        )
        s.add(skill)
        # Skill 4
        skill = Skill(
            name='Python',
        )
        s.add(skill)
        # Skill 5
        skill = Skill(
            name='Django',
        )
        s.add(skill)
        # Skill 6
        skill = Skill(
            name='SQL',
        )
        s.add(skill)
        # Skill 6
        skill = Skill(
            name='Linux',
        )
        s.add(skill)

if __name__ == '__main__':
    reset_database()
    # create_database()
    seed_vacancies()
    seed_skills()
    seed_specialities()
