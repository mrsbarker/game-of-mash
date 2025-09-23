
from sqlalchemy import String, Float, UniqueConstraint, create_engine, select
from sqlalchemy.orm import declarative_base, DeclarativeBase, Mapped, mapped_column, scoped_session, sessionmaker
from sqlalchemy.ext.declarative import ConcreteBase
# create MASH database

engine = create_engine("sqlite:///instance/mashoptions.db")
db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))
Base = declarative_base()
Base.query = db_session.query_property()

class Spouse(Base):
    __tablename__ = "spouse"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(unique=True)
    sex: Mapped[str] = mapped_column(String(1))

class Vehicle(Base):
    __tablename__ = "vehicle"
    id: Mapped[int] = mapped_column(primary_key=True)
    model: Mapped[str]
    make: Mapped[str] 
    desc: Mapped[str|None]
    UniqueConstraint("vehicle.make", "vehicle.model", "unq1")

class Career(Base):
    __tablename__ = "career"
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(unique=True)

class Salary(Base):
    __tablename__ = "salary"
    id: Mapped[int] = mapped_column(primary_key=True)
    amount: Mapped[float] = mapped_column(Float(2), unique=True)
    
def create_db():
    Base.metadata.create_all(engine)

