# This file handles events sent by the host,
# such as advancing or going back through game steps.

from Game.game_logic import host_advance, host_back
from Game.round1 import set_final_round1


def handle_host_event(session, data):
    event = data.get("event")

    if event == "host:advance":
        host_advance(session)

    elif event == "host:back":
        host_back(session)

    elif event == "host:setFinal":
        set_final_round1(
            session,
            data.get("choice", "")
        )

    elif event == "host:addTime":
        if session["round"] != 1 or session["step"] != "investigate":
            raise ValueError("Time can only be added during Investigate!")

        if session["timer"]["endsAt"] is None:
            raise ValueError("There is no active timer!")

        session["timer"]["endsAt"] += 60

    elif event == "host:releaseHint":
        if session["round"] != 1 or session["step"] != "investigate":
            raise ValueError("The hint can only be released during Investigate!")

        if "water" not in session["r1"]["hintsReleased"]:
            session["r1"]["hintsReleased"].append("water")

    elif event == "host:activateDay":
        if session["round"] != 2 or session["step"] != "plan":
            raise ValueError("A day can only be activated during Round 2 plan!")

        if session["r2"]["day"] not in [1, 2]:
            raise ValueError("Invalid day!")

    else:
        raise ValueError("Unknown host event")
