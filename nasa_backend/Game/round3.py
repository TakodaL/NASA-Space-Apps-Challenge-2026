
# This file contains the logic for Round 3.
# It calculates the rescue results, manages the rover battery,
# handles shelter inventory and calculates shelter scores.

import random

def initialize_rescue_times(session):
    if "travelTimes" not in session["r3"]:
        times = [
            {"walking": 4, "rover": 3},
            {"walking": 7, "rover": 5},
            {"walking": 11, "rover": 6}
        ]

        random.shuffle(times)

        session["r3"]["travelTimes"] = {
            1: times[0],
            2: times[1],
            3: times[2]
        }

    return session["r3"]["travelTimes"]


def calculate_rescue_result(rover_explorer, battery, travel_times):
    if battery < 0:
        raise ValueError("Battery cannot be negative!")

    if battery >= 1 and rover_explorer not in [1, 2, 3]:
        raise ValueError("Choose Explorer 1, 2 or 3!")

    if battery == 0:
        rover_explorer = None

    results = {}

    for explorer in [1, 2, 3]:
        if explorer == rover_explorer:
            time = travel_times[explorer]["rover"]
        else:
            time = travel_times[explorer]["walking"]

        results[explorer] = {
            "time": time,
            "safe": time <= 8
        }

    score = sum(
        1 for result in results.values()
        if result["safe"]
    )

    return {
        "results": results,
        "score": score
    }



from pathlib import Path
import json

DATA_PATH = Path(__file__).resolve().parent.parent / "Data" / "round3.json"

with open(DATA_PATH, "r", encoding="utf-8") as file:
    ROUND3_DATA = json.load(file)


def get_shelter_inventory(session):
    location = session["r1"]["final"]

    if location not in ["A", "B", "C"]:
        raise ValueError("Round 1 location has not been selected!")

    objects = ROUND3_DATA["shelter"]["objects"]

    inventory = {}

    for item, data in objects.items():
        if "availableBySite" in data:
            inventory[item] = data["availableBySite"][location]
        else:
            inventory[item] = data["available"]

    if not session["r2"].get("foodBagAvailable", True):
        inventory["packed_food_bag"] = 0

    return inventory



def calculate_shelter_score(placements, inventory):
    if len(placements) != 3:
        raise ValueError("Each crew must place exactly 3 objects!")

    inventory = inventory.copy()

    area_layers = {
        "A": 0,
        "B": 0,
        "C": 0
    }

    for placement in placements:
        item = placement["item"]
        area = placement["area"]

        if item not in inventory or inventory[item] <= 0:
            raise ValueError("Invalid or unavailable item!")

        inventory[item] -= 1

        if item in ["thick_water_bag", "packed_food_bag"]:
            if area not in ["A", "B", "C"]:
                raise ValueError("Invalid area!")

            area_layers[area] += 2

        elif item == "empty_storage_bag":
            if area not in ["A", "B", "C"]:
                raise ValueError("Invalid area!")

        elif item in ["wide_water_bag", "wide_clothing_bag"]:
            if area == "A":
                area_layers["A"] += 1
                area_layers["B"] += 1
            elif area == "B":
                area_layers["B"] += 1
                area_layers["C"] += 1
            else:
                raise ValueError("Wide items must cover A+B or B+C!")

    area_points = {}

    for area, layers in area_layers.items():
        area_points[area] = min(layers, 2)

    total_score = sum(area_points.values())

    return {
        "layers": area_layers,
        "areaPoints": area_points,
        "totalScore": total_score
    }


def save_rescue_result(session, rover_explorer):
    if session["round"] != 3 or session["step"] != "rescue":
        raise ValueError("Rescue result cannot be saved now!")

    if "rescueResults" in session["r3"]:
        raise ValueError("Rescue result has already been saved!")

    battery = session["r2"]["battery"]
    travel_times = initialize_rescue_times(session)

    result = calculate_rescue_result(
        rover_explorer,
        battery,
        travel_times
    )

    if battery >= 1:
        session["r2"]["battery"] -= 1

    session["r3"]["rover"] = rover_explorer if battery >= 1 else None
    session["r3"]["rescueResults"] = result["results"]
    session["r3"]["rescueScore"] = result["score"]

    session["classScore"] += result["score"]

    return session


def save_shelter_result(session, crew_id, placements):
    if session["round"] != 3 or session["step"] != "shelterBuild":
        raise ValueError("Shelter result cannot be saved now!")

    crew_exists = any(
        crew["id"] == crew_id for crew in session["crews"]
    )

    if not crew_exists:
        raise ValueError("Crew not found!")

    if crew_id in session["r3"]["shelters"]:
        raise ValueError("Shelter has already been submitted!")

    inventory = get_shelter_inventory(session)

    result = calculate_shelter_score(placements, inventory)

    session["r3"]["shelters"][crew_id] = placements
    session["r3"]["shelterScores"][crew_id] = result["totalScore"]

    return session


def end_round3(session):
    if session["round"] != 3:
        raise ValueError("This is not Round 3!")

    if "rescueScore" not in session["r3"]:
        raise ValueError("Rescue result is missing!")

    if session["r3"].get("shelterMissionScore") is not None:
        raise ValueError("Round 3 score has already been added!")

    crew_ids = [crew["id"] for crew in session["crews"]]

    for crew_id in crew_ids:
        if crew_id not in session["r3"]["shelterScores"]:
            raise ValueError("All crews must submit their shelters!")

    if not session["r3"]["shelterScores"]:
        raise ValueError("No shelter results found!")

    best_score = max(session["r3"]["shelterScores"].values())

    session["r3"]["shelterMissionScore"] = best_score
    session["classScore"] += best_score

    return session
