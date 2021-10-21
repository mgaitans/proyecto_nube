from backend import create_app
from flask_restful import Api
from .modelos import db
from .vistas import *
from flask_jwt_extended import JWTManager
from flask_cors import CORS, cross_origin

app = create_app('default')
app_context = app.app_context()
app_context.push()

db.init_app(app)
db.create_all()
cors = CORS(app)

api = Api(app)

api.add_resource(VistaTareas, '/api/tasks')
api.add_resource(VistaTarea, '/api/tasks/<int:id_task>')

jwt = JWTManager(app)