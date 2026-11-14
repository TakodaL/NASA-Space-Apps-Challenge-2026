# This file handles events sent by team devices,
# such as submissions, votes and system level choices.

from Game.round1 import submit_round1, vote_round1
from Game.round2 import validate_level
from .connections import get_device_crew, CREW_IDS


def handle_crew_pick(session, device_id, crew_id):
    if crew_id not in CREW_IDS:
        raise ValueError("Invalid crew")

    current_crew = get_device_crew(session, device_id)

    if current_crew:
        if current_crew["id"] != crew_id:
            raise ValueError("Device already belongs to a crew")
        return current_crew

    crew = next(
        (item for item in session["crews"] if item["id"] == crew_id),
        None
    )

    if crew is None:
        crew = {
            "id": crew_id,
            "devices": [],
            "status": "Exploring"
        }
        session["crews"].append(crew)

    if device_id not in crew["devices"]:
        crew["devices"].append(device_id)

    return crew


def handle_team_event(session, device_id, data):
    crew = get_device_crew(session, device_id)

    if crew is None:
        raise ValueError("Pick a crew first")

    event = data.get("event")

    if event == "team:ready":
        crew["status"] = "ready"

    elif event == "team:submit":
        submit_round1(
            session,
            crew["id"],
            data.get("choice", ""),
            data.get("reasonId", "")
        )
        crew["status"] = "locked"

    elif event == "team:vote":
        vote_round1(
            session,
            crew["id"],
            data.get("choice", "")
        )

    elif event == "team:setLevel":
        if session["round"] != 2 or session["step"] != "plan":
            raise ValueError("Level selection is not allowed now!")

        system = data.get("system", "")
        level_id = data.get("levelId", "")

        cost = validate_level(system, level_id)

        session["r2"]["levels"][system] = {
            "levelId": level_id,
            "cost": cost
        }

    else:
        raise ValueError("Unknown team event")

    return crew
