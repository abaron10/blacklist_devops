from server import create_app
from .modelos import db
from flask_restful import Api
from .vistas import VistaLogIn, VistaSignIn, VistaBlackList
from flask_jwt_extended import JWTManager
from flask_cors import CORS

app = create_app('default')
app_context = app.app_context()
app_context.push()
app.debug = True
db.init_app(app)
db.create_all()

cors = CORS(app)
api = Api(app)
api.add_resource(VistaSignIn, '/auth/signup')
api.add_resource(VistaLogIn, '/auth/login')
api.add_resource(VistaBlackList, '/blacklist/<string:email>')
jwt = JWTManager(app)
