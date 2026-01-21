@echo off
call venv\Scripts\activate
set LETTA_STORAGE_CONNECTOR=postgresql
set LETTA_PG_URI=postgresql+asyncpg://postgres:0000@localhost:5432/letta
set OPENAI_API_KEY=ak_1VV0ZF2Zq2iG91k2JR0yn6SA7X690
letta server
pause