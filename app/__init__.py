from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from app.config import Config
from app.routes.colaborador_routes import colaboradores_bp
from app.routes.avaliacoes_routes import avaliacoes_bp
from app.extensions import db

def create_app():
    app = Flask(__name__)
    app.config.from_object("app.config.Config") 

    db.init_app(app)

    from app.routes.colaborador_routes import colaboradores_bp
    from app.routes.avaliacoes_routes import avaliacoes_bp
    from app.routes.nota_final_routes import nota_final_bp
    app.register_blueprint(nota_final_bp)
    app.register_blueprint(colaboradores_bp)
    app.register_blueprint(avaliacoes_bp)

    return app
