#!/usr/bin/env python3
"""
Initialiseer de database voor Render deploy
Dit script maakt automatisch de database aan als die niet bestaat
"""

import os
import sys

def init_database():
    """Maak database aan als die niet bestaat"""
    from tankbeurt_database import init_db

    # Database pad voor Render
    db_path = '/opt/render/project/src/tankbeurten.db'

    # Als de database niet bestaat, maak hem aan
    if not os.path.exists(db_path):
        print(f"🔨 Database aanmaken op: {db_path}")
        init_db()
        print("✅ Database aangemaakt!")
    else:
        print("✅ Database bestaat al!")

if __name__ == '__main__':
    init_database()
