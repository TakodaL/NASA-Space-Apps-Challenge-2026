
from fastapi.testclient import TestClient
from main import app
from session_store import create_session_host

client = TestClient(app)

# Creează o sesiune nouă
host_data = create_session_host()
code = host_data["code"]
host_token = host_data["hostToken"]


with client.websocket_connect("/ws") as host:

    # HOST JOIN
    host.send_json({
        "event": "host:join",
        "code": code,
        "hostToken": host_token
    })

    assert host.receive_json()["event"] == "session:state"

    with client.websocket_connect("/ws") as device1:

        # DEVICE 1 JOIN
        device1.send_json({
            "event": "device:join",
            "code": code,
            "deviceId": "device1"
        })

        assert device1.receive_json()["event"] == "session:state"

        # DEVICE 1 alege ORION
        device1.send_json({
            "event": "crew:pick",
            "crewId": "orion"
        })

        # Două lobby:update:
        # unul la conectare și unul la alegerea echipei
        for _ in range(2):
            assert device1.receive_json()["event"] == "lobby:update"
            assert host.receive_json()["event"] == "lobby:update"

        with client.websocket_connect("/ws") as device2:

            # DEVICE 2 JOIN
            device2.send_json({
                "event": "device:join",
                "code": code,
                "deviceId": "device2"
            })

            assert device2.receive_json()["event"] == "session:state"

            # DEVICE 2 alege LYRA
            device2.send_json({
                "event": "crew:pick",
                "crewId": "lyra"
            })

            # Două lobby:update pentru fiecare conexiune:
            # unul la conectare și unul la alegerea echipei
            for _ in range(2):
                assert host.receive_json()["event"] == "lobby:update"
                assert device1.receive_json()["event"] == "lobby:update"
                assert device2.receive_json()["event"] == "lobby:update"

            # HOST: BRIEFING
            host.send_json({"event": "host:advance"})

            assert host.receive_json()["step"] == "briefing"
            assert device1.receive_json()["step"] == "briefing"
            assert device2.receive_json()["step"] == "briefing"

            # HOST: INVESTIGATE
            host.send_json({"event": "host:advance"})

            assert host.receive_json()["step"] == "investigate"
            assert device1.receive_json()["step"] == "investigate"
            assert device2.receive_json()["step"] == "investigate"

            # HOST: SUBMIT
            host.send_json({"event": "host:advance"})

            assert host.receive_json()["step"] == "submit"
            assert device1.receive_json()["step"] == "submit"
            assert device2.receive_json()["step"] == "submit"

            # ORION SUBMITS
            device1.send_json({
                "event": "team:submit",
                "choice": "A",
                "reasonId": "energy"
            })

            assert device1.receive_json()["event"] == "crew:status"
            assert host.receive_json()["event"] == "crew:status"
            assert device2.receive_json()["event"] == "crew:status"

            # HOST: SHARE
            host.send_json({"event": "host:advance"})

            assert host.receive_json()["step"] == "share"
            assert device1.receive_json()["step"] == "share"
            assert device2.receive_json()["step"] == "share"

            # HOST: DECIDE
            host.send_json({"event": "host:advance"})

            assert host.receive_json()["step"] == "decide"
            assert device1.receive_json()["step"] == "decide"
            assert device2.receive_json()["step"] == "decide"

            # ORION VOTES A
            device1.send_json({
                "event": "team:vote",
                "choice": "A"
            })

            # CREW STATUS
            assert device1.receive_json()["event"] == "crew:status"
            assert host.receive_json()["event"] == "crew:status"
            assert device2.receive_json()["event"] == "crew:status"

            # TALLY
            tally = device1.receive_json()

            print("Received tally:", tally)

            assert tally["event"] == "tally:update"
            assert tally["A"] == 1
            assert tally["B"] == 0
            assert tally["C"] == 0


print("WebSocket test passed!")
