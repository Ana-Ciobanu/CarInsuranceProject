from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.core.config import settings

raw = settings.DATABASE_URL
if raw.startswith("postgresql://"):
    sqla_url = "postgresql+psycopg://" + raw[len("postgresql://"):]
else:
    sqla_url = raw 

engine = create_engine(
    sqla_url,
    echo=settings.SQL_ECHO,
    pool_pre_ping=settings.POOL_PRE_PING,
    pool_size=settings.POOL_SIZE,
    connect_args={"connect_timeout": settings.DB_TIMEOUT},
)

SessionLocal = sessionmaker(
    bind=engine,
    autocommit=False,
    autoflush=False,
    expire_on_commit=False,
)

def get_session():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()