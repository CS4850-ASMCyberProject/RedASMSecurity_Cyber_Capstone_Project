import socket
import requests
from concurrent.futures import ThreadPoolExecutor

def fetch_metadata(target):
    data = {
        'subdomain': target,
        'ip': '0.0.0.0',
        'tech': 'Unknown',
    }
    try:
        # 1. Get IP
        data['ip'] = socket.gethostbyname(target)
        
        # 2. Get Tech (Server Header)
        url = f"http://{target}"
        # Timeout is key so one slow site doesn't break the scanner
        req = requests.get(url, timeout=3, allow_redirects=True)        
        data['tech'] = req.headers.get('Server', 'Unknown')
    except Exception:
        pass # Keep defaults if site is unreachable
    return data

def resolve_details(subdomain_list):
    # Workers set to 20 for speed
    with ThreadPoolExecutor(max_workers=20) as pool:
        results = list(pool.map(fetch_metadata, subdomain_list))
    return results