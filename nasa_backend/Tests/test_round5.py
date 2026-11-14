
from Game.round5 import calculate_round5_score,calculate_round5_mission_score


# Test 1: Perfect hypothesis

score = calculate_round5_score(
    "flowing_water",
    ["shape", "size"]
)

assert score == 3


# Test 2: Wrong cause

score = calculate_round5_score(
    "wind",
    ["shape", "size"]
)

assert score == 2


# Test 3: False reasons

score = calculate_round5_score(
    "flowing_water",
    ["stones_red", "mars_cold"]
)

assert score == 1


# Test 4: One real reason

score = calculate_round5_score(
    "flowing_water",
    ["shape", "mars_cold"]
)

assert score == 2


# Test 5: Mission score

scores = {
    "orion": 2,
    "lyra": 3,
    "vega": 1
}

assert calculate_round5_mission_score(scores) == 3

print("All Round 5 tests passed!")
