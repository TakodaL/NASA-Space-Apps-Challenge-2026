# This file contains the logic for Round 5.
# It checks the team's hypotheses and evidence,
# calculates the team scores and the mission score.

from pathlib import Path
import json


DATA_PATH = Path(__file__).resolve().parent.parent / "Data" / "round5.json"

with open(DATA_PATH, "r", encoding="utf-8") as file:
    ROUND5_DATA = json.load(file)


def validate_hypothesis(cause, reasons):
    causes = ROUND5_DATA["causes"]
    clues = ROUND5_DATA["clues"]
    required_reasons = ROUND5_DATA["hypothesis"]["requiredReasons"]

    if cause not in causes:
        raise ValueError("Invalid cause!")

    if len(reasons) != required_reasons:
        raise ValueError("Choose exactly 2 reasons!")

    if len(set(reasons)) != len(reasons):
        raise ValueError("You cannot choose the same reason twice!")

    for reason in reasons:
        if reason not in clues:
            raise ValueError("Invalid reason!")


def calculate_round5_score(cause, reasons):
    validate_hypothesis(cause, reasons)

    scoring = ROUND5_DATA["scoring"]
    clues = ROUND5_DATA["clues"]

    score = 0

    if cause == scoring["correctCause"]:
        score += scoring["causePoints"]

    for reason in reasons:
        if clues[reason]["isEvidence"]:
            score += scoring["evidencePoints"]

    return min(score, scoring["maxPoints"])


def calculate_round5_mission_score(team_scores):
    if not team_scores:
        raise ValueError("No team scores found!")

    return max(team_scores.values())
