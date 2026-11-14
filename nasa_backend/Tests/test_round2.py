
from Game.round2 import round2,calculate_day_result,calculate_round2_score,save_day_result,end_round2
from Routers.Websocket_utils.team_events import handle_team_event


def create_session():
    return {
        "round": 2,
        "step": "plan",
        "classScore": 0,
        "r2": {
            "battery": 8,
            "day": 1,
            "levels": {},
            "history": []
        }
    }


# Test 1: Energy allocation
result = round2(2, 2, 1, 2, 1, 8)

assert result["total_energy"] == 6
assert result["remaining_energy"] == 2


# Test 2: Battery limit
try:
    round2(2, 2, 2, 2, 2, 7)
    assert False
except ValueError:
    pass


# Test 3: Day survival
assert calculate_day_result(1, 1)["survived"] is True
assert calculate_day_result(0, 1)["survived"] is False
assert calculate_day_result(1, 0)["survived"] is False


# Test 4: Round score
assert calculate_round2_score(True, True) == 3
assert calculate_round2_score(True, False) == 1
assert calculate_round2_score(False, False) == 0


# Test 5: Day 1 result and battery
session = create_session()

save_day_result(session, 1, 1, 1, 6)

assert session["r2"]["battery"] == 2
assert session["r2"]["history"][0]["survived"] is True


# Test 6: Both days survived
session = create_session()

save_day_result(session, 1, 1, 1, 4)
save_day_result(session, 2, 1, 1, 2)

end_round2(session)

assert session["r2"]["score"] == 3
assert session["classScore"] == 3


# Test 7: Team sets a Round 2 level

session = create_session()
session["crews"] = [
    {
        "id": "orion",
        "devices": ["device1"],
        "status": "Exploring"
    }
]

handle_team_event(
    session,
    "device1",
    {
        "event": "team:setLevel",
        "system": "lifeSupport",
        "levelId": "basic"
    }
)

assert session["r2"]["levels"]["lifeSupport"] == {
    "levelId": "basic",
    "cost": 1
}

print("Team setLevel test passed!")


print("All Round 2 tests passed!")
