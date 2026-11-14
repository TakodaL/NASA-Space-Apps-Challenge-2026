# This file contains the logic for Round 1.
# It validates the location choices, saves team submissions and votes,
# and calculates the final score.

def round1(team_name: str, chosen_location: str):
    location = chosen_location.upper()

    options = {
        "A": "Mons Mouton Plateau",
        "B": "Malapert Massif",
        "C": "Nobile Rim 1"
    }

    if location not in options:
        raise ValueError("Choose A, B or C!")

    return {
        "team_name": team_name,
        "chosen_location": location,
        "location_name": options[location]
    }


def submit_round1(session, crew_id: str, choice: str, reason_id: str):
    if session["round"] != 1:
        raise ValueError("This is not Round 1!")

    if session["step"] != "submit":
        raise ValueError("Submissions are not allowed now!")

    crew_exists = any(crew["id"] == crew_id for crew in session["crews"])

    if not crew_exists:
        raise ValueError("Crew not found!")

    choice = choice.upper()

    if choice not in ["A", "B", "C"]:
        raise ValueError("Choose A, B or C!")

    if not reason_id:
        raise ValueError("A reason is required!")

    session["r1"]["submissions"][crew_id] = {
        "choice": choice,
        "reasonId": reason_id
    }

    return session


def vote_round1(session, crew_id: str, choice: str):
    if session["round"] != 1 or session["step"] != "decide":
        raise ValueError("Voting is not allowed now!")

    crew_exists = any(crew["id"] == crew_id for crew in session["crews"])

    if not crew_exists:
        raise ValueError("Crew not found!")

    choice = choice.upper()

    if choice not in ["A", "B", "C"]:
        raise ValueError("Choose A, B or C!")

    session["r1"]["votes"][crew_id] = choice

    return session


def set_final_round1(session, choice: str):
    if session["round"] != 1 or session["step"] != "decide":
        raise ValueError("The final decision cannot be set now!")

    if session["r1"]["final"] is not None:
        raise ValueError("The final decision has already been set!")

    choice = choice.upper()

    if choice not in ["A", "B", "C"]:
        raise ValueError("Choose A, B or C!")

    points = {
        "A": 3,
        "C": 2,
        "B": 1
    }

    water_supplies = {
        "A": {
            "thickWaterBags": 1,
            "wideWaterBags": 2
        },
        "C": {
            "thickWaterBags": 1,
            "wideWaterBags": 1
        },
        "B": {
            "thickWaterBags": 0,
            "wideWaterBags": 1
        }
    }

    session["r1"]["final"] = choice
    session["r1"]["score"] = points[choice]
    session["r1"]["waterSupplies"] = water_supplies[choice].copy()

    session["classScore"] += points[choice]

    return session
