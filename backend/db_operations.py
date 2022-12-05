import os

from .PGConnector import PGConnector


async def init_db(pgcon: PGConnector):
    create_realtime_watt = """
        CREATE TABLE IF NOT EXISTS realtime_watt(
            id serial PRIMARY KEY,
            ts TIMESTAMPTZ NOT NULL,
            watt INTEGER NOT NULL
        );
        CREATE INDEX IF NOT EXISTS realtime_watt_ts_index ON realtime_watt (ts);
    """
    await pgcon.execute(create_realtime_watt)


async def insert_watt(pgcon: PGConnector, watt: int):
    insert_watt = f"""
        INSERT INTO realtime_watt (ts, watt) VALUES (NOW(), {watt});
    """
    await pgcon.execute(insert_watt)


async def init_sql_files(pgcon: PGConnector):
    sql_function_folder = os.path.join(os.path.dirname(__file__), "sql_functions")
    for file in os.listdir(sql_function_folder):
        if file.endswith(".sql"):
            with open(os.path.join(sql_function_folder, file), "r") as f:
                await pgcon.execute(f.read())
            print("Loaded SQL function: {}".format(file))
