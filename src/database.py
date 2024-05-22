from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

URL_DATABASE  = "mysql+pymysql://root:@localhost:3306/v2"

engine = create_engine(URL_DATABASE)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

URL_DATABASE2 = "mysql+aiomysql://root:@localhost:3306/v2"

engine2 = create_async_engine(URL_DATABASE2)

AsyncSessionLocal = sessionmaker(engine2, expire_on_commit=False, class_=AsyncSession)

Base = declarative_base()

