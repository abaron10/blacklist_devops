from .modelos import db
from flask_restful import Api
from .vistas import VistaLogIn, VistaSignIn, VistaBlackList, VistaHealth
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from flask import Flask

def create_app(config_name):
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///conversion_system.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['JWT_SECRET_KEY'] = 'ROCK&ROLL_TRAIN_ACDC'
    app.config['PROPAGATE_EXCEPTION'] = True

    return app


app = create_app('default')
app_context = app.app_context()
app_context.push()
app.debug = True
db.init_app(app)
db.create_all()

cors = CORS(app)
api = Api(app)
api.add_resource(VistaSignIn, '/auth/signup')
api.add_resource(VistaHealth, '/')
api.add_resource(VistaLogIn, '/auth/login')
api.add_resource(VistaBlackList, '/blacklist/<string:email>')
jwt = JWTManager(app)

if __name__ == "__main__":
    app.run()
