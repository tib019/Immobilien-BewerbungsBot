# Projektscope — Immobilien-Bewerbungsbot

## Problem
Die Wohnungssuche in deutschen Großstädten ist extrem wettbewerbsintensiv. Wer nicht sofort auf neue Inserate reagiert, bekommt keine Wohnung. Manuelle Überwachung von Portalen ist mühsam.

## Lösung
Ein automatisierter Bot, der Immobilienportale überwacht, neue passende Inserate erkennt und automatisch Bewerbungen einreicht.

## In Scope
- Automatisches Durchsuchen von Immobilienportalen (ImmoScout24, Immowelt etc.)
- Filter nach Kriterien (Preis, Größe, Standort)
- Automatisches Ausfüllen und Einreichen von Bewerbungsformularen
- Duplikat-Tracking (SQLite)
- E-Mail-Benachrichtigungen bei neuen Bewerbungen
- YAML-Konfigurationsdatei für Suchparameter
- pytest-Tests

## Out of Scope
- Vollständiger Mietvertrag-Abschluss
- KI-generierte persönliche Anschreiben
- Mobile App
- Multi-User-SaaS

## Technologie-Stack
| Schicht | Technologie |
|---------|-------------|
| Sprache | Python |
| Browser-Automation | Playwright |
| Konfiguration | YAML |
| Datenbank | SQLite |
| E-Mail | SMTP |
| Tests | pytest |
