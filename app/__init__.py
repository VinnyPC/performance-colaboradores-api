# app/__init__.py
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from app.config import Config
from app.extensions import db
from flasgger import Swagger
import os, yaml

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)

    # Registrar blueprints
    from app.routes.colaborador_routes import colaboradores_bp
    from app.routes.avaliacoes_routes import avaliacoes_bp
    from app.routes.nota_final_routes import nota_final_bp
    app.register_blueprint(nota_final_bp)
    app.register_blueprint(colaboradores_bp)
    app.register_blueprint(avaliacoes_bp)

    # Configurar Swagger
    swagger = Swagger(app, template={
        "info": {
            "title": "API de Avaliações",
            "version": "1.0.0",
            "description": "Documentação dos endpoints da API de colaboradores e avaliações."
        },
        "tags": [
            {"name": "Avaliações", "description": "Endpoints de avaliação comportamental e de desafios"},
            {"name": "Colaboradores", "description": "Endpoints de colaboradores"},
            {"name": "Notas Finais", "description": "Endpoints para notas finais"}
        ]
    })

    # Função para carregar arquivos YAML em /docs
    def carregar_docs():
        docs_path = os.path.join(os.path.dirname(__file__), "docs")
        if os.path.exists(docs_path):
            for arquivo in os.listdir(docs_path):
                if arquivo.endswith((".yml", ".yaml")):
                    caminho = os.path.join(docs_path, arquivo)
                    try:
                        with open(caminho, "r", encoding="utf-8") as f:
                            spec = yaml.safe_load(f)

                            # Ignora arquivos vazios ou sem a chave 'paths'
                            if not spec:
                                print(f"[Swagger] Ignorado (vazio): {arquivo}")
                                continue

                            if "paths" not in spec:
                                print(f"[Swagger] Ignorado (sem 'paths'): {arquivo}")
                                continue

                            swagger.template.setdefault("paths", {})
                            swagger.template["paths"].update(spec["paths"])
                            print(f"[Swagger] Carregado: {arquivo}")

                    except Exception as e:
                        print(f"[Swagger] Erro ao carregar {arquivo}: {e}")


    carregar_docs()

    return app
