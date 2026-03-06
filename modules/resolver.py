import socket
import requests
from concurrent.futures import ThreadPoolExecutor
import re
import json
import os
from datetime import datetime

def load_settings():
    if os.path.exists('config.json'):
        with open('config.json', 'r') as f:
            return json.load(f)
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

def save_to_json(final_results):
    if not os.path.exists('data'):
        os.makedirs('data')

    # Create filename variation based on current timne stamp
    current_time = datetime.now().strftime("%Y%m%d_%H%M%S")
    current_path = f"data/scan_results_{current_time}.json"

    with open(path, 'w') as f:
        json.dump(final_results, f, indent=4)

    print(f"[+] Scanned results were saved to: {current_path}")