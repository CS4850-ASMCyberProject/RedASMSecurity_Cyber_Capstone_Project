import subprocess
import os
import resolver 
import db_handler  # This is the bridge to your Cloud VM

# CONFIGURATION 
DOMAIN = "redasmsecurity.cloud"
WORDLIST = r"C:\Tools\wordlists\top1million.txt"

def run_cmd(step_name, command):
    print(f"\n[*] STEP: {step_name}")
    try:
        # We use shell=True because of the 'type' and '|' commands in Windows
        subprocess.run(command, shell=True, check=True)
    except subprocess.CalledProcessError as e:
        print(f"[!] Error in {step_name}: {e}")

def main():
    print(f"=== RedASM Cloud-Linked Discovery Scanner: {DOMAIN} ===")

    # 1. PASSIVE DISCOVERY PHASE
    run_cmd("Subfinder Discovery", f"subfinder -d {DOMAIN} -silent > discovery.txt")
    run_cmd("Amass Passive Scan", f"amass enum -passive -d {DOMAIN} -silent >> discovery.txt")

    # 2. VERIFICATION PHASE
    print("[*] Filtering passive results for active hosts...")
    run_cmd("DNS Verification", "dnsx -l discovery.txt -silent -o verified_discovery.txt")

    # 3. ACTIVE BRUTE FORCE PHASE
    print("[*] Running 110k Brute Force hunt...")
    run_cmd("DNS Brute-Force", f"dnsx -d {DOMAIN} -w {WORDLIST} -t 100 -silent -o brute_results.txt")

    # 4. MERGE & DEDUPLICATE
    print("[*] Merging all unique findings...")
    # 'type' is the Windows version of 'cat'
    merge_cmd = "type verified_discovery.txt brute_results.txt | sort /unique > final_targets.txt"
    run_cmd("Merging Files", merge_cmd)

    # 5. TECH PROBE PHASE
    if not os.path.exists("final_targets.txt"):
        print("[!] No assets found. Check your network or wordlist.")
        return

    with open("final_targets.txt", "r") as f:
        targets = [line.strip() for line in f if line.strip()]

    print(f"[*] Probing {len(targets)} unique assets for Tech Stacks...")
    final_data = resolver.resolve_details(targets)

    # 6. DATABASE SYNC PHASE (The Cloud Link)
    print(f"\n[*] Syncing {len(final_data)} assets to Oracle Cloud VM...")
    
    success_count = 0
    for asset in final_data:
        try:
            # Pushing to the VM via db_handler
            db_handler.upsert_asset(asset['subdomain'], asset['ip'], asset['tech'])
            print(f"    [+] Synced: {asset['subdomain']}")
            success_count += 1
        except Exception as e:
            print(f"    [!] Failed to sync {asset['subdomain']}: {e}")

    print("\n" + "="*70)
    print(f"[SUCCESS] Scan Complete!")
    print(f"Total Assets Found: {len(targets)}")
    print(f"Successfully Synced to Cloud: {success_count}")
    print("="*70)

if __name__ == "__main__":
    main()