from fastapi import APIRouter, HTTPException, status

from app.schemas import Note
from app.store import store

router = APIRouter()


@router.get("/notes/{id}", response_model=Note)
def get_note(id: int) -> Note:
    note = store.get(id)
    if note is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Notiz nicht gefunden")
    return note


@router.delete("/notes/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_note(id: int) -> None:
    if not store.delete(id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Notiz nicht gefunden")
