from flask_login import UserMixin
from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.pool import QueuePool
import os
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
import streamlit as st

# Database setup
DATABASE_URL = "mysql+pymysql://root:rOOT@localhost/<cropyeild>"
if DATABASE_URL and DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

# Create engine with connection pooling
engine = create_engine(
    DATABASE_URL,
    poolclass=QueuePool,
    pool_size=5,
    max_overflow=10,
    pool_timeout=30,
    pool_recycle=1800
)

# Create scoped session factory
session_factory = sessionmaker(bind=engine)
Session = scoped_session(session_factory)

Base = declarative_base()

class User(Base, UserMixin):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    username = Column(String(80), unique=True, nullable=False)
    email = Column(String(120), unique=True, nullable=False)
    password_hash = Column(String(256), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

# Create tables
try:
    Base.metadata.create_all(engine)
except Exception as e:
    st.error(f"Error creating database tables: {str(e)}")

def get_db_session():
    """Get a new database session"""
    try:
        session = Session()
        return session
    except Exception as e:
        st.error(f"Error creating database session: {str(e)}")
        return None

def get_user_by_id(user_id):
    """Get user by ID with error handling"""
    session = get_db_session()
    if not session:
        return None

    try:
        return session.query(User).filter(User.id == user_id).first()
    except Exception as e:
        st.error(f"Database error: {str(e)}")
        return None
    finally:
        session.close()

def get_user_by_username(username):
    """Get user by username with error handling"""
    session = get_db_session()
    if not session:
        return None

    try:
        return session.query(User).filter(User.username == username).first()
    except Exception as e:
        st.error(f"Database error: {str(e)}")
        return None
    finally:
        session.close()

def create_user(username, email, password):
    """Create new user with error handling"""
    session = get_db_session()
    if not session:
        return None

    try:
        user = User(username=username, email=email)
        user.set_password(password)
        session.add(user)
        session.commit()
        return user
    except Exception as e:
        session.rollback()
        st.error(f"Error creating user: {str(e)}")
        return None
    finally:
        session.close()
