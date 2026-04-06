import mysql.connector
from datetime import datetime

#DB_Handler Creates a connection to the MySQL database and updates the database

# --- VM CONNECTION CONFIG ---
DB_HOST = "127.0.0.1"
DB_PORT = 3307
DB_USER = "asm_user"
DB_PASS = "073334K" # Set this on the VM
DB_NAME = "asm_database"

def get_connection():
    try:
        return mysql.connector.connect(
            host=DB_HOST,
            port=DB_PORT,
            user=DB_USER,
            password=DB_PASS,
            database=DB_NAME
        )
    except Exception as e:
        print(f"[!] DB Connection Failed: {e}")
        return None

def upsert_asset(subdomain, ip_address, title, status_code, webserver, tech_stack, port, cdn, url):
    conn = get_connection()
    if not conn: 
        return
    
    cursor = conn.cursor()

    # 1. Check if we've seen this subdomain
    cursor.execute("SELECT id, ip_address, title, status_code, webserver, tech_stack, port, cdn, url FROM assets WHERE subdomain = %s", (subdomain,))
    result = cursor.fetchone()

    if not result:
        # BRAND NEW DISCOVERY
        print(f"[*] New asset: {subdomain}")
        cursor.execute(
            "INSERT INTO assets (subdomain, ip_address, title, status_code, webserver, tech_stack, port, cdn, url) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)",
            (subdomain, ip_address, title, status_code, webserver, tech_stack, port, cdn, url)
        )
        asset_id = cursor.lastrowid
        cursor.execute(
            "INSERT INTO assets_scan_history (asset_id, change_type, new_value) VALUES (%s, 'INITIAL_DISCOVERY', %s)",
            (asset_id, subdomain)
        )
    else:
        asset_id, old_ip_address, old_title, old_status_code, old_webserver, old_tech_stack, old_port, old_cdn, old_url = result

        # 2. TRACK IP DRIFT
        if ip_address != old_ip_address:
            print(f"[!] IP Change: {subdomain} ({old_ip_address} -> {ip_address})")
            cursor.execute("UPDATE assets SET ip_address = %s WHERE id = %s", (ip_address, asset_id))
            cursor.execute(
                "INSERT INTO assets_scan_history (asset_id, change_type, old_value, new_value) VALUES (%s, 'IP_CHANGE', %s, %s)",
                (asset_id, old_ip_address, ip_address)
            )

        # 3. TRACK TITLE DRIFT
        if title != old_title:
            print(f"[!] Title Change: {subdomain} ({old_title} -> {title})")
            cursor.execute("UPDATE assets SET title = %s WHERE id = %s", (title, asset_id))
            cursor.execute(
                "INSERT INTO assets_scan_history (asset_id, change_type, old_value, new_value) VALUES (%s, 'TITLE_CHANGE', %s, %s)",
                (asset_id, old_title, title)
            )
            
        # 4. TRACK STATUS CODE DRIFT
        if status_code != old_status_code:
            print(f"[!] Status Code Change: {subdomain} ({old_status_code} -> {status_code})")
            cursor.execute("UPDATE assets SET status_code = %s WHERE id = %s", (status_code, asset_id))
            cursor.execute(
                "INSERT INTO assets_scan_history (asset_id, change_type, old_value, new_value) VALUES (%s, 'STATUS_CODE_CHANGE', %s, %s)",
                (asset_id, str(old_status_code), str(status_code))
            )
            
        # 5. TRACK WEBSERVER DRIFT
        if webserver != old_webserver:
            print(f"[!] Webserver Change: {subdomain} ({old_webserver} -> {webserver})")
            cursor.execute("UPDATE assets SET webserver = %s WHERE id = %s", (webserver, asset_id))
            cursor.execute(
                "INSERT INTO assets_scan_history (asset_id, change_type, old_value, new_value) VALUES (%s, 'WEBSERVER_CHANGE', %s, %s)",
                (asset_id, old_webserver, webserver)
            )
            
        # 6. TRACK TECH STACK DRIFT
        if tech_stack != old_tech_stack:
            print(f"[!] Tech Change: {subdomain} ({old_tech_stack} -> {tech_stack})")
            cursor.execute("UPDATE assets SET tech_stack = %s WHERE id = %s", (tech_stack, asset_id))
            cursor.execute(
                "INSERT INTO assets_scan_history (asset_id, change_type, old_value, new_value) VALUES (%s, 'TECH_STACK_CHANGE', %s, %s)",
                (asset_id, old_tech_stack, tech_stack)
            )
            
        # 7. TRACK PORT DRIFT
        if port != old_port:
            print(f"[!] Port Change: {subdomain} ({old_port} -> {port})")
            cursor.execute("UPDATE assets SET port = %s WHERE id = %s", (port, asset_id))
            cursor.execute(
                "INSERT INTO assets_scan_history (asset_id, change_type, old_value, new_value) VALUES (%s, 'PORT_CHANGE', %s, %s)",
                (asset_id, str(old_port), str(port))
            )
            
        # 8. TRACK CDN DRIFT
        if cdn != old_cdn:
            print(f"[!] CDN Change: {subdomain} ({old_cdn} -> {cdn})")
            cursor.execute("UPDATE assets SET cdn = %s WHERE id = %s", (cdn, asset_id))
            cursor.execute(
                "INSERT INTO assets_scan_history (asset_id, change_type, old_value, new_value) VALUES (%s, 'CDN_CHANGE', %s, %s)",
                (asset_id, old_cdn, cdn)
            )
            
        # 9. TRACK URL DRIFT
        if url != old_url:
            print(f"[!] URL Change: {subdomain} ({old_url} -> {url})")
            cursor.execute("UPDATE assets SET url = %s WHERE id = %s", (url, asset_id))
            cursor.execute(
                "INSERT INTO assets_scan_history (asset_id, change_type, old_value, new_value) VALUES (%s, 'URL_CHANGE', %s, %s)",
                (asset_id, old_url, url)
            )

    conn.commit()
    cursor.close()
    conn.close()
    
def upsert_vulnerability(subdomain, vulnerability_id, type, severity, matched_at, extracted_results, vulnerability_score):
    conn = get_connection()
    if not conn: return
    
    cursor = conn.cursor()
    
    cursor.execute("SELECT id FROM assets WHERE subdomain = %s", (subdomain,))
    asset = cursor.fetchone()
    if not asset:
        cursor.close()
        conn.close()
        return
    
    asset_id = asset[0]
    
    cursor.execute("SELECT asset_id, vulnerability_id, type, severity, matched_at, extracted_results, vulnerability_score FROM vulnerabilities WHERE asset_id = %s and vulnerability_id = %s", 
                   (asset_id, vulnerability_id))
    result = cursor.fetchone()
    
    if not result:
        print(f"[*] New Vulnerability: {vulnerability_id}")
        cursor.execute(
            "INSERT INTO vulnerabilities (asset_id, vulnerability_id, type, severity, matched_at, extracted_results, vulnerability_score) VALUES (%s, %s, %s, %s, %s, %s, %s)", 
            (asset_id, vulnerability_id, type, severity, matched_at, extracted_results, vulnerability_score)
        )
        cursor.execute(
            "INSERT INTO vulnerabilities_scan_history (asset_id, vulnerability_id, change_type, new_value) VALUES (%s, %s, 'INITIAL_DISCOVERY', %s)", 
            (asset_id, vulnerability_id, vulnerability_id)
        )
    else:
        asset_id, old_vulnerability_id, old_type, old_severity, old_matched_at, old_extracted_results, old_vulnerability_score = result
        
        # 2. TRACK Vulnerability_Id DRIFT
        if vulnerability_id != old_vulnerability_id:
            print(f"[!] Vulnerability_Id Change: {subdomain} ({old_vulnerability_id} -> {vulnerability_id})")
            cursor.execute("UPDATE vulnerabilities SET vulnerability_id = %s WHERE asset_id = %s and vulnerability_id = %s", (vulnerability_id, asset_id, old_vulnerability_id))
            cursor.execute(
                "INSERT INTO vulnerabilities_scan_history (asset_id, vulnerability_id, change_type, old_value, new_value) VALUES (%s, %s, 'Vulnerability_CHANGE', %s, %s)",
                (asset_id, vulnerability_id, old_vulnerability_id, vulnerability_id)
            )
            
        # 3. TRACK type DRIFT
        if type != old_type:
            print(f"[!] type: {subdomain} ({old_type} -> {type})")
            cursor.execute("UPDATE vulnerabilities SET type = %s WHERE asset_id = %s and vulnerability_id = %s", (type, asset_id, vulnerability_id))
            cursor.execute(
                "INSERT INTO vulnerabilities_scan_history (asset_id, vulnerability_id, change_type, old_value, new_value) VALUES (%s, %s, 'type_CHANGE', %s, %s)",
                (asset_id, vulnerability_id, old_type, type)
            )
            
        # 4. TRACK Severity DRIFT
        if severity != old_severity:
            print(f"[!] Severity Change: {subdomain} ({old_severity} -> {severity})")
            cursor.execute("UPDATE vulnerabilities SET severity = %s WHERE asset_id = %s and vulnerability_id = %s", (severity, asset_id, vulnerability_id))
            cursor.execute(
                "INSERT INTO vulnerabilities_scan_history (asset_id, vulnerability_id, change_type, old_value, new_value) VALUES (%s, %s, 'Severity_CHANGE', %s, %s)",
                (asset_id, vulnerability_id, old_severity, severity)
            )
            
        # 5. TRACK Matched-At DRIFT
        if matched_at != old_matched_at:
            print(f"[!] Matched-At Change: {subdomain} ({old_matched_at} -> {matched_at})")
            cursor.execute("UPDATE vulnerabilities SET matched_at = %s WHERE asset_id = %s and vulnerability_id = %s", (matched_at, asset_id, vulnerability_id))
            cursor.execute(
                "INSERT INTO vulnerabilities_scan_history (asset_id, vulnerability_id, change_type, old_value, new_value) VALUES (%s, %s, 'Matched_At_CHANGE', %s, %s)",
                (asset_id, vulnerability_id, old_matched_at, matched_at)
            )
            
        # 6. TRACK Extracted Results DRIFT
        if extracted_results != old_extracted_results:
            print(f"[!] Extracted Results Change: {subdomain} ({old_extracted_results} -> {extracted_results})")
            cursor.execute("UPDATE vulnerabilities SET extracted_results = %s WHERE asset_id = %s and vulnerability_id = %s", (extracted_results, asset_id, vulnerability_id))
            cursor.execute(
                "INSERT INTO vulnerabilities_scan_history (asset_id, vulnerability_id, change_type, old_value, new_value) VALUES (%s, %s, 'Extracted_Results_CHANGE', %s, %s)",
                (asset_id, vulnerability_id, old_extracted_results, extracted_results)
            )
            
        # 7. TRACK Vulnerability Score DRIFT
        if vulnerability_score != old_vulnerability_score:
            print(f"[!] Vulnerability Score Change: {subdomain} ({old_vulnerability_score} -> {vulnerability_score})")
            cursor.execute("UPDATE vulnerabilities SET vulnerability_score = %s WHERE asset_id = %s and vulnerability_id = %s", (vulnerability_score, asset_id, vulnerability_id))
            cursor.execute(
                "INSERT INTO vulnerabilities_scan_history (asset_id, vulnerability_id, change_type, old_value, new_value) VALUES (%s, %s, 'Vulnerability_Score_CHANGE', %s, %s)",
                (asset_id, vulnerability_id, old_vulnerability_score, vulnerability_score)
            )
        
    conn.commit()
    cursor.close()
    conn.close()
    
def upsert_url_paths(subdomain, url_path, status, size, words, line_count, duration):
    conn = get_connection()
    if not conn:
        return
    
    cursor = conn.cursor()
    
    cursor.execute("SELECT id FROM assets WHERE subdomain = %s", (subdomain,))
    asset = cursor.fetchone()
    if not asset:
        cursor.close()
        conn.close()
        return
    
    asset_id = asset[0]
    
    cursor.execute("SELECT asset_id, url_path, status, size, words, line_count, duration FROM url_paths WHERE asset_id = %s and url_path = %s", 
                   (asset_id, url_path))
    result = cursor.fetchone()
    
    if not result:
        print(f"[*] New URL Path: {url_path}")
        cursor.execute(
            "INSERT INTO url_paths (asset_id, url_path, status, size, words, line_count, duration) VALUES (%s, %s, %s, %s, %s, %s, %s)", 
            (asset_id, url_path, status, size, words, line_count, duration)
        )
        cursor.execute(
            "INSERT INTO url_paths_scan_history (asset_id, url_path, change_type, new_value) VALUES (%s, %s, 'INITIAL_DISCOVERY', %s)", 
            (asset_id, url_path, url_path)
        )
    else:
        asset_id, old_url_path, old_status, old_size, old_words, old_line_count, old_duration = result
        
        # 2. TRACK URL Path DRIFT
        if url_path != old_url_path:
            print(f"[!] URL Path Change: {subdomain} ({old_url_path} -> {url_path})")
            cursor.execute("UPDATE url_paths SET url_path = %s WHERE asset_id = %s and url_path = %s", (url_path, asset_id, old_url_path))
            cursor.execute(
                "INSERT INTO url_paths_scan_history (asset_id, url_path, change_type, old_value, new_value) VALUES (%s, %s, 'Vulnerability_CHANGE', %s, %s)",
                (asset_id, url_path, old_url_path, url_path)
            )
            
        # 3. TRACK Status DRIFT
        if status != old_status:
            print(f"[!] Status Change: {subdomain} ({old_status} -> {status})")
            cursor.execute("UPDATE url_paths SET status = %s WHERE asset_id = %s and url_path = %s", (status, asset_id, url_path))
            cursor.execute(
                "INSERT INTO url_paths_scan_history (asset_id, url_path, change_type, old_value, new_value) VALUES (%s, %s, 'type_CHANGE', %s, %s)",
                (asset_id, url_path, old_status, status)
            )
            
        # 4. TRACK Size DRIFT
        if size != old_size:
            print(f"[!] Size Change: {subdomain} ({old_size} -> {size})")
            cursor.execute("UPDATE url_paths SET size = %s WHERE asset_id = %s and url_path = %s", (size, asset_id, url_path))
            cursor.execute(
                "INSERT INTO url_paths_scan_history (asset_id, url_path, change_type, old_value, new_value) VALUES (%s, %s, 'Severity_CHANGE', %s, %s)",
                (asset_id, url_path, old_size, size)
            )
            
        # 5. TRACK Words DRIFT
        if words != old_words:
            print(f"[!] Words Change: {subdomain} ({old_words} -> {words})")
            cursor.execute("UPDATE url_paths SET words = %s WHERE asset_id = %s and url_path = %s", (words, asset_id, url_path))
            cursor.execute(
                "INSERT INTO url_paths_scan_history (asset_id, url_path, change_type, old_value, new_value) VALUES (%s, %s, 'Severity_CHANGE', %s, %s)",
                (asset_id, url_path, old_words, words)
            )
            
        # 6. TRACK line_count DRIFT
        if line_count != old_line_count:
            print(f"[!] Line Count Change: {subdomain} ({old_line_count} -> {line_count})")
            cursor.execute("UPDATE url_paths SET line_count = %s WHERE asset_id = %s and url_path = %s", (line_count, asset_id, url_path))
            cursor.execute(
                "INSERT INTO url_paths_scan_history (asset_id, url_path, change_type, old_value, new_value) VALUES (%s, %s, 'Severity_CHANGE', %s, %s)",
                (asset_id, url_path, old_line_count, line_count)
            )
            
        # 7. TRACK Vulnerability Score DRIFT
        if duration != old_duration:
            print(f"[!] Vulnerability Score Change: {subdomain} ({old_duration} -> {duration})")
            cursor.execute("UPDATE url_paths SET duration = %s WHERE asset_id = %s and url_path = %s", (duration, asset_id, url_path))
        
    conn.commit()
    cursor.close()
    conn.close()
    
def delsert_juice_shop_paths(subdomain, confirmed_paths):
    conn = get_connection()
    if not conn:
        return
    
    cursor = conn.cursor()
    
    cursor.execute("SELECT id FROM assets WHERE subdomain = %s", (subdomain,))
    asset = cursor.fetchone()
    if not asset:
        cursor.close()
        conn.close()
        return
    
    asset_id = asset[0]
    
    cursor.execute("SELECT url_path FROM juice_shop_paths WHERE asset_id = %s", (asset_id,))
    database_paths = {row[0] for row in cursor.fetchall()}
    
    confirmed_paths = set(confirmed_paths)
    
    new_paths = confirmed_paths - database_paths
    removed_paths = database_paths - confirmed_paths
    
    for path in new_paths:
        print(f"[*] New Juice Shop Path: {path}")
        cursor.execute(
            "INSERT INTO juice_shop_paths (asset_id, url_path) VALUES (%s, %s)", 
            (asset_id, path)
        )
    
    # 2. TRACK Juice Shop URL Path DRIFT
    for path in removed_paths:
        print(f"[!] Removing Juice Shop Path: {path}")
        cursor.execute("DELETE FROM juice_shop_paths WHERE asset_id = %s and url_path = %s", (asset_id, path))
        
    conn.commit()
    cursor.close()
    conn.close()
