# This file creates and stores game sessions.
# It generates room codes and initializes the session data.

import secrets

CHARACTERS = "ABCDEFGHJKLMNPQRSTUVWXYZ"

sessions = {}


def generate_code():
    while True:
        letters = []

        for i in range(4):
            letters.append(secrets.choice(CHARACTERS))

        code = "".join(letters)

        if code not in sessions:
            return code


def create_session_host():
    code = generate_code()

    sessions[code] = {
        "round": 1,
        "step": "lobby",
        "classScore": 0,
        "crews": [],
        "hostToken": secrets.token_urlsafe(16),

        "timer": {
            "endsAt": None
        },

        "r1": {
            "submissions": {},
            "votes": {},
            "final": None,
            "score": 0,
            "waterSupplies": {
                "thickWaterBags": 0,
                "wideWaterBags": 0
            },
            "hintsReleased": []
        },

        "r2": {
            "battery": 8,
            "day": 1,
            "levels": {},
            "history": []
        },

        "r3": {
            "roles": {},
            "rover": None,
            "shelters": {},
            "shelterScores": {}
        }
    }

    return {
        "code": code,
        "hostToken": sessions[code]["hostToken"]
    }
