
# This file contains the logic for Round 4.
# It calculates the food bag values, checks the limits,
# determines the winning team and calculates the mission score.

from pathlib import Path
import json

DATA_PATH = Path(__file__).resolve().parent.parent / "Data" / "round4.json"

with open(DATA_PATH, "r", encoding="utf-8") as file:
    ROUND4_DATA = json.load(file)


def calculate_bag_result(selected_foods):
    foods = ROUND4_DATA["foods"]

    if not isinstance(selected_foods, list):
        raise ValueError("Food selection must be a list!")

    if len(selected_foods) != len(set(selected_foods)):
        raise ValueError("A food can only be selected once!")

    space = 0
    water = 0
    energy = 0

    for food_id in selected_foods:
        if food_id not in foods:
            raise ValueError("Invalid food!")

        food = foods[food_id]

        space += food["space"]
        water += food["water"]
        energy += food["energy"]

    energy_ok = 12 <= energy <= 14
    space_ok = space <= 9
    water_ok = water <= 2

    limits_passed = sum([
        energy_ok,
        space_ok,
        water_ok
    ])

    if limits_passed == 3:
        points = 3
    elif limits_passed == 2:
        points = 1
    else:
        points = 0

    return {
        "foods": selected_foods,
        "space": space,
        "water": water,
        "energy": energy,
        "energy_ok": energy_ok,
        "space_ok": space_ok,
        "water_ok": water_ok,
        "points": points
    }


def calculate_round4_winner(team_results):
    if not team_results:
        raise ValueError("There are no team results!")

    best_points = max(
        result["points"] for result in team_results.values()
    )

    best_teams = [
        crew_id
        for crew_id, result in team_results.items()
        if result["points"] == best_points
    ]

    best_energy = max(
        team_results[crew_id]["energy"]
        for crew_id in best_teams
    )

    winners = [
        crew_id
        for crew_id in best_teams
        if team_results[crew_id]["energy"] == best_energy
    ]

    return {
        "bestPoints": best_points,
        "bestEnergy": best_energy,
        "winners": winners
    }


def calculate_round4_mission_score(team_results):
    winner = calculate_round4_winner(team_results)
    return winner["bestPoints"]
