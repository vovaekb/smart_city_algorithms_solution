import os
import flask
import json
from flask import Flask, _app_ctx_stack, render_template, request, jsonify, Response
from flask_cors import CORS, cross_origin
from sqlalchemy.orm import scoped_session
from app.database import SessionLocal, engine, Base
#from app.models import Users
from config import Config, DevConfig, ProductionConfig

# Create database structure
#Base.metadata.create_all(bind=engine)

APP_ROOT = os.path.dirname(os.path.abspath(__file__))


app = Flask(__name__)
CORS(app, supports_credentials=True)
app.session = scoped_session(SessionLocal, scopefunc=_app_ctx_stack.__ident_func__)
#app.secret_key = os.environ.get("FN_FLASK_SECRET_KEY", default=False)

if os.environ['FLASK_DEV'] == True:
    print("Dev env")
    app.config.from_object(DevConfig)
else:
    print("Prod env")
    app.config.from_object(ProductionConfig)


# Global methods and classes

# Error handlers
class CustomError(Exception):
    pass

# Error handlers
class ValidationError(Exception):
    pass

@app.after_request
def set_headers(response):
    response.headers["Referrer-Policy"] = 'no-referrer'
    return response

# BLUEPRINTS
from app.vacancies.views import vacancies_blueprint
from app.skills.views import skills_blueprint

app.register_blueprint(vacancies_blueprint)
app.register_blueprint(skills_blueprint)

# from app import views
