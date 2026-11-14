# This file handles WebSocket connections
# and routes messages between the host, server and team devices.

from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from session_store import sessions
import json
from pathlib import Path
from .Websocket_utils.connections import device_connections, host_connections, get_device_crew
from .Websocket_utils.lobby import send_to_all, update_lobby
from .Websocket_utils.host_events import handle_host_event
from .Websocket_utils.team_events import handle_crew_pick, handle_team_event

router = APIRouter(tags=["WebSocket"])

BASE_DIR = Path(__file__).resolve().parent.parent
ROUND1_FILE = BASE_DIR / "Data" / "round1.json"

with open(ROUND1_FILE, "r", encoding="utf-8") as file:
    ROUND1_DATA = json.load(file)

ROUND2_FILE = BASE_DIR / "Data" / "round2.json"

with open(ROUND2_FILE, "r", encoding="utf-8") as file:
    ROUND2_DATA = json.load(file)

def get_session_state(session):
    step_data = None

    if session["round"] == 1:
        step_data = ROUND1_DATA

    elif session["round"] == 2:
        step_data = ROUND2_DATA

    return {
        "event": "session:state",
        "round": session["round"],
        "step": session["step"],
        "stepData": step_data,
        "timer": session.get("timer", {"endsAt": None}),
        "classScore": session["classScore"]
    }



async def broadcast_state(code):
    session = sessions[code]
    await send_to_all(code, get_session_state(session))


async def send_error(websocket, error):
    await websocket.send_json({
        "event": "error",
        "message": str(error)
    })


@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()

    code = None
    device_id = None
    is_host = False

    try:
        first_message = await websocket.receive_json()

        event = first_message.get("event")
        code = first_message.get("code")

        if code not in sessions:
            await websocket.close(code=1008)
            return

        session = sessions[code]
        device_connections.setdefault(code, {})

        if event == "host:join":
            if first_message.get("hostToken") != session["hostToken"]:
                await websocket.close(code=1008)
                return

            is_host = True
            host_connections[code] = websocket

        elif event == "device:join":
            device_id = first_message.get("deviceId")

            if not device_id:
                await websocket.close(code=1008)
                return

            device_connections[code][device_id] = websocket

        else:
            await websocket.close(code=1008)
            return

        await websocket.send_json(get_session_state(session))

        if not is_host:
            crew = get_device_crew(session, device_id)

            if crew:
                await websocket.send_json({
                    "event": "you:state",
                    "crewId": crew["id"],
                    "job": crew.get("job"),
                    "privateData": None
                })

            await update_lobby(code, sessions)

        while True:
            data = await websocket.receive_json()
            event = data.get("event")

            try:
                if event.startswith("host:"):
                    if not is_host:
                        raise ValueError("Only host can do this")

                    handle_host_event(session, data)
                    await broadcast_state(code)

                elif event == "crew:pick":
                    if is_host:
                        raise ValueError("Only devices can pick a crew")

                    handle_crew_pick(
                        session,
                        device_id,
                        data.get("crewId")
                    )
                    await update_lobby(code, sessions)

                elif event.startswith("team:"):
                    if is_host:
                        raise ValueError("Only devices can do this")

                    crew = handle_team_event(session, device_id, data)

                    await send_to_all(code, {
                    "event": "crew:status",
                    "crewId": crew["id"],
                    "status": crew["status"]
                    })

                    if event == "team:vote":
                        votes = session["r1"]["votes"]

                        tally = {
                            "A": sum(1 for vote in votes.values() if vote == "A"),
                            "B": sum(1 for vote in votes.values() if vote == "B"),
                            "C": sum(1 for vote in votes.values() if vote == "C")
                        }

                        await send_to_all(code, {
                            "event": "tally:update",
                            **tally
                        })

                else:
                    raise ValueError("Unknown event")

            except ValueError as error:
                await send_error(websocket, error)

    except WebSocketDisconnect:
        pass

    finally:
        if code and is_host:
            if host_connections.get(code) is websocket:
                del host_connections[code]

        elif code and device_id:
            if device_connections.get(code, {}).get(device_id) is websocket:
                del device_connections[code][device_id]
                await update_lobby(code, sessions)
