# This file handles team joining and lobby updates.

from .connections import device_connections, host_connections


async def send_to_all(code, message):
    host = host_connections.get(code)

    if host:
        await host.send_json(message)

    for websocket in device_connections.get(code, {}).values():
        await websocket.send_json(message)


async def update_lobby(code, sessions):
    session = sessions[code]
    connected = device_connections.get(code, {})

    crews = []

    for crew in session["crews"]:
        crews.append({
            "id": crew["id"],
            "deviceCount": sum(
                1 for device_id in crew["devices"]
                if device_id in connected
            )
        })

    await send_to_all(code, {
        "event": "lobby:update",
        "crews": crews
    })
