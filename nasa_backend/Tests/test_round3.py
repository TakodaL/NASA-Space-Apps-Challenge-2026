
from Game.round3 import calculate_rescue_result, calculate_shelter_score


# Test 1: Rescue with battery

travel_times = {
    1: {"walking": 4, "rover": 3},
    2: {"walking": 7, "rover": 5},
    3: {"walking": 11, "rover": 6}
}

result = calculate_rescue_result(3, 1, travel_times)

assert result["results"][1]["safe"] is True
assert result["results"][2]["safe"] is True
assert result["results"][3]["safe"] is True
assert result["score"] == 3


# Test 2: Rescue without battery

result = calculate_rescue_result(3, 0, travel_times)

assert result["results"][3]["safe"] is False
assert result["score"] == 2


# Test 3: Shelter score

inventory = {
    "thick_water_bag": 1,
    "wide_water_bag": 2,
    "packed_food_bag": 1,
    "wide_clothing_bag": 1,
    "empty_storage_bag": 1
}

placements = [
    {"item": "thick_water_bag", "area": "A"},
    {"item": "wide_water_bag", "area": "B"},
    {"item": "packed_food_bag", "area": "C"}
]

result = calculate_shelter_score(placements, inventory)

assert result["totalScore"] == 5

print("All Round 3 tests passed!")
