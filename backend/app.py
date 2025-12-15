from src import create_app
from config import Config

app = create_app()

if __name__ == "__main__":
    app.run(debug=True)

print(Config.SQLALCHEMY_DATABASE_URI)