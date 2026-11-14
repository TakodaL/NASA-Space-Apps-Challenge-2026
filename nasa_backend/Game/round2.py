# This file contains the logic for Round 2.
# It manages the battery, system levels, storm days,
# survival results and round score.

from pathlib import Path
import json
import random

DATA_PATH = Path(__file__).resolve().parent.parent / "Data" / "round2.json"

with open(DATA_PATH, "r", encoding="utf-8") as file:
    ROUND2_DATA = json.load(file)



def initialize_round2(session):
    if "stormDays" not in session["r2"]:
        session["r2"]["stormDays"] = random.choices(
            [2, 3],
            weights=[70, 30]
        )[0]

    if "foodBagAvailable" not in session["r2"]:
        session["r2"]["foodBagAvailable"] = True

    if "score" not in session["r2"]:
        session["r2"]["score"] = 0

    return session



def validate_level(system: str, level_id: str):
    systems = ROUND2_DATA["systems"]

    if system not in systems:
        raise ValueError("Invalid system!")

    levels = systems[system]["levels"]

    if level_id not in levels:
        raise ValueError("Invalid level!")

    return levels[level_id]["cost"]


def round2(
    number_of_teams: int,
    life_support: int,
    food: int,
    temperature: int,
    comms: int,
    battery: int
):
    if number_of_teams < 1 or number_of_teams > 4:
        raise ValueError("There have to be between 1 and 4 teams!")

    if life_support not in [0, 1, 2]:
        raise ValueError("Life Support must be 0, 1 or 2!")

    if food not in [0, 1, 2]:
        raise ValueError("Food must be 0, 1 or 2!")

    if temperature not in [0, 1, 2]:
        raise ValueError("Temperature must be 0, 1 or 2!")

    if comms not in [0, 1, 2]:
        raise ValueError("Communications must be 0, 1 or 2!")

    total_energy = life_support + food + temperature + comms

    if total_energy > battery:
        raise ValueError("Not enough battery energy!")

    return {
        "life_support": life_support,
        "food": food,
        "temperature": temperature,
        "comms": comms,
        "total_energy": total_energy,
        "remaining_energy": battery - total_energy
    }


def calculate_day_result(life_support: int, temperature: int):
    survived = life_support >= 1 and temperature >= 1
    return {"survived": survived}


def calculate_round2_score(
    day1_survived: bool,
    day2_survived: bool,
    day3_survived: bool = None,
    storm_days: int = 2
):
    if storm_days not in [2, 3]:
        raise ValueError("Storm duration must be 2 or 3 days!")

    if day1_survived is False:
        return 0

    if not day2_survived:
        return 1

    if storm_days == 3 and not day3_survived:
        return 1

    return 3


def update_class_score(session, round_score):
    session["classScore"] += round_score
    return session


def save_day_result(
    session,
    day,
    life_support,
    temperature,
    total_energy,
    food=None
):
    storm_days = session["r2"].get("stormDays", 2)

    if day not in [1, 2, 3] or day > storm_days:
        raise ValueError("Invalid storm day!")

    if day != len(session["r2"]["history"]) + 1:
        raise ValueError("Days must be completed in order!")

    result = calculate_day_result(life_support, temperature)

    update_battery(session, total_energy)

    if food == 0:
        session["r2"]["foodBagAvailable"] = False

    session["r2"]["history"].append({
        "day": day,
        "survived": result["survived"],
        "energy_used": total_energy
    })

    return session


def end_round2(session):
    storm_days = session["r2"].get("stormDays", 2)
    history = session["r2"]["history"]

    if len(history) != storm_days:
        raise ValueError("All storm days must have results!")

    day_results = {
        result["day"]: result["survived"]
        for result in history
    }

    day1 = day_results.get(1)
    day2 = day_results.get(2)
    day3 = day_results.get(3)

    if day1 is None or day2 is None:
        raise ValueError("Both first days must have results!")

    score = calculate_round2_score(
        day1,
        day2,
        day3,
        storm_days
    )

    if session["r2"].get("score", 0) != 0:
        raise ValueError("Round 2 score has already been added!")

    session["r2"]["score"] = score
    update_class_score(session, score)

    return session


def update_battery(session, total_energy):
    if total_energy < 0:
        raise ValueError("Energy cannot be negative!")

    if total_energy > session["r2"]["battery"]:
        raise ValueError("Not enough battery energy!")

    session["r2"]["battery"] -= total_energy

    return session
