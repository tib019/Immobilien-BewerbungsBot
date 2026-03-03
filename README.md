# 🏠 Immobilien-Bewerbungsbot

[![Python](https://img.shields.io/badge/Python-3.8+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![Selenium](https://img.shields.io/badge/Selenium-43B02A?style=for-the-badge&logo=selenium&logoColor=white)](https://selenium.dev)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=for-the-badge)](LICENSE)


Ein vollautomatisierter Python-Bot, der neue Immobilienangebote auf Immonet (und optional ImmobilienScout24) überwacht und automatisch Bewerbungen mit personalisierten Daten versendet. Das Tool richtet sich an alle, die ihre Wohnungssuche effizienter und zeitsparender gestalten möchten.

---

## 🚀 Features

- **Automatische Überwachung** von Immobilienangeboten
- **Intelligente Filterung** nach Preis, Zimmer, Städten etc.
- **Automatisches Ausfüllen und Versenden** von Bewerbungsformularen
- **E-Mail-Benachrichtigungen** über neue Bewerbungen und Fehler
- **Datenbank-Tracking** zur Vermeidung von Doppelbewerbungen
- **Anti-Detection-Techniken** (User-Agent-Rotation, Delays)
- **Konfigurierbare Suchkriterien** und Bewerbungsdaten
- **Automatischer Scheduler** für regelmäßige Durchläufe
- **Umfassende Fehlerbehandlung** und Logging

---

## 🛠️ Installation

### Voraussetzungen
- Python 3.8 oder höher
- Google Chrome (für Selenium WebDriver)
- Optional: ChromeDriver im PATH

### Automatische Installation

```bash
python setup.py
```

Das Setup-Skript installiert alle Abhängigkeiten, prüft die Umgebung und hilft bei der Konfiguration.

### Manuelle Installation

```bash
pip install -r requirements.txt
```

---

## ⚙️ Konfiguration

Alle Einstellungen erfolgen in der Datei `config.yaml`:

- **Persönliche Daten** (Name, E-Mail, Adresse, etc.)
- **Suchkriterien** (max. Preis, Zimmer, Städte)
- **Bewerbungstext** (frei anpassbar)
- **E-Mail-Konfiguration** (SMTP für Benachrichtigungen)
- **Bot-Einstellungen** (Intervalle, Limits, Anti-Detection)

Beispiel siehe `config.yaml`.

---

## 🏃‍♂️ Nutzung

### Starten des Bots

```bash
python immobilien_bot_main.py
```

Der Bot läuft im Hintergrund, sucht regelmäßig nach neuen Angeboten und bewirbt sich automatisch. Logs und Statusmeldungen werden ausgegeben und per E-Mail versendet (sofern konfiguriert).

### Testen

```bash
python test_bot.py
```

---

## 🏗️ Architektur

- **immobilien_bot.py**: Kernklassen, Scraper, Datenbank
- **immobilien_bot_main.py**: Hauptlogik, Scheduler
- **email_manager.py**: E-Mail-Handling
- **config.yaml**: Zentrale Konfiguration
- **setup.py**: Installations- und Konfigurationsskript
- **test_bot.py**: Tests

---

## 📝 Rechtliche Hinweise

- Die Nutzung kann gegen die AGB der Zielseiten verstoßen.
- Rate-Limiting und respektvolle Nutzung werden empfohlen.
- Nutzung auf eigene Verantwortung!

---

## 📄 Lizenz

MIT License – siehe LICENSE-Datei.

---

## 🤝 Beitragen

Pull Requests und Feature-Ideen sind willkommen!

---

## 📚 Weitere Informationen

- Ausführliche Dokumentation: `🏠 Immobilien-Bewerbungsbot.md`
- Projektzusammenfassung: `🏠 Immobilien-Bewerbungsbot - Projektzusammenfassung.md`
- Website-Analyse: `Website-Analyse für Immobilien-Bewerbungsbot.md`

---

**Entwickelt von tibo** 