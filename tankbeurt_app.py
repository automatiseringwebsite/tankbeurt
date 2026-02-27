#!/usr/bin/env python3
"""
Tankbeurt Formulier Backend (Zonder flask-cors)
Flask server om tankbeurten te verzamelen en op te slaan
"""

from flask import Flask, request, jsonify, send_from_directory
from flask import Response
import sqlite3
import os
from datetime import datetime

# Database pad - dynamisch voor Render en lokaal
# Render: /opt/render/project/src/tankbeurten.db
# Lokaal: tankbeurten.db in dezelfde map
if os.path.exists('/opt/render/project/src'):
    DB_PATH = '/opt/render/project/src/tankbeurten.db'
    STATIC_FOLDER = '/opt/render/project/src'
else:
    DB_PATH = os.path.join(os.path.dirname(__file__), 'tankbeurten.db')
    STATIC_FOLDER = os.path.dirname(__file__)

app = Flask(__name__, static_folder=STATIC_FOLDER)

# CORS headers toevoegen
@app.after_request
def add_cors_headers(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'GET, POST, DELETE, OPTIONS'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type'
    return response

# OPTIONS request handler
@app.route('/', methods=['OPTIONS'])
@app.route('/api/<path:path>', methods=['OPTIONS'])
def options_handler(path=None):
    response = jsonify()
    return add_cors_headers(response)

def get_db():
    """Maak database connectie"""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """Initialiseer database"""
    conn = get_db()
    c = conn.cursor()
    
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
    print("✓ Database geïnitialiseerd")

@app.route('/')
def index():
    """Serveer het HTML formulier"""
    try:
        # Probeer index.html
        return send_from_directory(STATIC_FOLDER, 'index.html')
    except Exception as e:
        # Fallback: tankbeurt_formulier.html
        try:
            return send_from_directory(STATIC_FOLDER, 'tankbeurt_formulier.html')
        except Exception as e2:
            # Als beide niet werken, toon debug info
            return jsonify({
                'error': 'Geen HTML bestand gevonden',
                'static_folder': STATIC_FOLDER,
                'files': os.listdir(STATIC_FOLDER) if os.path.exists(STATIC_FOLDER) else [],
                'original_error': str(e),
                'fallback_error': str(e2)
            }), 500

@app.route('/api/debug')
def debug_info():
    """Debug informatie"""
    return jsonify({
        'static_folder': STATIC_FOLDER,
        'db_path': DB_PATH,
        'static_folder_exists': os.path.exists(STATIC_FOLDER),
        'db_exists': os.path.exists(DB_PATH),
        'current_dir': os.getcwd(),
        'script_dir': os.path.dirname(__file__),
        'files_in_static': os.listdir(STATIC_FOLDER) if os.path.exists(STATIC_FOLDER) else []
    })

@app.route('/api/tankbeurten', methods=['GET'])
def get_tankbeurten():
    """Haal alle tankbeurten op"""
    conn = get_db()
    c = conn.cursor()
    
    c.execute("""
        SELECT * FROM tankbeurten 
        ORDER BY datum DESC, tijd DESC 
        LIMIT 50
    """)
    
    tankbeurten = [dict(row) for row in c.fetchall()]
    conn.close()
    
    return jsonify(tankbeurten)

@app.route('/api/tankbeurten', methods=['POST'])
def add_tankbeurt():
    """Voeg een nieuwe tankbeurt toe"""
    data = request.json
    
    try:
        conn = get_db()
        c = conn.cursor()
        
        # Bereken gereden km indien niet opgegeven
        km_voor = data.get('kilometerstand_voor')
        km_na = data.get('kilometerstand_na')
        
        if km_voor and km_na:
            gereden = float(km_na) - float(km_voor)
        else:
            gereden = None
        
        # Voeg tankbeurt toe
        c.execute("""
            INSERT INTO tankbeurten (
                datum, tijd, station_naam, station_merk, station_adres,
                stad, provincie, brandstof_soort, brandstof_prijs_per_liter,
                aantal_liters, totaal_bedrag, kilometerstand_voor, kilometerstand_na,
                gereden_km, opmerkingen, foto_pad
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            data.get('datum'),
            data.get('tijd'),
            data.get('station_naam'),
            data.get('station_merk'),
            data.get('station_adres'),
            data.get('stad'),
            data.get('provincie'),
            data.get('brandstof'),
            data.get('brandstof_prijs_per_liter'),
            data.get('aantal_liters'),
            data.get('totaal_bedrag'),
            data.get('kilometerstand_voor'),
            data.get('kilometerstand_na'),
            gereden,
            data.get('opmerkingen'),
            data.get('foto_pad')
        ))
        
        conn.commit()
        tankbeurt_id = c.lastrowid
        conn.close()
        
        print(f"✅ Tankbeurt #{tankbeurt_id} toegevoegd: {data.get('station_naam')} - €{data.get('totaal_bedrag', 0)}")
        
        return jsonify({
            'success': True,
            'tankbeurt_id': tankbeurt_id,
            'message': 'Tankbeurt opgeslagen!'
        })
        
    except Exception as e:
        print(f"❌ FOUT bij opslaan: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/statistieken')
def get_statistieken():
    """Bereken basis statistieken"""
    conn = get_db()
    c = conn.cursor()
    
    c.execute("""
        SELECT
            COUNT(*) as aantal,
            SUM(totaal_bedrag) as totaal_uitgegeven,
            AVG(brandstof_prijs_per_liter) as gemiddelde_prijs,
            SUM(aantal_liters) as totaal_liters,
            AVG(gereden_km) as gemiddelde_km_per_tank
        FROM tankbeurten
    """)
    
    stats = dict(c.fetchone())
    conn.close()
    
    return jsonify(stats)

@app.route('/api/exporteer/csv')
def exporteer_csv():
    """Exporteer tankbeurten naar CSV"""
    conn = get_db()
    c = conn.cursor()
    
    c.execute("""
        SELECT * FROM tankbeurten 
        ORDER BY datum DESC, tijd DESC
    """)
    
    rows = c.fetchall()
    conn.close()
    
    # CSV string bouwen
    import io
    import csv
    
    output = io.StringIO()
    writer = csv.writer(output)
    
    # Header
    writer.writerow(['ID', 'Datum', 'Tijd', 'Station', 'Merk', 'Adres', 
                  'Stad', 'Provincie', 'Brandstof', 'Prijs/Liter', 'Liters', 'Totaal',
                  'Km Vóór', 'Km Na', 'Gereden Km', 'Opmerkingen', 'Foto Pad'])
    
    # Data
    for row in rows:
        writer.writerow(list(row))
    
    # Response
    response = app.response_class(
        output.getvalue().encode('utf-8'),
        mimetype='text/csv',
        headers={'Content-Disposition': f'attachment; filename=tankbeurten_{datetime.now().strftime("%Y%m%d")}.csv'}
    )
    
    return add_cors_headers(response)

@app.route('/api/tankbeurten/<int:tankbeurt_id>', methods=['DELETE'])
def delete_tankbeurt(tankbeurt_id):
    """Verwijder een tankbeurt"""
    conn = get_db()
    c = conn.cursor()

    c.execute("DELETE FROM tankbeurten WHERE id = ?", (tankbeurt_id,))
    conn.commit()
    conn.close()

    return jsonify({'success': True, 'message': 'Tankbeurt verwijderd'})

@app.route('/api/tankbeurten/<int:tankbeurt_id>', methods=['PUT'])
def update_tankbeurt(tankbeurt_id):
    """Update een bestaande tankbeurt"""
    data = request.json

    try:
        conn = get_db()
        c = conn.cursor()

        # Bereken gereden km indien nodig
        km_voor = data.get('kilometerstand_voor')
        km_na = data.get('kilometerstand_na')

        if km_voor and km_na:
            gereden = float(km_na) - float(km_voor)
        else:
            gereden = None

        # Update tankbeurt
        c.execute("""
            UPDATE tankbeurten SET
                datum = ?,
                tijd = ?,
                station_naam = ?,
                station_merk = ?,
                station_adres = ?,
                stad = ?,
                provincie = ?,
                brandstof_soort = ?,
                brandstof_prijs_per_liter = ?,
                aantal_liters = ?,
                totaal_bedrag = ?,
                kilometerstand_voor = ?,
                kilometerstand_na = ?,
                gereden_km = ?,
                opmerkingen = ?
            WHERE id = ?
        """, (
            data.get('datum'),
            data.get('tijd'),
            data.get('station_naam'),
            data.get('station_merk'),
            data.get('station_adres'),
            data.get('stad'),
            data.get('provincie'),
            data.get('brandstof'),
            data.get('brandstof_prijs_per_liter'),
            data.get('aantal_liters'),
            data.get('totaal_bedrag'),
            data.get('kilometerstand_voor'),
            data.get('kilometerstand_na'),
            gereden,
            data.get('opmerkingen'),
            tankbeurt_id
        ))

        conn.commit()
        conn.close()

        print(f"✅ Tankbeurt #{tankbeurt_id} bijgewerkt")

        return jsonify({
            'success': True,
            'tankbeurt_id': tankbeurt_id,
            'message': 'Tankbeurt bijgewerkt!'
        })

    except Exception as e:
        print(f"❌ FOUT bij bijwerken: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

# Initialiseer database bij app import (werkt ook met gunicorn)
print("🔧 Database initialiseren...")
init_db()

if __name__ == '__main__':
    # Start server
    print("\n" + "="*50)
    print("🚗 Tankbeurt Formulier Backend")
    print("="*50)
    print(f"📝 Formulier: http://localhost:5000")
    print(f"📊 API: http://localhost:5000/api/tankbeurten")
    print(f"📈 Statistieken: http://localhost:5000/api/statistieken")
    print(f"📥 CSV Export: http://localhost:5000/api/exporteer/csv")
    print("="*50)
    print("\nDruk Ctrl+C om te stoppen\n")
    
    app.run(host='0.0.0.0', port=5000, debug=True)
