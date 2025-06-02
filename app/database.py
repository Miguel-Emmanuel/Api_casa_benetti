from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

# Cambia los valores de usuario, contraseña, host y base de datos según tu configuración de MySQL
SQLALCHEMY_DATABASE_URL = "mysql+mysqlconnector://benetti_user:TuPasswordSegura123@localhost/pagos_benetti"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
