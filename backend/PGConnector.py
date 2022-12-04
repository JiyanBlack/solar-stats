import os

import asyncpg


class PGConnector:
    def __init__(self) -> None:
        self.user = os.getenv("POSTGRES_USER")
        self.password = os.getenv("POSTGRES_PASSWORD")
        self.host = os.getenv("DB_HOST")
        self.port = os.getenv("DB_PORT")
        self.database = os.getenv("POSTGRES_DB")
        self._connection_pool = None
        self.conn = None

    async def connect(self):
        if not self._connection_pool:
            try:
                self._connection_pool = await asyncpg.create_pool(
                    min_size=1,
                    max_size=50,
                    command_timeout=60,
                    host=self.host,
                    port=self.port,
                    user=self.user,
                    password=self.password,
                    database=self.database,
                    max_inactive_connection_lifetime=120,
                )

            except Exception as e:
                print(e)

    async def fetch(self, query: str):
        await self.connect()
        async with self._connection_pool.acquire() as conn:
            result = await conn.fetch(query)
            return result

    async def execute(self, query: str) -> None:
        await self.connect()
        async with self._connection_pool.acquire() as conn:
            async with conn.transaction():
                await conn.execute(query)
