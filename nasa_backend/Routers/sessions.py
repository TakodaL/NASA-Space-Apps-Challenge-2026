# This file contains the session API endpoints.
# It allows the host to create a new session
# and retrieve information about an existing session.

from fastapi import APIRouter, HTTPException
from session_store import create_session_host, sessions

router = APIRouter(prefix="/sessions", tags=["Sessions"])

@router.post("/")
def create_session():
    return create_session_host()

@router.get("/{code}")
def get_session(code: str):
    if code not in sessions:
        raise HTTPException(status_code = 404, detail = "Session not found!")

    session = sessions[code]

    return {
        "code": code,
        "round": session["round"],
        "step": session["step"],
        "classScore": session["classScore"],
        "crews": session["crews"]
    }