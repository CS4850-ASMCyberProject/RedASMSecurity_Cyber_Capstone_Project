import subprocess
import shutil
from modules.db_handler import upsert_asset

def run_subdomain_scanner(target_domain):
    # Check if subfinder is installed
    if not shutil.which("subfinder"):
        print("Error: subfinder is not installed or not in PATH.")
        return []

    print(f"Running subfinder for {target_domain}...")
    try:
        result = subprocess.run(["subfinder", "-d", target_domain, "-silent"], capture_output=True, text=True, check=True)
        subdomains = result.stdout.splitlines()
        print(f"Found {len(subdomains)} subdomains for {target_domain}.")
        return subdomains
    except subprocess.CalledProcessError as e:
        print(f"Error running subfinder: {e}")
        return []

        #This is not finished yet. Will need to add functionality to resolve the subdomains to IP addresses and identify the tech stack. This is just a starting point for the subdomain scanning module.
        