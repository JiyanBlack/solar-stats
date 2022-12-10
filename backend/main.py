import os
from datetime import datetime

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, validator

from .db_operations import init_db, init_sql_files, insert_watt
from .fronius_connector import FroniusConnector
from .PGConnector import PGConnector
import json

app = FastAPI()


app.add_middleware(
    CORSMiddleware, allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"]
)


class Item(BaseModel):
    query_start_time: datetime
    query_end_time: datetime
    gap: int
    intz: str


@app.get("/api/save_watt")
async def save_watt(request: Request):
    try:
        watt = app.state.fc.fetch_realtime_watt()
    except Exception as e:
        watt = 0
    await insert_watt(app.state.db, watt)
    return {"watt": watt}


@app.get("/api/get_watt")
async def get_watt(request: Request):
    try:
        watt = app.state.fc.fetch_realtime_watt(3)
    except Exception as e:
        watt = 0
    return {"watt": watt}


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
        SELECT * FROM timeseries_watt('{item.query_start_time}', '{item.query_end_time}', {item.gap}, '{item.intz}');
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
    await init_db(pgcon)
    await init_sql_files(pgcon)
