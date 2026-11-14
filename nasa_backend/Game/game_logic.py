
# This file manages the game flow.
# It controls the transitions between rounds and steps
# when the host moves forward or backward.
from .round_steps import get_round_steps

def host_advance(session):

    current_round = session["round"]
    step = session["step"]

    # ROUND 1
    if current_round == 1:

        if step == "lobby":
            if len(session["crews"]) < 2:
                raise ValueError("At least 2 crews are required!")

            session["step"] = "briefing"
            return session

        if step == "roundComplete":
            session["round"] = 2
            session["step"] = "alert"
            return session

        if step == "decide":
            if session["r1"]["final"] is None:
                raise ValueError("The host must set the final answer first!")

            session["step"] = "reveal"
            return session

        steps = get_round_steps(1)

        if step in steps:
            current_index = steps.index(step)

            if current_index < len(steps) - 1:
                session["step"] = steps[current_index + 1]

            elif step == "debrief":
                session["step"] = "roundComplete"

        return session

    # ROUND 2
    if current_round == 2:

        day = session["r2"]["day"]

        if step == "roundComplete":
            session["round"] = 3
            session["step"] = "alert"
            return session

        if step == "dayResult":
            history = session["r2"]["history"]

            if not history or history[-1]["day"] != day:
                raise ValueError("Day result has not been calculated!")

            if not history[-1]["survived"]:
                session["step"] = "result"
                return session

            storm_days = session["r2"].get("stormDays", 2)

            if day < storm_days:
                session["r2"]["day"] += 1
                session["step"] = "day2Alert"
                return session

            session["step"] = "result"
            return session

        if step == "alert":
            session["step"] = "investigate"

        elif step == "investigate":
            session["step"] = "plan"

        elif step == "day2Alert":
            session["step"] = "plan"

        elif step == "result":
            session["step"] = "debrief"

        elif step == "debrief":
            session["step"] = "roundComplete"

        return session

    # ROUND 3
    if current_round == 3:

        if step == "roundComplete":
            session["round"] = 4
            session["step"] = "pack"
            return session

        if step == "rescue":
            if "rescueScore" not in session["r3"]:
                raise ValueError("Rescue result is missing!")

        elif step == "shelterBuild":
            crew_ids = [crew["id"] for crew in session["crews"]]

            for crew_id in crew_ids:
                if crew_id not in session["r3"]["shelterScores"]:
                    raise ValueError("All crews must submit their shelters!")

        steps = get_round_steps(3)

        if step in steps:
            current_index = steps.index(step)

            if current_index < len(steps) - 1:
                session["step"] = steps[current_index + 1]

            elif step == "debrief":
                session["step"] = "roundComplete"

        return session

    # ROUND 4
    if current_round == 4:

        if step == "roundComplete":
            session["round"] = 5
            session["step"] = "clues"
            return session

        steps = get_round_steps(4)

        if step in steps:
            current_index = steps.index(step)

            if current_index < len(steps) - 1:
                session["step"] = steps[current_index + 1]

            elif step == "debrief":
                session["step"] = "roundComplete"

        return session

    # ROUND 5
    if current_round == 5:

        if step == "roundComplete":
            session["step"] = "end"
            return session

        steps = get_round_steps(5)

        if step in steps:
            current_index = steps.index(step)

            if current_index < len(steps) - 1:
                session["step"] = steps[current_index + 1]

            elif step == "debrief":
                session["step"] = "roundComplete"

        return session

    return session


def host_back(session):

    current_round = session["round"]
    step = session["step"]

    # ROUND 1
    if current_round == 1:

        if step == "lobby":
            return session

        if step == "roundComplete":
            session["step"] = "debrief"
            return session

        if step == "reveal":
            session["step"] = "decide"
            return session

        if step == "decide":
            if session["r1"]["final"] is not None:
                raise ValueError("The final decision is already locked!")

            session["step"] = "share"
            return session

        steps = get_round_steps(1)
        current_index = steps.index(step)

        if current_index > 0:
            session["step"] = steps[current_index - 1]

        return session

    # ROUND 2
    if current_round == 2:

        if step == "roundComplete":
            session["step"] = "debrief"
            return session

        if step == "debrief":
            session["step"] = "result"
            return session

        if step == "result":
            session["step"] = "dayResult"
            return session

        if step == "dayResult":
            session["step"] = "plan"
            return session

        if step == "day2Alert":
            session["r2"]["day"] -= 1
            session["step"] = "dayResult"
            return session

        if step == "plan":
            if session["r2"]["day"] > 1:
                session["step"] = "day2Alert"
            else:
                session["step"] = "investigate"

            return session

        if step == "investigate":
            session["step"] = "alert"
            return session

        return session

    # ROUND 3
    if current_round == 3:

        if step == "roundComplete":
            session["step"] = "debrief"
            return session

        steps = get_round_steps(3)

        if step in steps:
            current_index = steps.index(step)

            if current_index > 0:
                session["step"] = steps[current_index - 1]

        return session

    # ROUND 4
    if current_round == 4:

        if step == "roundComplete":
            session["step"] = "debrief"
            return session

        steps = get_round_steps(4)

        if step in steps:
            current_index = steps.index(step)

            if current_index > 0:
                session["step"] = steps[current_index - 1]

        return session

    # ROUND 5
    if current_round == 5:

        if step == "roundComplete":
            session["step"] = "debrief"
            return session

        steps = get_round_steps(5)

        if step in steps:
            current_index = steps.index(step)

            if current_index > 0:
                session["step"] = steps[current_index - 1]

        return session

    return session
