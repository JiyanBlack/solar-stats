from fastapi import FastAPI, Request

from .db_operations import init_db, insert_watt
from .fronius_connector import FroniusConnector
from .PGConnector import PGConnector

app = FastAPI()


@app.get("/")
async def root(request: Request):
    return {"message": "Hello World"}


@app.get("/get_watt")
async def get_watt(request: Request):
    fc = FroniusConnector("192.168.0.227")
    try:
        watt = fc.fetch_realtime_watt()
    except Exception as e:
        watt = 0
    await insert_watt(app.state.db, watt)
    return {"watt": watt}


@app.on_event("startup")
async def startup():
    pgcon = PGConnector()
    await pgcon.connect()
    app.state.db = pgcon
    await init_db(pgcon)
