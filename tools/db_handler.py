import mysql.connector
from datetime import datetime

# --- VM CONNECTION CONFIG ---
VM_IP = "129.213.96.223" 
DB_USER = "asm_user"
DB_PASS = "062504K" # Set this on the VM
DB_NAME = "asm_project"

def get_connection():
    try:
        return mysql.connector.connect(
            host=VM_IP,
            user=DB_USER,
            password=DB_PASS,
            database=DB_NAME
        )
    except Exception as e:
        print(f"[!] DB Connection Failed: {e}")
        return None

def upsert_asset(subdomain, ip_address, tech_stack):
    conn = get_connection()
    if not conn: return
    
    cursor = conn.cursor()

    # 1. Check if we've seen this subdomain
    cursor.execute("SELECT id, ip_address, tech_stack FROM assets WHERE subdomain = %s", (subdomain,))
    result = cursor.fetchone()

    if not result:
        # BRAND NEW DISCOVERY
        print(f"[*] New asset: {subdomain}")
        cursor.execute(
            "INSERT INTO assets (subdomain, ip_address, tech_stack) VALUES (%s, %s, %s)",
            (subdomain, ip_address, tech_stack)
        )
        asset_id = cursor.lastrowid
        cursor.execute(
            "INSERT INTO scan_history (asset_id, change_type, new_value) VALUES (%s, 'INITIAL_DISCOVERY', %s)",
            (asset_id, subdomain)
        )
    else:
        asset_id, old_ip, old_tech = result

        # 2. TRACK IP DRIFT
        if ip_address != old_ip:
            print(f"[!] IP Change: {subdomain} ({old_ip} -> {ip_address})")
            cursor.execute("UPDATE assets SET ip_address = %s, time_stamp = NOW() WHERE id = %s", (ip_address, asset_id))
            cursor.execute(
                "INSERT INTO scan_history (asset_id, change_type, old_value, new_value) VALUES (%s, 'IP_CHANGE', %s, %s)",
                (asset_id, old_ip, ip_address)
            )

        # 3. TRACK TECH STACK DRIFT
        if tech_stack != old_tech:
            print(f"[!] Tech Change: {subdomain} ({old_tech} -> {tech_stack})")
            cursor.execute("UPDATE assets SET tech_stack = %s, time_stamp = NOW() WHERE id = %s", (tech_stack, asset_id))
            cursor.execute(
                "INSERT INTO scan_history (asset_id, change_type, old_value, new_value) VALUES (%s, 'TECH_STACK_CHANGE', %s, %s)",
                (asset_id, old_tech, tech_stack)
            )

    conn.commit()
    cursor.close()
    conn.close()