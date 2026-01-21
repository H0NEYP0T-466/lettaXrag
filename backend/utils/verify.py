import asyncio
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.future import select
from models.models import Organization

DATABASE_URL = "postgresql+asyncpg://postgres:0000@localhost/letta"

async def verify_database():
    engine = create_async_engine(DATABASE_URL, echo=True)
    async with engine.begin() as conn:
        # Check if the table exists by executing a simple query
        result = await conn.execute(select(Organization))
        rows = result.all()
        print("Organizations table verified, rows: ", rows)

asyncio.run(verify_database())