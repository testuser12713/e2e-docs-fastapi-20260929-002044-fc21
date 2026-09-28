from datetime import UTC, datetime

from app.schemas import Note, NoteCreate


class NoteStore:
    def __init__(self) -> None:
        self._notes: dict[int, Note] = {}
        self._next_id: int = 1

    def add(self, note: NoteCreate) -> Note:
        created = Note(
            id=self._next_id,
            titel=note.titel,
            inhalt=note.inhalt,
            tags=note.tags,
            erstellt_am=datetime.now(UTC),
        )
        self._notes[self._next_id] = created
        self._next_id += 1
        return created

    def list_all(self, tag: str | None = None) -> list[Note]:
        notes = list(self._notes.values())
        if tag is not None:
            notes = [note for note in notes if tag in note.tags]
        return notes

    def get(self, note_id: int) -> Note | None:
        return self._notes.get(note_id)

    def delete(self, note_id: int) -> bool:
        return self._notes.pop(note_id, None) is not None


store = NoteStore()
