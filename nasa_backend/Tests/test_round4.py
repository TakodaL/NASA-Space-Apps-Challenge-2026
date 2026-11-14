
from Game.round4 import calculate_bag_result,calculate_round4_winner,calculate_round4_mission_score


# Test 1: Bag result

foods = [
    "chicken_and_rice",
    "spaghetti_with_meat",
    "beef_and_gravy",
    "dried_apricot_bites",
    "chocolate_bar"
]

result = calculate_bag_result(foods)

assert result["energy"] == 12
assert result["space"] == 7
assert result["water"] == 2
assert result["points"] == 3


# Test 2: Bag with fewer points

foods = [
    "chicken_and_rice",
    "dried_apricot_bites"
]

result = calculate_bag_result(foods)

assert result["points"] == 1


# Test 3: Round 4 winner

results = {
    "crew1": {"points": 3, "energy": 12},
    "crew2": {"points": 3, "energy": 14},
    "crew3": {"points": 1, "energy": 13}
}

winner = calculate_round4_winner(results)

assert winner["winners"] == ["crew2"]
assert winner["bestPoints"] == 3


# Test 4: Mission score

results = {
    "crew1": {"points": 3, "energy": 12},
    "crew2": {"points": 1, "energy": 13}
}

score = calculate_round4_mission_score(results)

assert score == 3

print("All Round 4 tests passed!")
