import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.schemas import NoteCreate
from app.store import store


@pytest.fixture(autouse=True)
def _reset_store():
    store._notes.clear()
    store._next_id = 1
    yield
    store._notes.clear()
    store._next_id = 1


def _create_note(titel: str = "Einkaufsliste", tags: list[str] | None = None):
    return store.add(NoteCreate(titel=titel, inhalt="Milch", tags=tags or []))


def test_get_note_existing_returns_200():
    note = _create_note()
    with TestClient(app) as client:
        response = client.get(f"/notes/{note.id}")
    assert response.status_code == 200
    body = response.json()
    assert body["id"] == note.id
    assert body["titel"] == "Einkaufsliste"
    assert body["inhalt"] == "Milch"
    assert body["tags"] == []


def test_get_note_unknown_returns_404():
    with TestClient(app) as client:
        response = client.get("/notes/999")
    assert response.status_code == 404
    assert response.json() == {"detail": "Notiz nicht gefunden"}


def test_delete_note_removes_note():
    note = _create_note()
    with TestClient(app) as client:
        response = client.delete(f"/notes/{note.id}")
        assert response.status_code == 204
        follow_up = client.get(f"/notes/{note.id}")
    assert follow_up.status_code == 404


def test_delete_note_unknown_returns_404():
    with TestClient(app) as client:
        response = client.delete("/notes/999")
    assert response.status_code == 404
    assert response.json() == {"detail": "Notiz nicht gefunden"}
