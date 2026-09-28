from datetime import datetime

import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.store import store


@pytest.fixture(autouse=True)
def reset_store():
    store._notes.clear()
    store._next_id = 1
    yield


def test_create_note_returns_id_and_erstellt_am():
    with TestClient(app) as client:
        response = client.post(
            "/notes",
            json={"titel": "Einkaufsliste", "inhalt": "Milch", "tags": ["haus", "wichtig"]},
        )
    assert response.status_code == 201
    body = response.json()
    assert body["id"] == 1
    assert body["titel"] == "Einkaufsliste"
    assert body["inhalt"] == "Milch"
    assert body["tags"] == ["haus", "wichtig"]
    assert "erstellt_am" in body
    datetime.fromisoformat(body["erstellt_am"].replace("Z", "+00:00"))


def test_create_note_rejects_empty_title():
    with TestClient(app) as client:
        response = client.post("/notes", json={"titel": ""})
    assert response.status_code == 422


def test_create_note_rejects_title_over_100_chars():
    with TestClient(app) as client:
        response = client.post("/notes", json={"titel": "x" * 101})
    assert response.status_code == 422


def test_create_note_rejects_more_than_5_tags():
    with TestClient(app) as client:
        response = client.post(
            "/notes", json={"titel": "Titel", "tags": ["a", "b", "c", "d", "e", "f"]}
        )
    assert response.status_code == 422


def test_list_all_notes():
    with TestClient(app) as client:
        client.post("/notes", json={"titel": "Eins", "tags": ["wichtig"]})
        client.post("/notes", json={"titel": "Zwei", "tags": ["egal"]})
        response = client.get("/notes")
    assert response.status_code == 200
    body = response.json()
    assert len(body) == 2
    assert [note["id"] for note in body] == [1, 2]


def test_list_notes_filtered_by_tag():
    with TestClient(app) as client:
        client.post("/notes", json={"titel": "Eins", "tags": ["wichtig"]})
        client.post("/notes", json={"titel": "Zwei", "tags": ["egal"]})
        response = client.get("/notes", params={"tag": "wichtig"})
    assert response.status_code == 200
    body = response.json()
    assert len(body) == 1
    assert body[0]["titel"] == "Eins"


def test_list_notes_filtered_by_missing_tag_returns_empty():
    with TestClient(app) as client:
        client.post("/notes", json={"titel": "Eins", "tags": ["wichtig"]})
        response = client.get("/notes", params={"tag": "fehlt"})
    assert response.status_code == 200
    assert response.json() == []
