from flask import Flask, flash, redirect, render_template, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from Web.config import Config
from Web import models

db = SQLAlchemy()

migrate = Migrate()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
   
    migrate.init_app(app, db)

    
    from routes import routes
    app.register_blueprint(routes)

    return app

if __name__ == '__main__':
    app = create_app()
    app.run()