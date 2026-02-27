#!/usr/bin/env python3
"""
Tankbeurt Database
SQLite database om tankbeurten te tracken en analyseren
"""

import sqlite3
import json
import os
from datetime import datetime

def init_db():
    """
    Initialiseer de database (compatibel met Flask)
    Maak database aan als die nog niet bestaat
    """
    # Database pad - dynamisch voor Render en lokaal
    if os.path.exists('/opt/render/project/src'):
        db_path = '/opt/render/project/src/tankbeurten.db'
    else:
        db_path = os.path.join(os.path.dirname(__file__), 'tankbeurten.db')

    # Maak connectie en tabellen
    conn = sqlite3.connect(db_path)
    c = conn.cursor()

    # Tankbeurten tabel
    c.execute("""
        CREATE TABLE IF NOT EXISTS tankbeurten (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            datum TEXT NOT NULL,
            tijd TEXT,
            station_naam TEXT,
            station_merk TEXT,
            station_adres TEXT,
            stad TEXT,
            provincie TEXT,
            brandstof_soort TEXT,
            brandstof_prijs_per_liter REAL,
            aantal_liters REAL,
            totaal_bedrag REAL,
            kilometerstand_voor REAL,
            kilometerstand_na REAL,
            gereden_km REAL,
            opmerkingen TEXT,
            auto_id INTEGER,
            foto_pad TEXT,
            aangemaakt_op TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    conn.commit()
    conn.close()

    return db_path

class TankbeurtDatabase:
    def __init__(self, db_path="/Users/imace/clawd/tankbeurten.db"):
        self.conn = sqlite3.connect(db_path)
        self.cursor = self.conn.cursor()
        self._create_tables()

    def _create_tables(self):
        """Maak tabellen aan als ze niet bestaan"""
        # Hoofdtabel: Tankbeurten
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS tankbeurten (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                datum TEXT NOT NULL,
                tijd TEXT,
                station_naam TEXT,
                station_merk TEXT,
                station_adres TEXT,
                station_stad TEXT,
                station_provincie TEXT,

                brandstof_soort TEXT,  -- benzine, diesel, lpg, electra
                brandstof_prijs_per_liter REAL,  -- in euro's
                aantal_liters REAL,
                totaal_bedrag REAL,

                kilometerstand_voor REAL,
                kilometerstand_na REAL,
                gereden_km REAL,

                betaling_methode TEXT,  -- pin, contactloos, app
                auto_id INTEGER,

                foto_path TEXT,
                opmerkingen TEXT,

                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        # Auto-tabel
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS autos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                merk TEXT,
                model TEXT,
                bouwjaar INTEGER,
                kenteken TEXT,
                brandstof_type TEXT,  -- benzine, diesel, lpg, electra
                UNIQUE(merk, model, kenteken)
            )
        """)

        # Tankstation-tabel (voor locaties)
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS tankstations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                naam TEXT,
                merk TEXT,
                adres TEXT,
                postcode TEXT,
                stad TEXT,
                provincie TEXT,
                latitude REAL,
                longitude REAL,
                is_active BOOLEAN DEFAULT 1,
                UNIQUE(naam, adres)
            )
        """)

        self.conn.commit()
        print("✓ Tabellen aangemaakt")

    def tankbeurt_toevoegen(self, data):
        """Voeg een nieuwe tankbeurt toe"""
        self.cursor.execute("""
            INSERT INTO tankbeurten (
                datum, tijd, station_naam, station_merk, station_stad,
                brandstof_soort, brandstof_prijs_per_liter, aantal_liters, totaal_bedrag,
                kilometerstand_voor, kilometerstand_na, gereden_km,
                auto_id, foto_path, opmerkingen
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
                data['datum'],
                data.get('tijd'),
                data['station_naam'],
                data.get('station_merk'),
                data.get('station_stad'),
                data['brandstof_soort'],
                data.get('brandstof_prijs_per_liter'),
                data.get('aantal_liters'),
                data.get('totaal_bedrag'),
                data.get('kilometerstand_voor'),
                data.get('kilometerstand_na'),
                data.get('gereden_km'),
                data.get('auto_id'),
                data.get('foto_path'),
                data.get('opmerkingen')
            ))
        self.conn.commit()
        print(f"✓ Tankbeurt toegevoegd: €{data.get('totaal_bedrag', 0)}")

    def alle_tankbeurten(self):
        """Haal alle tankbeurten op"""
        self.cursor.execute("SELECT * FROM tankbeurten ORDER BY datum DESC, tijd DESC")
        return self.cursor.fetchall()

    def statistieken(self):
        """Bereken basis statistieken"""
        self.cursor.execute("""
            SELECT
                COUNT(*) as aantal,
                SUM(totaal_bedrag) as totaal_uitgegeven,
                AVG(brandstof_prijs_per_liter) as gemiddelde_prijs,
                SUM(aantal_liters) as totaal_liters,
                AVG(gereden_km) as gemiddelde_km_per_tank
            FROM tankbeurten
        """)
        return self.cursor.fetchone()

    def exporteer_naar_csv(self, bestandsnaam):
        """Exporteer data naar CSV"""
        import csv
        self.cursor.execute("SELECT * FROM tankbeurten ORDER BY datum DESC")
        rows = self.cursor.fetchall()

        with open(bestandsnaam, 'w', newline='') as f:
            writer = csv.writer(f)
            # Header
            writer.writerow(['Datum', 'Tijd', 'Station', 'Merk', 'Stad',
                          'Brandstof', 'Prijs/Liter', 'Liters', 'Totaal',
                          'Km Vóór', 'Km Na', 'Gereden Km'])
            # Data
            for row in rows:
                writer.writerow([row[1], row[2], row[3], row[4], row[5],
                                row[6], row[7], row[8], row[9],
                                row[10], row[11], row[12]])

        print(f"✓ Geëxporteerd naar {bestandsnaam}")

    def sluit(self):
        self.conn.close()


# Voorbeeld gebruik
if __name__ == "__main__":
    db = TankbeurtDatabase()

    # Voorbeeld tankbeurt (pas dit aan met je echte data!)
    voorbeeld_data = {
        'datum': '2026-02-24',
        'tijd': '14:30',
        'station_naam': 'Shell - Centrum',
        'station_merk': 'Shell',
        'station_stad': 'Utrecht',
        'brandstof_soort': 'Euro 95',
        'brandstof_prijs_per_liter': 1.92,
        'aantal_liters': 32.5,
        'totaal_bedrag': 62.40,
        'kilometerstand_voor': 145230,
        'kilometerstand_na': 145680,
        'gereden_km': 450,
        'foto_path': '/pad/naar/foto.jpg',
        'opmerkingen': 'Goede prijs vandaag'
    }

    print("\n📊 Tankbeurt Database - Template")
    print("="*50)
    print("\nVul de tankbeurt in met echte data van je foto's:")
    print("- Station naam en merk")
    print("- Prijs per liter en aantal liters")
    print("- Totaal bedrag (van de bon)")
    print("- Kilometerstand voor en na")
    print("- Brandstof soort (Euro 95/Euro 98/Diesel/LPG)")

    # Voeg voorbeeld toe (verwijder dit in productie!)
    # db.tankbeurt_toevoegen(voorbeeld_data)

    # Toon statistieken
    print("\n" + "="*50)
    print("📈 Actuele statistieken:")
    stats = db.statistieken()
    if stats[0] > 0:
        print(f"  Aantal tankbeurten: {stats[0]}")
        print(f"  Totaal uitgegeven: €{stats[1]:.2f}")
        print(f"  Gemiddelde prijs: €{stats[2]:.3f}/liter")
        print(f"  Totaal liters: {stats[3]:.1f}")
        if stats[4]:
            print(f"  Gemiddeld km/tank: {stats[4]:.1f}")

    db.sluit()
