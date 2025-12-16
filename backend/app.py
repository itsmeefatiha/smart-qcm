from src import create_app
from config import Config
from src.exams import exams_bp

app = create_app()

# Enregistrer le blueprint exams
app.register_blueprint(exams_bp, url_prefix="/exams")

if __name__ == "__main__":
    app.run(debug=True)
