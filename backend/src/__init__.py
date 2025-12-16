

from flask import Flask, jsonify
# Les imports sont corrects, en supposant que ia_bp est défini dans ia/__init__.py
from src.extensions import db, migrate, jwt, cors, bcrypt
from src.auth import auth_bp
from src.users import users_bp
from src.documents import documents_bp

# Import du Blueprint IA avec gestion d'erreur
try:
    from src.ia import ia_bp
except ImportError as e:
    print(f"⚠️  AVERTISSEMENT: Impossible d'importer le Blueprint IA: {e}")
    print("   Les routes /api/ia ne seront pas disponibles.")
    ia_bp = None
except Exception as e:
    print(f"❌ ERREUR lors de l'import du Blueprint IA: {e}")
    import traceback
    traceback.print_exc()
    ia_bp = None

def create_app():
    app = Flask(__name__, instance_relative_config=True)

    # Configuration
    app.config.from_object('config.Config')
    app.config.from_pyfile('config.py', silent=True)

    # Initialisation des extensions
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    cors.init_app(app)
    bcrypt.init_app(app)

    # Route racine pour tester que le serveur fonctionne
    @app.route('/', methods=['GET'])
    def index():
        """Route racine pour afficher les endpoints disponibles"""
        routes_info = {
            "message": "API Smart QCM - Serveur actif",
            "endpoints": {
                "auth": {
                    "register": "POST /api/auth/register",
                    "login": "POST /api/auth/login",
                    "logout": "POST /api/auth/logout"
                },
                "users": {
                    "profile": "GET /api/users/profile"
                },
                "documents": {
                    "upload": "POST /api/documents/upload",
                    "list": "GET /api/documents"
                },
                "ia": {
                    "generate": "POST /api/ia/generate",
                    "list": "GET /api/ia/",
                    "details": "GET /api/ia/<qcm_id>"
                }
            },
            "status": "✅ Tous les Blueprints sont enregistrés"
        }
        return jsonify(routes_info), 200

    # Enregistrement des Blueprints
    # J'ajoute /api devant les préfixes pour suivre la convention REST
    
    app.register_blueprint(auth_bp, url_prefix="/api/auth") 
    app.register_blueprint(users_bp, url_prefix="/api/users")
    app.register_blueprint(documents_bp, url_prefix='/api/documents')
    
    # 💥 Ajout du Blueprint IA 
    # C'est l'étape manquante pour activer la génération de QCM.
    if ia_bp is not None:
        app.register_blueprint(ia_bp, url_prefix='/api/ia')
        print("✅ Blueprint IA enregistré avec succès sur /api/ia")
    else:
        print("⚠️  Blueprint IA non enregistré (import échoué)") 

    # Assurez-vous que les tables sont créées lors du premier lancement ou de la migration
    with app.app_context():
        # Nécessaire si vous n'utilisez pas de système de migration avancé au début
        db.create_all() 

    return app

# Ajoutez cette partie pour lancer l'application (si elle est exécutée directement)
if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)