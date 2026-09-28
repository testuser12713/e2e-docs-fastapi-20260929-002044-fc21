from fastapi import APIRouter, HTTPException, status

from app.schemas import Note, NoteCreate

router = APIRouter()


@router.post("/notes", response_model=Note, status_code=status.HTTP_201_CREATED)
def create_note(note: NoteCreate) -> Note:
    raise HTTPException(status_code=501, detail="POST /notes wird von Ticket #3 implementiert")


@router.get("/notes", response_model=list[Note])
def list_notes(tag: str | None = None) -> list[Note]:
    raise HTTPException(status_code=501, detail="GET /notes wird von Ticket #3 implementiert")
