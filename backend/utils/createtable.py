import asyncio
from sqlalchemy. ext.asyncio import create_async_engine
from letta.orm.sqlalchemy_base import SqlalchemyBase

DATABASE_URL = "postgresql+asyncpg://postgres:0000@127.0.0.1:5432/letta"

async def create_tables():
    engine = create_async_engine(DATABASE_URL, echo=True)
    
    async with engine.begin() as conn:
        await conn.run_sync(SqlalchemyBase.metadata.create_all)
    
    await engine.dispose()
    print("✅ All tables created successfully!")

if __name__ == "__main__": 
    asyncio.run(create_tables())