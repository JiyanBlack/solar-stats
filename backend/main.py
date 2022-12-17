import json
import os
from datetime import datetime

from fastapi import FastAPI, Request, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from .db_operations import init_db, init_sql_files, insert_watt
from .fronius_connector import FroniusConnector
from .PGConnector import PGConnector


app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class Item(BaseModel):
    query_start_time: datetime
    query_end_time: datetime
    gap: int
    intz: str


async def update_watt() -> None:
    watt = await get_watt_from_inverter()
    app.state.realtime_watt = {
        "ts": datetime.now(),
        "watt": watt,
    }


async def get_watt_from_inverter() -> None:
    try:
        watt = app.state.fc.fetch_realtime_watt()
    except Exception as _:
        watt = 0
    return watt


@app.get("/api/save_watt")
async def save_watt(request: Request) -> dict[str, None]:
    watt = await get_watt_from_inverter()
    await insert_watt(app.state.db, watt)
    return {"watt": watt}


@app.get("/api/get_watt")
async def get_watt(request: Request, background_tasks: BackgroundTasks):
    last_updated_seconds_ago = (datetime.now() - app.state.realtime_watt["ts"]).total_seconds()
    if last_updated_seconds_ago > 3:
        background_tasks.add_task(update_watt)
    return {"watt": app.state.realtime_watt["watt"]}


@app.get("/api/get_watt_history")
async def get_watt_history(request: Request):
    pgcon = app.state.db
    query = """
        SELECT * FROM realtime_watt ORDER BY ts DESC LIMIT 1000;
    """
    return await pgcon.fetch(query)


@app.post("/api/get_aggregated_watt")
async def get_aggregated_watt(request: Request, item: Item):
    pgcon = app.state.db

    query = f"""
        SELECT * FROM timeseries_watt('{item.query_start_time}',
        '{item.query_end_time}', {item.gap}, '{item.intz}');
    """
    res = await pgcon.fetch(query)
    return json.loads(res[0]["result"])


app.mount("/", StaticFiles(directory="frontend/build/", html=True), name="static")


@app.on_event("startup")
async def startup():
    pgcon = PGConnector()
    await pgcon.connect()
    app.state.db = pgcon
    app.state.fc = FroniusConnector(os.getenv("INVERTER_HOST"))
    watt = await get_watt_from_inverter()
    app.state.realtime_watt = {
        "ts": datetime.now(),
        "watt": watt,
    }
    await init_db(pgcon)
    await init_sql_files(pgcon)
