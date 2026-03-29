# Immobilien-BewerbungsBot

[![Python](https://img.shields.io/badge/Python-3.8+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![Selenium](https://img.shields.io/badge/Selenium-43B02A?style=for-the-badge&logo=selenium&logoColor=white)](https://selenium.dev)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge)](LICENSE)

Vollautomatisierter Python-Bot zur Überwachung von Immobilienangeboten auf Immonet (optional auch ImmobilienScout24) und zum automatischen Versenden von Bewerbungen mit personalisierten Daten.

---

## Features

- Automatische Überwachung neuer Immobilienangebote
- Filterung nach Preis, Zimmeranzahl und Städten
- Automatisches Ausfüllen und Versenden von Bewerbungsformularen
- E-Mail-Benachrichtigungen über neue Bewerbungen und Fehler
- Datenbank-Tracking zur Vermeidung von Doppelbewerbungen
- Anti-Detection-Techniken (User-Agent-Rotation, zufällige Delays)
- Konfigurierbare Suchkriterien und Bewerbungsdaten
- Automatischer Scheduler für regelmäßige Durchläufe
- Umfassende Fehlerbehandlung und Logging

---

## Tech Stack

| Komponente | Technologie |
|------------|-------------|
| Sprache | Python 3.8+ |
| Browser-Automatisierung | Selenium WebDriver |
| Browser | Google Chrome + ChromeDriver |
| Datenbank | SQLite |
| Konfiguration | YAML |
| E-Mail | SMTP (konfigurierbar) |

---

## Installation

### Voraussetzungen

- Python 3.8 oder höher
- Google Chrome
- ChromeDriver (optional, wird ggf. automatisch installiert)

### Automatisch

```bash
python setup.py
```

Das Setup-Skript installiert alle Abhängigkeiten, prüft die Umgebung und führt durch die Konfiguration.

### Manuell

```bash
pip install -r requirements.txt
```

---

## Konfiguration

Alle Einstellungen werden in `config.yaml` vorgenommen:

- **Persönliche Daten**: Name, E-Mail, Adresse, Telefon
- **Suchkriterien**: maximaler Preis, Zimmeranzahl, Zielstädte
- **Bewerbungstext**: frei anpassbarer Motivationstext
- **E-Mail-Konfiguration**: SMTP-Server und Zugangsdaten für Benachrichtigungen
- **Bot-Einstellungen**: Suchintervalle, Bewerbungslimits, Anti-Detection-Parameter

---

## Verwendung

### Bot starten

```bash
python immobilien_bot_main.py
```

Der Bot läuft im Hintergrund, sucht regelmäßig nach neuen Angeboten und sendet automatisch Bewerbungen. Statusmeldungen und Logs werden ausgegeben sowie per E-Mail zugestellt (sofern konfiguriert).

---

## Tests

```bash
# Alle Tests ausführen
python -m pytest

# Einzelne Testdatei
python test_bot.py
```

Tests befinden sich im `tests/`-Ordner:
- `test_immobilien_bot.py` - Tests für Kernfunktionen
- `test_email_manager.py` - Tests für E-Mail-Versand

---

## Projektstruktur

```
Immobilien-BewerbungsBot/
  immobilien_bot.py        # Kernklassen, Scraper, Datenbanklogik
  immobilien_bot_main.py   # Hauptlogik und Scheduler
  email_manager.py         # E-Mail-Handling
  config.yaml              # Zentrale Konfiguration
  setup.py                 # Installations- und Konfigurationsskript
  requirements.txt         # Python-Abhängigkeiten
  tests/                   # Pytest-Testdateien
```

---

## Rechtliche Hinweise

Die Nutzung dieses Tools kann gegen die Allgemeinen Geschäftsbedingungen der Zielplattformen verstoßen. Rate-Limiting und respektvolles Crawling-Verhalten werden empfohlen. Die Nutzung erfolgt auf eigene Verantwortung.

---

## Lizenz

MIT License - siehe [LICENSE](LICENSE) für Details.

---

## Autor

**Tobias Buss**
- GitHub: [@tib019](https://github.com/tib019)
