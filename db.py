from sqlalchemy import create_engine, Column, Integer, String, Text, JSON, TIMESTAMP, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from config import DATABASE_URL

# ✅ Base must be declared before model classes
Base = declarative_base()

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

class EmailLog(Base):
    __tablename__ = "emails"

    id = Column(Integer, primary_key=True, index=True)
    message_id = Column(String, unique=True, index=True)
    sender = Column(String, nullable=False)
    subject = Column(String, nullable=False)
    body = Column(Text, nullable=False)
    predictions = Column(JSON, nullable=False)  # dict {intent: score}
    reply = Column(Text, nullable=False)
    created_at = Column(TIMESTAMP, server_default=func.now())

def init_db():
    Base.metadata.create_all(bind=engine)
