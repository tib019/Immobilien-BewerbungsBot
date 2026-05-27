# ADR-002: SQLite für Bewerbungs-Tracking

**Status:** Accepted  
**Datum:** 2025

## Kontext
Der Bot muss verfolgen, welche Angebote bereits beworben wurden (keine Dopplungen).

## Entscheidung
SQLite-Datenbank (`test_bot.db`) für lokales Tracking von gesehenen und beworbenen Inseraten.

## Abgewogene Alternativen
- **JSON-Datei:** Einfacher, aber keine strukturierten Abfragen
- **PostgreSQL:** Überdimensioniert für lokale Einzelnutzung

## Konsequenzen
**Positiv:**
- Einfache Einrichtung, keine externe Datenbank
- SQL-Abfragen für Duplikat-Prüfung

**Negativ:**
- `test_bot.db` sollte nicht im Repository liegen (`.gitignore`)
