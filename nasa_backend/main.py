from fastapi import FastAPI
from Routers import sessions, websocket

app = FastAPI()

app.include_router(sessions.router)
app.include_router(websocket.router)