from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

SQLALCHEMY_DATABASE_URI = "postgres://postgres:123@localhost/netology_career_app"
#SQLALCHEMY_DATABASE_URI = "postgres://vyiszxalaohtlo:0a7324d388c44218af10a37aa3491bd42348031578c0b8a8bb84a66973fa738f@ec2-52-87-107-83.compute-1.amazonaws.com:5432/dauh8amv0h9cif"
# SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL'] - for production

engine = create_engine(
    SQLALCHEMY_DATABASE_URI
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
