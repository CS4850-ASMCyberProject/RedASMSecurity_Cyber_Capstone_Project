import socket
import requests
from concurrent.futures import ThreadPoolExecutor
import os
from datetime import datetime

def load_settings():
   return {"max_workers": 3, "timeout": 5}


def fetch_metadata(target):
    settings = load_settings()
    # Data structure for our results
    data = {
        'subdomain': target,
        'ip': '0.0.0.0',
        'tech': 'N/A',
    }

    try:
        data['ip'] = socket.gethostbyname(target)
        url = f"http://{target}"
        req = requests.get(url, timeout=5, allow_redirects=True)        
        data['tech'] = req.headers.get('Server', 'Unknown')
            
    except Exception:
        # If site is down or DNS fails, we keep the defaults
        pass
        
    return data

# Use threading to handle multiple sites at once so it's not slow with larger data sets
def resolve_details(subdomain_list):
    settings = load_settings()
    workers = settings.get('max_workers', 3) 
    with ThreadPoolExecutor(max_workers=workers) as pool:
        final_results = list(pool.map(fetch_metadata, subdomain_list))

    return final_results