# ADR-001: Python + Playwright für Immobilien-Scraping

**Status:** Accepted  
**Datum:** 2025

## Kontext
Immobilienportale (ImmoScout24, Immowelt etc.) sind JavaScript-basierte SPAs. Scraping erfordert einen echten Browser.

## Entscheidung
Python mit Playwright für Browser-Automatisierung und Formular-Einreichung auf Immobilienportalen.

## Abgewogene Alternativen
- **Selenium:** Älter, langsamere API
- **requests/BeautifulSoup:** Kein JavaScript-Rendering
- **Puppeteer (Node.js):** Python für dieses Projekt bevorzugt

## Konsequenzen
**Positiv:**
- Voller Browser-Rendering-Support
- Formulare automatisch ausfüllbar
- Asynchrone Operationen möglich

**Negativ:**
- Anti-Bot-Schutz auf Portalen kann Automation blockieren
- Hoher Ressourcenverbrauch durch Browser
