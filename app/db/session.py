# from sqlalchemy import create_engine
# from sqlalchemy.orm import sessionmaker

# SessionLocal = sessionmaker(autoflush=False, expire_on_commit=False)

# def init_engine(url: str):
#     engine = create_engine(url, future=True, pool_pre_ping=True)
#     return engine
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from core.config import settings

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
    """
    Yields a SQLAlchemy database session.

    This generator function creates a new database session using SessionLocal,
    yields it for use in a context (such as a dependency in FastAPI routes),
    and ensures that the session is properly closed after use.

    Yields:
        Session: An active SQLAlchemy session object.

    Example:
        async def some_route(db: Session = Depends(get_session)):
            # use db here
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()