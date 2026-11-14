# This file defines the steps for each round
# and provides the step list used by the game logic.

ROUND1_STEPS = [
    "briefing",
    "investigate",
    "submit",
    "share",
    "decide",
    "reveal",
    "debrief"
]

ROUND2_STEPS = [
    "alert",
    "investigate",
    "plan",
    "dayResult",
    "day2Alert",
    "plan",
    "dayResult",
    "result",
    "debrief"
]

ROUND3_STEPS = [
    "alert",
    "rescuePlan",
    "rescue",
    "shelterAlert",
    "shelterBuild",
    "shelterResults",
    "debrief"
]

ROUND4_STEPS = [
    "pack",
    "reveal",
    "improve",
    "results",
    "debrief"
]

ROUND5_STEPS = [
    "clues",
    "hypothesis",
    "results",
    "debrief"
]

def get_round_steps(round_number):
    if round_number == 1:
        return ROUND1_STEPS

    elif round_number == 2:
        return ROUND2_STEPS

    elif round_number == 3:
        return ROUND3_STEPS

    elif round_number == 4:
        return ROUND4_STEPS

    elif round_number == 5:
        return ROUND5_STEPS
    return []