from datetime import datetime

import pytest
from fastapi.testclient import TestClient
from pydantic import ValidationError

from app.main import app
from app.schemas import NoteCreate
from app.store import NoteStore


def test_health_returns_200_with_app_name():
    with TestClient(app) as client:
        response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok", "app": "notizen-api"}


def test_note_create_accepts_valid_input():
    note = NoteCreate(titel="Einkaufsliste", inhalt="Milch", tags=["haus", "wichtig"])
    assert note.titel == "Einkaufsliste"
    assert note.inhalt == "Milch"
    assert note.tags == ["haus", "wichtig"]


def test_note_create_defaults():
    note = NoteCreate(titel="Titel")
    assert note.inhalt == ""
    assert note.tags == []


def test_note_create_rejects_empty_title():
    with pytest.raises(ValidationError):
        NoteCreate(titel="")


def test_note_create_rejects_title_over_100_chars():
    with pytest.raises(ValidationError):
        NoteCreate(titel="x" * 101)


def test_note_create_rejects_more_than_5_tags():
    with pytest.raises(ValidationError):
        NoteCreate(titel="Titel", tags=["a", "b", "c", "d", "e", "f"])


def test_store_crud():
    store = NoteStore()

    first = store.add(NoteCreate(titel="Eins", tags=["wichtig"]))
    second = store.add(NoteCreate(titel="Zwei", tags=["egal"]))

    assert first.id == 1
    assert second.id == 2
    assert isinstance(first.erstellt_am, datetime)

    assert len(store.list_all()) == 2
    assert [note.id for note in store.list_all(tag="wichtig")] == [1]
    assert store.list_all(tag="fehlt") == []

    assert store.get(1) is first
    assert store.get(99) is None

    assert store.delete(1) is True
    assert store.get(1) is None
    assert store.delete(99) is False


def test_stub_routes_respond_501():
    with TestClient(app) as client:
        assert client.post("/notes", json={"titel": "x"}).status_code == 501
        assert client.get("/notes").status_code == 501
        assert client.get("/notes/1").status_code == 501
        assert client.delete("/notes/1").status_code == 501
