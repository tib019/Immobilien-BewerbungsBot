#!/usr/bin/env python3
"""
Test-Skript für den Immobilien-Bewerbungsbot
Testet die Grundfunktionalitäten ohne echte Bewerbungen

Autor: tibo
Datum: 2025-07-03
"""

import sys
import logging
from datetime import datetime
from immobilien_bot import BewerbungsConfig, DatabaseManager, ImmonetScraper, ImmobilienAngebot

# Logging konfigurieren
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def test_database():
    """Testet die Datenbank-Funktionalität"""
 print("️ Teste Datenbank...")
    
    try:
        db = DatabaseManager("test_bot.db")
        
        # Test-Angebot erstellen
        test_angebot = ImmobilienAngebot(
            id="test123",
            titel="Test-Wohnung",
            preis=1000.0,
            groesse=50.0,
            zimmer=2,
            ort="Berlin",
            url="https://example.com/test",
            anbieter="Test-Anbieter",
            erstellt=datetime.now(),
            website="immonet"
        )
        
        # Bewerbung speichern
        db.bewerbung_speichern(test_angebot, True)
        
        # Prüfen ob bereits beworben
        bereits_beworben = db.ist_bereits_beworben("test123")
        
        if bereits_beworben:
 print("Datenbank-Test erfolgreich!")
            return True
        else:
 print("Datenbank-Test fehlgeschlagen!")
            return False
            
    except Exception as e:
 print(f" Datenbank-Fehler: {e}")
        return False

def test_config():
    """Testet die Konfiguration"""
 print("️ Teste Konfiguration...")
    
    try:
        config = BewerbungsConfig(
            anrede="Herr",
            vorname="Test",
            nachname="User",
            email="test@example.com",
            telefon="123456789",
            strasse="Teststraße 1",
            plz="12345",
            ort="Berlin",
            bewerbungstext="Test-Bewerbung",
            max_preis=1500.0,
            min_zimmer=2,
            max_zimmer=4,
            suchstaedte=["Berlin"]
        )
        
 print("Konfiguration erfolgreich erstellt!")
        print(f"   - Name: {config.vorname} {config.nachname}")
        print(f"   - E-Mail: {config.email}")
        print(f"   - Suchstädte: {config.suchstaedte}")
        print(f"   - Preisbereich: bis {config.max_preis}€")
        return True
        
    except Exception as e:
 print(f" Konfiguration-Fehler: {e}")
        return False

def test_scraper_basic():
    """Testet die Grundfunktionen des Scrapers (ohne echte Anfragen)"""
 print("️ Teste Scraper-Grundfunktionen...")
    
    try:
        config = BewerbungsConfig(
            vorname="Test",
            nachname="User",
            email="test@example.com",
            suchstaedte=["Berlin"]
        )
        
        # Scraper erstellen (ohne WebDriver für Test)
        scraper = ImmonetScraper(config)
        
        # Session testen
        if scraper.session:
 print("HTTP-Session erstellt")
        
        # User-Agent testen
        user_agent = scraper.get_random_user_agent()
        if user_agent:
 print(f" User-Agent: {user_agent[:50]}...")
        
        # Cleanup
        scraper.cleanup()
        
 print("Scraper-Grundfunktionen erfolgreich!")
        return True
        
    except Exception as e:
 print(f" Scraper-Fehler: {e}")
        return False

def test_angebot_parsing():
    """Testet das Parsen von Angebots-Daten"""
 print("Teste Angebots-Parsing...")
    
    try:
        config = BewerbungsConfig()
        scraper = ImmonetScraper(config)
        
        # Test-Preis parsen
        test_preise = [
            "1.472 € Kaltmiete",
            "1,200.50 EUR",
            "850€",
            "2.000 Euro"
        ]
        
        for preis_text in test_preise:
            preis = scraper._parse_preis(preis_text)
            print(f"   '{preis_text}' -> {preis}€")
        
        # Test-Zimmer extrahieren
        test_texte = [
            "3 Zimmer Wohnung",
            "Schöne 2-Zimmer-Wohnung",
            "4 Zimmer, 80m²"
        ]
        
        for text in test_texte:
            zimmer = scraper._extract_zimmer(text)
            print(f"   '{text}' -> {zimmer} Zimmer")
        
        scraper.cleanup()
 print("Angebots-Parsing erfolgreich!")
        return True
        
    except Exception as e:
 print(f" Parsing-Fehler: {e}")
        return False

def test_email_manager():
    """Testet den E-Mail-Manager (ohne echte E-Mails zu senden)"""
 print("Teste E-Mail-Manager...")
    
    try:
        from email_manager import EmailManager
        
        config = BewerbungsConfig(
            vorname="Test",
            email="test@example.com"
        )
        
        email_manager = EmailManager(config)
        
        # Template-Loading testen
        if email_manager.templates:
 print("E-Mail-Templates geladen")
        
        # Test-Angebot für E-Mail
        test_angebot = ImmobilienAngebot(
            id="email_test",
            titel="E-Mail Test Wohnung",
            preis=1200.0,
            groesse=60.0,
            zimmer=3,
            ort="Berlin",
            url="https://example.com/email_test",
            anbieter="Test-Makler",
            erstellt=datetime.now(),
            website="immonet"
        )
        
 print("E-Mail-Manager erfolgreich initialisiert!")
        return True
        
    except Exception as e:
 print(f" E-Mail-Manager-Fehler: {e}")
        return False

def run_all_tests():
    """Führt alle Tests aus"""
 print("IMMOBILIEN-BOT TESTS")
    print("=" * 40)
    
    tests = [
        ("Datenbank", test_database),
        ("Konfiguration", test_config),
        ("Scraper-Grundfunktionen", test_scraper_basic),
        ("Angebots-Parsing", test_angebot_parsing),
        ("E-Mail-Manager", test_email_manager)
    ]
    
    results = []
    
    for test_name, test_func in tests:
        print(f"\n{test_name}:")
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
 print(f" Unerwarteter Fehler in {test_name}: {e}")
            results.append((test_name, False))
    
    # Ergebnisse zusammenfassen
    print("\n" + "=" * 40)
 print("TEST-ERGEBNISSE:")
    print("=" * 40)
    
    passed = 0
    failed = 0
    
    for test_name, result in results:
        status = "✅ BESTANDEN" if result else "❌ FEHLGESCHLAGEN"
        print(f"{test_name}: {status}")
        if result:
            passed += 1
        else:
            failed += 1
    
    print(f"\nGesamt: {passed} bestanden, {failed} fehlgeschlagen")
    
    if failed == 0:
 print("\n Alle Tests bestanden! Der Bot ist bereit für den Einsatz.")
 print("\n Nächste Schritte:")
        print("1. Bearbeiten Sie config.yaml mit Ihren echten Daten")
        print("2. Starten Sie den Bot mit: python3 immobilien_bot_main.py")
    else:
 print(f"\n️ {failed} Tests fehlgeschlagen. Bitte prüfen Sie die Konfiguration.")
    
    return failed == 0

if __name__ == "__main__":
    try:
        success = run_all_tests()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
 print("\n\n Tests abgebrochen.")
        sys.exit(1)
    except Exception as e:
 print(f"\n Unerwarteter Fehler: {e}")
        sys.exit(1)

