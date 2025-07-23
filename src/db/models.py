from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Float, DateTime, LargeBinary, \
    BigInteger
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession

from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.orm import declarative_base, sessionmaker
from dotenv import load_dotenv
import os

load_dotenv()
DATABASE_URL = os.getenv('DATABASE_URL')

Base = declarative_base()
engine = create_async_engine(DATABASE_URL)
AsyncSessionLocal = sessionmaker(bind=engine)


# # Настройка SSL-контекста
# ssl_context = ssl.create_default_context()
# ssl_context.check_hostname = False
# ssl_context.verify_mode = ssl.CERT_NONE
#
# ssl_context.load_verify_locations(cafile="путь r ca")
#
# engine = create_async_engine(
#     DATABASE_URL,
#     echo=True,
#     connect_args={"ssl_disabled": True}
# )
#
# AsyncSessionLocal = sessionmaker(
#     engine, expire_on_commit=False, class_=AsyncSession
# )

class Image(Base):
    __tablename__ = 'images'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    image_data = Column(LargeBinary, nullable=False)

class Department(Base):
    __tablename__ = 'departments'
    department_id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)

class Role(Base):
    __tablename__ = 'roles'
    role_id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    department_id = Column(Integer, ForeignKey('departments.department_id'), nullable=True)

class Player(Base):
    __tablename__ = 'players'
    player_id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    password = Column(String(100), nullable=False)
    tg_id = Column(BigInteger, unique=True, nullable=False)


class CaseRequirement(Base):
    __tablename__ = 'case_requirements'
    case_id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    description = Column(String(1000), nullable=True)
    required_it_points = Column(Integer)
    required_hr_points = Column(Integer)
    required_ec_points = Column(Integer)
    required_bp_points = Column(Integer)


class Session(Base):
    __tablename__ = 'sessions'
    session_id = Column(Integer, primary_key=True, autoincrement=True)
    password = Column(String(100), nullable=False)
    count_players = Column(Integer)
    case_id = Column(Integer, ForeignKey('case_requirements.case_id'))
    case = relationship("CaseRequirement")


class SessionPlayer(Base):
    __tablename__ = 'session_players'
    session_id = Column(Integer, ForeignKey('sessions.session_id'), primary_key=True)
    player_id = Column(Integer, ForeignKey('players.player_id'), primary_key=True)
    role_id = Column(Integer, ForeignKey('roles.role_id'))
    is_positive = Column(Boolean)


class GameCurrency(Base):
    __tablename__ = 'game_currency'
    session_id = Column(Integer, ForeignKey('sessions.session_id'), primary_key=True)
    remains = Column(Integer, default=1000)


class Tool(Base):
    __tablename__ = 'tools'
    tool_id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    description = Column(String(1000), nullable=True)
    cost = Column(Integer, nullable=False)
    it_points = Column(Integer)
    hr_points = Column(Integer)
    ec_points = Column(Integer)
    bp_points = Column(Integer)
    department_id = Column(Integer, ForeignKey('departments.department_id'))


class ManagementCard(Base):
    __tablename__ = 'management_cards'
    card_id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    description = Column(String(1000), nullable=True)
    it_effect = Column(Integer)
    hr_effect = Column(Integer)
    ec_effect = Column(Integer)
    bp_effect = Column(Integer)


class GameResult(Base):
    __tablename__ = 'game_results'
    result_id = Column(Integer, primary_key=True, autoincrement=True)
    session_id = Column(Integer, ForeignKey('sessions.session_id'))
    start_time = Column(DateTime)
    end_time = Column(DateTime)
    total_it_points = Column(Integer)
    total_hr_points = Column(Integer)
    total_ec_points = Column(Integer)
    total_bp_points = Column(Integer)
    is_successful = Column(Boolean)


class PlayerStatistics(Base):
    __tablename__ = 'player_statistics'
    player_id = Column(Integer, ForeignKey('players.player_id'), primary_key=True)
    total_games_played = Column(Integer, default=0)
    total_wins = Column(Integer, default=0)
    total_losses = Column(Integer, default=0)
    average_it_points = Column(Float, default=0)
    average_hr_points = Column(Float, default=0)
    average_ec_points = Column(Float, default=0)
    average_bp_points = Column(Float, default=0)


async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
