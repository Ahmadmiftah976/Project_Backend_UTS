def iso(h):
    return f"2026-11-01T{h:02d}:00:00"


def create_room(client, name="Ruang A", capacity=10):
    return client.post("/rooms", json={"name": name, "capacity": capacity})


def book(client, room_id, start, end, who="Budi"):
    return client.post(
        "/reservations",
        json={
            "room_id": room_id,
            "booked_by": who,
            "start_time": iso(start),
            "end_time": iso(end),
        },
    )


def test_root(client):
    assert client.get("/").status_code == 200


def test_create_and_get_room(client):
    res = create_room(client)
    assert res.status_code == 201
    assert client.get(f"/rooms/{res.json()['id']}").json()["name"] == "Ruang A"


def test_create_room_invalid_capacity(client):
    assert create_room(client, capacity=0).status_code == 422


def test_get_room_not_found(client):
    assert client.get("/rooms/999").status_code == 404


def test_create_reservation_201(client):
    room_id = create_room(client).json()["id"]
    res = book(client, room_id, 9, 11)
    assert res.status_code == 201
    assert res.json()["status"] == "active"


def test_overlap_returns_409(client):
    room_id = create_room(client).json()["id"]
    book(client, room_id, 9, 11)
    assert book(client, room_id, 10, 12, who="Ani").status_code == 409


def test_too_long_returns_422(client):
    room_id = create_room(client).json()["id"]
    assert book(client, room_id, 8, 13).status_code == 422


def test_unknown_room_returns_404(client):
    assert book(client, 123, 9, 10).status_code == 404


def test_cancel_reservation(client):
    room_id = create_room(client).json()["id"]
    rid = book(client, room_id, 9, 11).json()["id"]
    res = client.patch(f"/reservations/{rid}/cancel")
    assert res.status_code == 200
    assert res.json()["status"] == "cancelled"


def test_list_reservations_by_room(client):
    r1 = create_room(client).json()["id"]
    r2 = create_room(client, "Ruang B").json()["id"]
    book(client, r1, 9, 10)
    book(client, r2, 9, 10)
    assert len(client.get("/reservations").json()) == 2
    assert len(client.get(f"/reservations?room_id={r1}").json()) == 1
