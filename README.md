# notizen-api

Eine kleine REST-API zur Verwaltung von Notizen. Jede Notiz besteht aus `id`, `titel`, `inhalt`, `tags` und `erstellt_am`. Die Daten werden in einem In-Memory-Speicher gehalten (keine Datenbank) und gehen beim Neustart des Prozesses verloren.

## Tech-Stack

- **Sprache**: Python
- **Framework**: FastAPI
- **Validierung**: Pydantic v2
- **Konfiguration**: pydantic-settings
- **Speicher**: In-Memory (keine Datenbank)
- **Tests**: pytest + FastAPI `TestClient`

## Installation

```bash
python -m pip install -r requirements.txt
```

## Starten (Entwicklung)

```bash
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000
```

Danach ist die API unter `http://localhost:8000` erreichbar, die interaktive
Dokumentation (Swagger UI) unter `http://localhost:8000/docs`.

## Endpunkte

| Methode | Pfad                | Beschreibung                                          | Status                              |
| ------- | ------------------- | ----------------------------------------------------- | ----------------------------------- |
| GET     | `/health`           | Health-Check, liefert `{"status":"ok","app":...}`     | 200                                 |
| POST    | `/notes`            | Legt eine Notiz an (Body: `NoteCreate`)               | 201 → `Note`                        |
| GET     | `/notes`            | Listet alle Notizen, optional gefiltert per `?tag=x`  | 200 → `list[Note]`                  |
| GET     | `/notes/{id}`       | Liefert eine einzelne Notiz                           | 200 → `Note` / 404                  |
| DELETE  | `/notes/{id}`       | Löscht eine Notiz                                     | 204 / 404                           |

### Beispiel (POST /notes)

```bash
curl -X POST http://localhost:8000/notes \
  -H "Content-Type: application/json" \
  -d '{"titel":"Einkaufsliste","inhalt":"Milch","tags":["haus"]}'
```

## Modelle

- **NoteCreate**: `titel` (1–100 Zeichen, Pflicht), `inhalt` (Standard `""`), `tags` (max. 5).
- **Note**: `id`, `titel`, `inhalt`, `tags`, `erstellt_am` (UTC).

## Konfiguration

| Env-Variable | Beschreibung                | Standard      |
| ------------ | --------------------------- | ------------- |
| `APP_NAME`   | Name der App (im Health-Check zurückgegeben) | `notizen-api` |

## Tests

```bash
python -m pytest
```
