# %%
""" Database configuration"""
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker
SQLALCHEMY_DATABASE_URL = "sqlite:///./movies.db"
# # Creer un moteur de base de donnees (engine) qui etablit la connexion avec notre base SQLite (movies.db)
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
# %%
# Definir SessionLocal qui permet de creer des sessions pour interagir avec la base de sonnees
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Definir Base, qui servira de classe de base pour nos modeles SQLAlchemy.
Base = declarative_base()

if __name__ == "__main__":
    try:
        with engine.connect() as conn:
            print("Connexion a la base de donnees reussie.")
    except Exception as e:
        print(f"Erreur de connexion a la base de donnees: {e}")
# %%
