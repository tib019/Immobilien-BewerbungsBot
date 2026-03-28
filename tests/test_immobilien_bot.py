"""
Comprehensive tests for immobilien_bot.py
Tests cover: ImmobilienAngebot dataclass, BewerbungsConfig dataclass,
scraper logic, SQLite database operations, and edge cases.
"""
import sys
import os
import sqlite3
import pytest
from datetime import datetime
from unittest.mock import MagicMock, patch, PropertyMock

# Ensure the repo root is on the path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Selenium imports cause side-effects at import time; patch before importing module
with patch("selenium.webdriver.Chrome"):
    from immobilien_bot import (
        ImmobilienAngebot,
        BewerbungsConfig,
        DatabaseManager,
        ImmonetScraper,
        ImmobilienScout24Scraper,
    )


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def make_angebot(**kwargs):
    defaults = dict(
        id="test-id-001",
        titel="Schöne Wohnung",
        preis=1200.0,
        groesse=70.0,
        zimmer=3,
        ort="Berlin",
        url="https://www.immonet.de/expose/test-id-001",
        anbieter="Muster Makler",
        erstellt=datetime(2025, 1, 15, 10, 0, 0),
        website="immonet",
    )
    defaults.update(kwargs)
    return ImmobilienAngebot(**defaults)


def make_config(**kwargs):
    defaults = dict(
        vorname="Max",
        nachname="Mustermann",
        email="max@example.com",
        max_preis=2000.0,
        min_zimmer=1,
        max_zimmer=5,
    )
    defaults.update(kwargs)
    return BewerbungsConfig(**defaults)


# ---------------------------------------------------------------------------
# ImmobilienAngebot dataclass tests
# ---------------------------------------------------------------------------

class TestImmobilienAngebot:
    def test_creation_with_all_fields(self):
        ts = datetime(2025, 6, 1, 12, 0, 0)
        angebot = ImmobilienAngebot(
            id="abc-123",
            titel="Top Wohnung",
            preis=900.0,
            groesse=55.0,
            zimmer=2,
            ort="Hamburg",
            url="https://example.com/abc-123",
            anbieter="Immo GmbH",
            erstellt=ts,
            website="immonet",
        )
        assert angebot.id == "abc-123"
        assert angebot.titel == "Top Wohnung"
        assert angebot.preis == 900.0
        assert angebot.groesse == 55.0
        assert angebot.zimmer == 2
        assert angebot.ort == "Hamburg"
        assert angebot.url == "https://example.com/abc-123"
        assert angebot.anbieter == "Immo GmbH"
        assert angebot.erstellt == ts
        assert angebot.website == "immonet"

    def test_hash_is_based_on_id(self):
        a1 = make_angebot(id="unique-001")
        a2 = make_angebot(id="unique-001", titel="Anderer Titel", preis=999.0)
        assert hash(a1) == hash(a2)

    def test_hash_differs_for_different_ids(self):
        a1 = make_angebot(id="id-001")
        a2 = make_angebot(id="id-002")
        assert hash(a1) != hash(a2)

    def test_equality_same_id(self):
        a1 = make_angebot(id="same-id")
        a2 = make_angebot(id="same-id", preis=5000.0)
        assert a1 == a2

    def test_inequality_different_ids(self):
        a1 = make_angebot(id="id-A")
        a2 = make_angebot(id="id-B")
        assert a1 != a2

    def test_equality_with_non_angebot(self):
        angebot = make_angebot()
        assert angebot != "not an angebot"
        assert angebot != 42
        assert angebot != None

    def test_can_be_used_in_set(self):
        a1 = make_angebot(id="dup")
        a2 = make_angebot(id="dup")
        a3 = make_angebot(id="unique")
        s = {a1, a2, a3}
        assert len(s) == 2

    def test_can_be_used_as_dict_key(self):
        angebot = make_angebot(id="key-001")
        d = {angebot: "value"}
        lookup = make_angebot(id="key-001")
        assert d[lookup] == "value"

    def test_zero_preis(self):
        angebot = make_angebot(preis=0.0)
        assert angebot.preis == 0.0

    def test_large_wohnung(self):
        angebot = make_angebot(groesse=500.0, zimmer=10, preis=10000.0)
        assert angebot.groesse == 500.0
        assert angebot.zimmer == 10


# ---------------------------------------------------------------------------
# BewerbungsConfig dataclass tests
# ---------------------------------------------------------------------------

class TestBewerbungsConfig:
    def test_defaults(self):
        config = BewerbungsConfig()
        assert config.anrede == "Herr"
        assert config.vorname == ""
        assert config.nachname == ""
        assert config.email == ""
        assert config.telefon == ""
        assert config.smtp_server == "smtp.gmail.com"
        assert config.smtp_port == 587
        assert config.smtp_username == ""
        assert config.smtp_password == ""
        assert config.max_preis == 2000.0
        assert config.min_zimmer == 1
        assert config.max_zimmer == 5

    def test_post_init_sets_default_suchstaedte(self):
        config = BewerbungsConfig()
        assert config.suchstaedte is not None
        assert isinstance(config.suchstaedte, list)
        assert "Berlin" in config.suchstaedte
        assert "München" in config.suchstaedte
        assert "Hamburg" in config.suchstaedte

    def test_post_init_preserves_custom_suchstaedte(self):
        config = BewerbungsConfig(suchstaedte=["Köln", "Frankfurt"])
        assert config.suchstaedte == ["Köln", "Frankfurt"]

    def test_custom_values(self):
        config = BewerbungsConfig(
            anrede="Frau",
            vorname="Maria",
            nachname="Muster",
            email="maria@example.com",
            telefon="0987654321",
            max_preis=1500.0,
            min_zimmer=2,
            max_zimmer=4,
        )
        assert config.anrede == "Frau"
        assert config.vorname == "Maria"
        assert config.nachname == "Muster"
        assert config.email == "maria@example.com"
        assert config.telefon == "0987654321"
        assert config.max_preis == 1500.0
        assert config.min_zimmer == 2
        assert config.max_zimmer == 4

    def test_smtp_custom_config(self):
        config = BewerbungsConfig(
            smtp_server="smtp.outlook.com",
            smtp_port=465,
            smtp_username="user@outlook.com",
            smtp_password="secret",
        )
        assert config.smtp_server == "smtp.outlook.com"
        assert config.smtp_port == 465

    def test_suchstaedte_none_triggers_default(self):
        # Passing None explicitly should trigger __post_init__ default
        config = BewerbungsConfig(suchstaedte=None)
        assert config.suchstaedte == ["Berlin", "München", "Hamburg"]


# ---------------------------------------------------------------------------
# DatabaseManager (in-memory SQLite) tests
# ---------------------------------------------------------------------------

class TestDatabaseManager:
    @pytest.fixture
    def db(self, tmp_path):
        db_path = str(tmp_path / "test_immobilien.db")
        return DatabaseManager(db_path=db_path)

    def test_init_creates_tables(self, db):
        with sqlite3.connect(db.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT name FROM sqlite_master WHERE type='table' AND name='bewerbungen'"
            )
            assert cursor.fetchone() is not None
            cursor.execute(
                "SELECT name FROM sqlite_master WHERE type='table' AND name='logs'"
            )
            assert cursor.fetchone() is not None

    def test_ist_bereits_beworben_returns_false_for_unknown(self, db):
        assert db.ist_bereits_beworben("unknown-id") is False

    def test_bewerbung_speichern_and_check(self, db):
        angebot = make_angebot(id="save-001")
        db.bewerbung_speichern(angebot, erfolgreich=True)
        assert db.ist_bereits_beworben("save-001") is True

    def test_bewerbung_speichern_erfolgreich_false(self, db):
        angebot = make_angebot(id="fail-001")
        db.bewerbung_speichern(angebot, erfolgreich=False)
        assert db.ist_bereits_beworben("fail-001") is True

    def test_bewerbung_speichern_duplicate_upsert(self, db):
        angebot = make_angebot(id="dup-001")
        db.bewerbung_speichern(angebot, erfolgreich=True)
        db.bewerbung_speichern(angebot, erfolgreich=False)
        # Should still be there, no exception
        assert db.ist_bereits_beworben("dup-001") is True

    def test_log_speichern(self, db):
        db.log_speichern("INFO", "Test log message", angebot_id="log-001")
        with sqlite3.connect(db.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT level, message, angebot_id FROM logs WHERE angebot_id = ?", ("log-001",))
            row = cursor.fetchone()
        assert row is not None
        assert row[0] == "INFO"
        assert row[1] == "Test log message"
        assert row[2] == "log-001"

    def test_log_speichern_without_angebot_id(self, db):
        db.log_speichern("ERROR", "Something went wrong")
        with sqlite3.connect(db.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM logs WHERE message = ?", ("Something went wrong",))
            row = cursor.fetchone()
        assert row is not None

    def test_multiple_bewerbungen(self, db):
        angebote = [make_angebot(id=f"multi-{i}") for i in range(5)]
        for a in angebote:
            db.bewerbung_speichern(a, erfolgreich=True)
        for a in angebote:
            assert db.ist_bereits_beworben(a.id) is True
        assert db.ist_bereits_beworben("multi-99") is False

    def test_bewerbung_data_persisted_correctly(self, db):
        angebot = make_angebot(
            id="data-001",
            titel="Persisted Wohnung",
            preis=1500.0,
            groesse=80.0,
            zimmer=3,
            ort="München",
            website="immonet",
        )
        db.bewerbung_speichern(angebot, erfolgreich=True)
        with sqlite3.connect(db.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT titel, preis, groesse, zimmer, ort, erfolgreich FROM bewerbungen WHERE id = ?", ("data-001",))
            row = cursor.fetchone()
        assert row[0] == "Persisted Wohnung"
        assert row[1] == 1500.0
        assert row[2] == 80.0
        assert row[3] == 3
        assert row[4] == "München"
        assert row[5] == 1  # SQLite stores bool as int


# ---------------------------------------------------------------------------
# ImmonetScraper URL / parsing helpers tests
# ---------------------------------------------------------------------------

class TestImmonetScraperParsing:
    @pytest.fixture
    def scraper(self):
        config = make_config()
        with patch("selenium.webdriver.Chrome"):
            s = ImmonetScraper(config)
        s.driver = None  # Prevent real driver usage
        return s

    def test_get_location_id_berlin(self, scraper):
        assert scraper._get_location_id("Berlin") == "AD08DE8634"

    def test_get_location_id_muenchen(self, scraper):
        assert scraper._get_location_id("München") == "AD08DE8635"

    def test_get_location_id_hamburg(self, scraper):
        assert scraper._get_location_id("Hamburg") == "AD08DE8636"

    def test_get_location_id_unknown_falls_back_to_berlin(self, scraper):
        assert scraper._get_location_id("UnknownCity") == "AD08DE8634"

    def test_extract_id_from_uuid_url(self, scraper):
        url = "https://www.immonet.de/expose/3814ec52-e485-45f0-8d7e-512e039d9c66"
        result = scraper._extract_id_from_url(url)
        assert result == "3814ec52-e485-45f0-8d7e-512e039d9c66"

    def test_extract_id_from_non_uuid_url(self, scraper):
        url = "https://www.immonet.de/expose/12345"
        result = scraper._extract_id_from_url(url)
        assert result == "12345"

    def test_parse_preis_standard(self, scraper):
        assert scraper._parse_preis("1.472 € Kaltmiete") == 1472.0

    def test_parse_preis_simple(self, scraper):
        assert scraper._parse_preis("950") == 950.0

    def test_parse_preis_with_comma(self, scraper):
        result = scraper._parse_preis("1.200,50 €")
        # After replace('.','') and (',','.') the string becomes "1200.50 €"
        assert result == 1200.50

    def test_parse_preis_empty(self, scraper):
        assert scraper._parse_preis("") == 0.0

    def test_parse_preis_no_number(self, scraper):
        assert scraper._parse_preis("auf Anfrage") == 0.0

    def test_extract_zimmer_standard(self, scraper):
        assert scraper._extract_zimmer("3 Zimmer, 75 m²") == 3

    def test_extract_zimmer_default_when_absent(self, scraper):
        assert scraper._extract_zimmer("keine Info") == 2

    def test_extract_groesse_standard(self, scraper):
        assert scraper._extract_groesse("75 m²") == 75.0

    def test_extract_groesse_with_comma(self, scraper):
        assert scraper._extract_groesse("67,5 m²") == 67.5

    def test_extract_groesse_default_when_absent(self, scraper):
        assert scraper._extract_groesse("keine Info") == 50.0

    def test_erfuellt_kriterien_passes(self, scraper):
        angebot = make_angebot(preis=1500.0, zimmer=2)
        assert scraper._erfuellt_kriterien(angebot) is True

    def test_erfuellt_kriterien_preis_too_high(self, scraper):
        angebot = make_angebot(preis=9999.0, zimmer=2)
        assert scraper._erfuellt_kriterien(angebot) is False

    def test_erfuellt_kriterien_zimmer_too_few(self, scraper):
        scraper.config.min_zimmer = 3
        angebot = make_angebot(preis=1000.0, zimmer=1)
        assert scraper._erfuellt_kriterien(angebot) is False

    def test_erfuellt_kriterien_zimmer_too_many(self, scraper):
        scraper.config.max_zimmer = 3
        angebot = make_angebot(preis=1000.0, zimmer=6)
        assert scraper._erfuellt_kriterien(angebot) is False

    def test_get_random_user_agent_returns_string(self, scraper):
        ua = scraper.get_random_user_agent()
        assert isinstance(ua, str)
        assert "Mozilla" in ua


# ---------------------------------------------------------------------------
# ImmonetScraper.suche_neue_angebote with mocked HTTP
# ---------------------------------------------------------------------------

class TestImmonetScraperHTTP:
    @pytest.fixture
    def scraper(self):
        config = make_config(max_preis=2000.0, min_zimmer=1, max_zimmer=5)
        with patch("selenium.webdriver.Chrome"):
            s = ImmonetScraper(config)
        s.driver = None
        return s

    def _make_html(self, items_html: str) -> str:
        return f"""
        <html><body>
            {items_html}
        </body></html>
        """

    def _make_item(self, href="/expose/3814ec52-e485-45f0-8d7e-512e039d9c66",
                   title="Test Wohnung", price="1200 €",
                   details="2 Zimmer, 60 m²"):
        return f"""
        <div class="classified-item">
            <a href="{href}">Link</a>
            <h2>{title}</h2>
            <span class="price">{price}</span>
            <div class="details">{details}</div>
        </div>
        """

    @patch("time.sleep")
    def test_suche_returns_angebote(self, mock_sleep, scraper):
        html = self._make_html(self._make_item())
        mock_resp = MagicMock()
        mock_resp.content = html.encode()
        mock_resp.raise_for_status = MagicMock()

        with patch.object(scraper.session, "get", return_value=mock_resp):
            result = scraper.suche_neue_angebote("Berlin")

        assert isinstance(result, list)
        assert len(result) == 1
        assert result[0].website == "immonet"
        assert result[0].ort == "Berlin"

    @patch("time.sleep")
    def test_suche_empty_html_returns_empty_list(self, mock_sleep, scraper):
        html = "<html><body></body></html>"
        mock_resp = MagicMock()
        mock_resp.content = html.encode()
        mock_resp.raise_for_status = MagicMock()

        with patch.object(scraper.session, "get", return_value=mock_resp):
            result = scraper.suche_neue_angebote("Berlin")

        assert result == []

    @patch("time.sleep")
    def test_suche_connection_error_returns_empty_list(self, mock_sleep, scraper):
        with patch.object(scraper.session, "get", side_effect=Exception("Connection refused")):
            result = scraper.suche_neue_angebote("Berlin")

        assert result == []

    @patch("time.sleep")
    def test_suche_filters_expensive_angebote(self, mock_sleep, scraper):
        scraper.config.max_preis = 800.0
        html = self._make_html(self._make_item(price="1200 €"))
        mock_resp = MagicMock()
        mock_resp.content = html.encode()
        mock_resp.raise_for_status = MagicMock()

        with patch.object(scraper.session, "get", return_value=mock_resp):
            result = scraper.suche_neue_angebote("Berlin")

        assert result == []

    @patch("time.sleep")
    def test_suche_malformed_html_does_not_crash(self, mock_sleep, scraper):
        html = "<html><body><div class='classified-item'><BROKEN><<</div></body></html>"
        mock_resp = MagicMock()
        mock_resp.content = html.encode()
        mock_resp.raise_for_status = MagicMock()

        with patch.object(scraper.session, "get", return_value=mock_resp):
            result = scraper.suche_neue_angebote("Berlin")

        assert isinstance(result, list)

    @patch("time.sleep")
    def test_suche_multiple_angebote(self, mock_sleep, scraper):
        items = "".join([
            self._make_item(
                href=f"/expose/3814ec52-e485-45f0-8d7e-512e039d9c{i:02d}",
                title=f"Wohnung {i}",
                price="1000 €"
            )
            for i in range(3)
        ])
        html = self._make_html(items)
        mock_resp = MagicMock()
        mock_resp.content = html.encode()
        mock_resp.raise_for_status = MagicMock()

        with patch.object(scraper.session, "get", return_value=mock_resp):
            result = scraper.suche_neue_angebote("Berlin")

        assert len(result) == 3

    @patch("time.sleep")
    def test_suche_item_without_link_skipped(self, mock_sleep, scraper):
        html = self._make_html('<div class="classified-item"><h2>No Link</h2></div>')
        mock_resp = MagicMock()
        mock_resp.content = html.encode()
        mock_resp.raise_for_status = MagicMock()

        with patch.object(scraper.session, "get", return_value=mock_resp):
            result = scraper.suche_neue_angebote("Berlin")

        assert result == []


# ---------------------------------------------------------------------------
# ImmobilienScout24Scraper tests
# ---------------------------------------------------------------------------

class TestImmobilienScout24Scraper:
    @pytest.fixture
    def scraper(self):
        config = make_config()
        with patch("selenium.webdriver.Chrome"):
            s = ImmobilienScout24Scraper(config)
        s.driver = None
        return s

    def test_suche_returns_empty_list(self, scraper):
        result = scraper.suche_neue_angebote("Berlin")
        assert result == []

    def test_bewerbe_returns_false(self, scraper):
        angebot = make_angebot()
        result = scraper.bewerbe_auf_angebot(angebot)
        assert result is False


# ---------------------------------------------------------------------------
# Functional / integration-like test with full scrape + DB flow
# ---------------------------------------------------------------------------

class TestFullFlow:
    @patch("time.sleep")
    def test_scrape_then_save_to_db(self, mock_sleep, tmp_path):
        config = make_config(max_preis=2000.0)
        with patch("selenium.webdriver.Chrome"):
            scraper = ImmonetScraper(config)
        scraper.driver = None

        html = """
        <html><body>
            <div class="classified-item">
                <a href="/expose/aaaaaaaa-bbbb-cccc-dddd-eeeeeeeeeeee">Link</a>
                <h2>Schöne Wohnung im Prenzlauer Berg</h2>
                <span class="price">1150 €</span>
                <div class="details">3 Zimmer, 85 m²</div>
            </div>
        </body></html>
        """
        mock_resp = MagicMock()
        mock_resp.content = html.encode()
        mock_resp.raise_for_status = MagicMock()

        db = DatabaseManager(db_path=str(tmp_path / "flow.db"))

        with patch.object(scraper.session, "get", return_value=mock_resp):
            angebote = scraper.suche_neue_angebote("Berlin")

        assert len(angebote) == 1
        angebot = angebote[0]

        # Not yet applied
        assert not db.ist_bereits_beworben(angebot.id)

        # Save as successful application
        db.bewerbung_speichern(angebot, erfolgreich=True)
        assert db.ist_bereits_beworben(angebot.id)

        # Second run: same listing should be filtered
        with patch.object(scraper.session, "get", return_value=mock_resp):
            angebote2 = scraper.suche_neue_angebote("Berlin")

        new_ones = [a for a in angebote2 if not db.ist_bereits_beworben(a.id)]
        assert new_ones == []


# ---------------------------------------------------------------------------
# Regression / edge case tests
# ---------------------------------------------------------------------------

class TestEdgeCases:
    @pytest.fixture
    def scraper(self):
        config = make_config()
        with patch("selenium.webdriver.Chrome"):
            s = ImmonetScraper(config)
        s.driver = None
        return s

    def test_angebot_with_zero_preis_still_fulfills_criteria(self, scraper):
        angebot = make_angebot(preis=0.0, zimmer=2)
        assert scraper._erfuellt_kriterien(angebot) is True

    def test_preis_exactly_at_max(self, scraper):
        scraper.config.max_preis = 1000.0
        angebot = make_angebot(preis=1000.0, zimmer=2)
        assert scraper._erfuellt_kriterien(angebot) is True

    def test_preis_one_cent_over_max(self, scraper):
        scraper.config.max_preis = 1000.0
        angebot = make_angebot(preis=1000.01, zimmer=2)
        assert scraper._erfuellt_kriterien(angebot) is False

    def test_zimmer_at_min_boundary(self, scraper):
        scraper.config.min_zimmer = 2
        angebot = make_angebot(preis=500.0, zimmer=2)
        assert scraper._erfuellt_kriterien(angebot) is True

    def test_zimmer_at_max_boundary(self, scraper):
        scraper.config.max_zimmer = 4
        angebot = make_angebot(preis=500.0, zimmer=4)
        assert scraper._erfuellt_kriterien(angebot) is True

    def test_parse_preis_zero_string(self, scraper):
        assert scraper._parse_preis("0") == 0.0

    def test_extract_zimmer_multi_digit(self, scraper):
        assert scraper._extract_zimmer("12 Zimmer Haus") == 12

    def test_extract_groesse_large_value(self, scraper):
        assert scraper._extract_groesse("350 m²") == 350.0

    def test_config_empty_suchstaedte_list(self):
        config = BewerbungsConfig(suchstaedte=[])
        assert config.suchstaedte == []

    def test_angebot_titel_empty_string(self):
        angebot = make_angebot(titel="")
        assert angebot.titel == ""

    @patch("time.sleep")
    def test_http_404_handled_gracefully(self, mock_sleep, scraper):
        import requests as req_lib
        mock_resp = MagicMock()
        mock_resp.raise_for_status.side_effect = req_lib.exceptions.HTTPError("404")

        with patch.object(scraper.session, "get", return_value=mock_resp):
            result = scraper.suche_neue_angebote("Hamburg")

        assert result == []
