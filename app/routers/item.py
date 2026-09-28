from fastapi import APIRouter, HTTPException, status

from app.schemas import Note

router = APIRouter()


@router.get("/notes/{id}", response_model=Note)
def get_note(id: int) -> Note:
    raise HTTPException(status_code=501, detail="GET /notes/{id} wird von Ticket #1 implementiert")


@router.delete("/notes/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_note(id: int) -> None:
    raise HTTPException(
        status_code=501, detail="DELETE /notes/{id} wird von Ticket #1 implementiert"
    )
