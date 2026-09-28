from fastapi import APIRouter, status

from app.schemas import Note, NoteCreate
from app.store import store

router = APIRouter()


@router.post("/notes", response_model=Note, status_code=status.HTTP_201_CREATED)
def create_note(note: NoteCreate) -> Note:
    return store.add(note)


@router.get("/notes", response_model=list[Note])
def list_notes(tag: str | None = None) -> list[Note]:
    return store.list_all(tag)
