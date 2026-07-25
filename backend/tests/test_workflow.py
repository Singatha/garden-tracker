from httpx import AsyncClient


async def test_complete_garden_workflow(client: AsyncClient, auth_headers: dict[str, str]):
    garden_response = await client.post(
        "/api/v1/gardens",
        json={"name": "Home Garden", "location": "Backyard"},
        headers=auth_headers,
    )
    assert garden_response.status_code == 201
    garden_id = garden_response.json()["id"]

    area_response = await client.post(
        f"/api/v1/gardens/{garden_id}/areas",
        json={"name": "Sunny Bed", "area_type": "bed"},
        headers=auth_headers,
    )
    assert area_response.status_code == 201

    planting_response = await client.post(
        f"/api/v1/gardens/{garden_id}/plantings",
        json={
            "growing_area_id": area_response.json()["id"],
            "crop": "Tomato",
            "variety": "Roma",
            "quantity": 4,
            "method": "transplanted",
            "planted_on": "2026-07-20",
        },
        headers=auth_headers,
    )
    assert planting_response.status_code == 201
    assert planting_response.json()["crop"] == "Tomato"
    planting_id = planting_response.json()["id"]

    activity_response = await client.post(
        f"/api/v1/gardens/{garden_id}/activities",
        json={
            "planting_id": planting_id,
            "event_type": "watered",
            "occurred_on": "2026-07-25",
            "notes": "Deep watering after a warm day",
        },
        headers=auth_headers,
    )
    assert activity_response.status_code == 201

    status_response = await client.patch(
        f"/api/v1/gardens/{garden_id}/plantings/{planting_id}",
        json={"status": "finished"},
        headers=auth_headers,
    )
    assert status_response.status_code == 200
    assert status_response.json()["status"] == "finished"

    activities = await client.get(f"/api/v1/gardens/{garden_id}/activities", headers=auth_headers)
    assert activities.json()[0]["notes"] == "Deep watering after a warm day"


async def test_garden_isolation(client: AsyncClient, auth_headers: dict[str, str]):
    garden = (
        await client.post("/api/v1/gardens", json={"name": "Private"}, headers=auth_headers)
    ).json()
    other = await client.post(
        "/api/v1/auth/register",
        json={"email": "other@example.com", "name": "Other", "password": "secret123"},
    )
    other_headers = {"Authorization": f"Bearer {other.json()['access_token']}"}
    response = await client.get(f"/api/v1/gardens/{garden['id']}/areas", headers=other_headers)
    assert response.status_code == 404
