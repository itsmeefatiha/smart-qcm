# app.py

from dotenv import load_dotenv
load_dotenv() 

from src import create_app


# Crée l'instance de l'application
app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
    
