from flask import Flask

# configura el mando de importación global
def create_app(config_name):
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///conversion_system.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['JWT_SECRET_KEY'] = 'ROCK&ROLL_TRAIN_ACDC'
    app.config['PROPAGATE_EXCEPTION'] = True

    return app