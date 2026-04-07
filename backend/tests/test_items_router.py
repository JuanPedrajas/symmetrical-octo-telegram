import pytest


@pytest.mark.asyncio
async def test_list_items_empty(async_client):
    response = await async_client.get("/api/v1/items/")
    assert response.status_code == 200
    assert response.json() == []


@pytest.mark.asyncio
async def test_create_item(async_client):
    response = await async_client.post(
        "/api/v1/items/",
        json={"name": "Test Item", "description": "A test item"},
    )
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "Test Item"
    assert data["description"] == "A test item"
    assert "id" in data


@pytest.mark.asyncio
async def test_get_item(async_client):
    create_resp = await async_client.post(
        "/api/v1/items/",
        json={"name": "Get Me", "description": "Find this item"},
    )
    item_id = create_resp.json()["id"]

    response = await async_client.get(f"/api/v1/items/{item_id}")
    assert response.status_code == 200
    assert response.json()["name"] == "Get Me"


@pytest.mark.asyncio
async def test_delete_item(async_client):
    create_resp = await async_client.post(
        "/api/v1/items/",
        json={"name": "Delete Me", "description": ""},
    )
    item_id = create_resp.json()["id"]

    delete_resp = await async_client.delete(f"/api/v1/items/{item_id}")
    assert delete_resp.status_code == 204

    get_resp = await async_client.get(f"/api/v1/items/{item_id}")
    assert get_resp.status_code == 404


@pytest.mark.asyncio
async def test_get_item_not_found(async_client):
    response = await async_client.get("/api/v1/items/999")
    assert response.status_code == 404
