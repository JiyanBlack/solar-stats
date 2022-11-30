from fastapi import FastAPI, Request

from .db_operations import init_db, insert_watt
from .fronius_connector import FroniusConnector
from .PGConnector import PGConnector
import os
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

app = FastAPI()
origins = ["http://localhost:3000", "localhost:3000"]


app.add_middleware(
    CORSMiddleware, allow_origins=origins, allow_credentials=True, allow_methods=["*"], allow_headers=["*"]
)


app.mount("/", StaticFiles(directory="frontend/build/", html=True), name="static")


@app.get("/get_watt")
async def get_watt(request: Request):
    try:
        watt = app.state.fc.fetch_realtime_watt()
    except Exception as e:
        watt = 0
    await insert_watt(app.state.db, watt)
    return {"watt": watt}


@app.on_event("startup")
async def startup():
    pgcon = PGConnector()
    await pgcon.connect()
    app.state.db = pgcon
    app.state.fc = FroniusConnector(os.getenv("INVERTER_HOST"))
    await init_db(pgcon)