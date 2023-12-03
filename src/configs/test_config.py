from fastapi.testclient import TestClient
from sqlalchemy import StaticPool
from sqlalchemy.engine import create_engine
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker

from src.db.configs import get_session
from src.main import app

mock_engine = create_engine("sqlite:///./test.db", echo=True, poolclass=StaticPool)
engine = create_async_engine("sqlite+aiosqlite:///./test.db", echo=True)
TestingSessionLocal = async_sessionmaker(
    bind=engine, class_=AsyncSession, autoflush=False
)


async def override_get_session():
    async with TestingSessionLocal() as session:
        yield session


app.dependency_overrides[get_session] = override_get_session
client = TestClient(app)
