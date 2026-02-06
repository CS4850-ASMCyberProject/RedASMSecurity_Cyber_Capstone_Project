import sqlite3
import os

db_dir = '/srv/asm_project/data/'
db_path = os.join(db_dir, 'asm_assets.db')

def intialize_db():
    if not os.path.exists(db_dr):
        os.makedirs(db_dir)
        print(f"Created directory for database at {db_dir}")

    connection = sqlite3.connect(db_path)
    cursor = connection.cursor()

    connection.execute('PRAGMA foreign_keys = ON;')
    
    cursor.executescript('''
    --Table 1: assets
    CREATE TABLE IF NOT EXISTS assets (
        id INTEGER PRIMARY KEY,
        subdomain TEXT UNIQUE,
        ip_address TEXT,
        tech_stack TEXT,
        vt_score INTEGER DEFAULT 0,
        is_active BOOLEAN DEFAULT 1,
        time_stamp DATETIME DEFAULT CURRENT_TIMESTAMP

    );
    CREATE INDEX IF NOT EXISTS idx_subdomain ON assets(subdomain);

    --Table 2: scan_history
    CREATE TABLE IF NOT EXISTS scan_history (
        id INTEGER PRIMARY KEY,
        asset_id INTEGER,
        change_type TEXT, --eg: 'IP_CHANGE', 'TECH_STACK_CHANGE', 'VT_SCORE_CHANGE', 'STATUS_CHANGE'
        old_value TEXT,
        new_value TEXT,
        time_change DATETIME DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (asset_id) REFERENCES assets(id)
    );
    CREATE INDEX IF NOT EXISTS idx_asset_id ON scan_history(asset_id);

''')

    connection.commit()
    connection.close()

    print("Database has been created and initialized")


def upsert_asset(subdomain, ip_address, tech_stack):
    connection = sqlite3.connect(db_path)
    cursor = connection.cursor()

    cursor.execute("SELECT id, ip_address, tech_stack FROM assets WHERE subdomain = ?", (subdomain,))
    result = cursor.fetchone()

    if not result:
        print(f"Inserting new asset: {subdomain}")
        cursor.execute("INSERT INTO assets (subdomain, ip_address, tech_stack) VALUES (?, ?, ?)",(subdomain, ip_address, tech_stack))

