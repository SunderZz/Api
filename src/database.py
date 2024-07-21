from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

URL_DATABASE2 = "mysql+aiomysql://root:@localhost:3306/nougainv2"

engine2 = create_async_engine(
    URL_DATABASE2,
    echo=True,
    pool_size=10,
    max_overflow=20,
    pool_recycle=1800,
    pool_timeout=30,
    echo_pool=True,
)
AsyncSessionLocal = sessionmaker(engine2, expire_on_commit=False, class_=AsyncSession)

Base = declarative_base()


async def get_db():
    async with AsyncSessionLocal() as session:
        yield session
        await session.commit()
