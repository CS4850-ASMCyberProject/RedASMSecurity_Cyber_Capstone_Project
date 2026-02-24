import sqlite3
import os

# Define the directory and full path for the database file
db_dir = '/srv/asm_project/data/'
db_path = os.path.join(db_dir, 'asm_assets.db') # Note: Fixed os.join to os.path.join for you

def initialize_db():
    # Create the data directory if it doesn't already exist
    if not os.path.exists(db_dir): # Note: Fixed db_dr to db_dir for you
        os.makedirs(db_dir)
        print(f"Created directory for database at {db_dir}")

    # Establish a connection to the SQLite database file
    connection = sqlite3.connect(db_path)
    cursor = connection.cursor()

    # Enable Foreign Key support (required for the link between assets and history)
    connection.execute('PRAGMA foreign_keys = ON;')
    
    # Define the structure of the database using SQL
    cursor.executescript('''
    -- Table 1: Master list of discovered subdomains and their current state
    CREATE TABLE IF NOT EXISTS assets (
        id INTEGER PRIMARY KEY,
        subdomain TEXT UNIQUE,
        ip_address TEXT,
        tech_stack TEXT,
        vt_score INTEGER DEFAULT 0,
        is_active BOOLEAN DEFAULT 1,
        time_stamp DATETIME DEFAULT CURRENT_TIMESTAMP

    );
    -- Index to make searching by subdomain lightning fast
    CREATE INDEX IF NOT EXISTS idx_subdomain ON assets(subdomain);

    -- Table 2: Audit trail to track every change (Drift) over time
    CREATE TABLE IF NOT EXISTS scan_history (
        id INTEGER PRIMARY KEY,
        asset_id INTEGER,
        change_type TEXT, -- e.g., 'IP_CHANGE', 'TECH_STACK_CHANGE', 'VT_SCORE_CHANGE'
        old_value TEXT,
        new_value TEXT,
        time_change DATETIME DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (asset_id) REFERENCES assets(id)
    );
    -- Index to quickly pull the history of a specific asset
    CREATE INDEX IF NOT EXISTS idx_asset_id ON scan_history(asset_id);

''')

    # Save changes and close the connection
    connection.commit()
    connection.close()

    print("Database has been created and initialized")


def upsert_asset(subdomain, ip_address, tech_stack):
    # Connect to the database to perform a lookup/update
    connection = sqlite3.connect(db_path)
    cursor = connection.cursor()

    # Check if we have seen this subdomain before
    cursor.execute("SELECT id, ip_address, tech_stack FROM assets WHERE subdomain = ?", (subdomain,))
    result = cursor.fetchone()

    # If result is empty, this is a brand new discovery
    if not result:
        print(f"[*] Inserting new asset: {subdomain}")
        cursor.execute("INSERT INTO assets (subdomain, ip_address, tech_stack) VALUES (?, ?, ?)",
                       (subdomain, ip_address, tech_stack))

        new_asset_id = cursor.lastrowid
        
        cursor.execute("""
            INSERT INTO scan_history (asset_id, change_type, new_value)
            VALUES (?, 'INITIAL_DISCOVERY', ?)
        """, (new_asset_id, subdomain))

    else:
        asset_id, old_ip, old_tech = result

        if ip_address != old_ip:
            print(f"IP address change detected for {subdomain}: {old_ip} -> {ip_address}")
            cursor.execute("UPDATE assets SET ip_address = ?, time_stamp = CURRENT_TIMESTAMP WHERE id = ?",
            (ip_address, asset_id))
            
            cursor.execute("""
            INSERT INTO scan_history (asset_id, change_type, old_value, new_value)
            VALUES (?, 'IP_CHANGE', ?, ?)
            """, (asset_id, old_ip, ip_address))



        if tech_stack != old_tech:
            print(f"Tech stack change detected for {subdomain}: {old_tech} -> {tech_stack}")
            cursor.execute("UPDATE assets SET tech_stack = ?, time_stamp = CURRENT_TIMESTAMP WHERE id = ?",
            (tech_stack, asset_id))
            
            cursor.execute("""
            INSERT INTO scan_history (asset_id, change_type, old_value, new_value)
            VALUES (?, 'TECH_STACK_CHANGE', ?, ?)
            """, (asset_id, old_tech, tech_stack))

    connection.commit()
    connection.close()

# Example usage: