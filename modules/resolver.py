import socket
import requests
from concurrent.futures import ThreadPoolExecutor
import re

def fetch_metadata(target):
    # Data structure for our results
    data = {
        'subdomain': target,
        'ip': '0.0.0.0',
        'tech': 'N/A',
        'title': 'N/A',
        'status': 0
    }

    try:
        # Resolve the IP address
        data['ip'] = socket.gethostbyname(target)
        
        url = f"http://{target}"
        req = requests.get(url, timeout=5, allow_redirects=True)        
        data['status'] = req.status_code
        data['tech'] = req.headers.get('Server', 'Unknown')
        
        # Grab the page title with regex
        find_title = re.search('<title>(.*?)</title>', req.text, re.IGNORECASE)
        if find_title:
            data['title'] = find_title.group(1).strip()
            
    except Exception:
        # If site is down or DNS fails, we keep the defaults
        pass
        
    return data

# Use threading to handle multiple sites at once so it's not slow with larger data sets
def resolve_details(subdomain_list, workers=10): 
    with ThreadPoolExecutor(max_workers=workers) as pool:
        final_results = list(pool.map(fetch_metadata, subdomain_list))

    return final_results
