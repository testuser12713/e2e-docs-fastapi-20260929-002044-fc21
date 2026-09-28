from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field, field_validator


class NoteCreate(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    titel: str = Field(min_length=1, max_length=100)
    inhalt: str = ""
    tags: list[str] = Field(default_factory=list)

    @field_validator("tags")
    @classmethod
    def tags_within_limit(cls, value: list[str]) -> list[str]:
        if len(value) > 5:
            raise ValueError("höchstens 5 Tags erlaubt")
        return value


class Note(BaseModel):
    id: int
    titel: str
    inhalt: str
    tags: list[str]
    erstellt_am: datetime
