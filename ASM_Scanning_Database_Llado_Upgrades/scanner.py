from terminal_run import run_cmd
import os
import resolver 
import db_handler  # This is the bridge to your Cloud VM

# CONFIGURATION 
DOMAIN = "redasmsecurity.cloud"
WORDLIST = r"~/SecLists/Discovery/DNS/subdomains-top1million-5000.txt"

def main():
    print(f"=== RedASM Cloud-Linked Discovery Scanner: {DOMAIN} ===")

    # 1. PASSIVE DISCOVERY PHASE
    run_cmd("Subfinder Discovery", f"subfinder -d {DOMAIN} -silent > discovery.txt")

    # 2. VERIFICATION PHASE
    print("[*] Filtering passive results for active hosts...")
    run_cmd("DNS Verification", "dnsx -l discovery.txt -silent -o verified_discovery.txt")

    # 3. ACTIVE BRUTE FORCE PHASE
    print("[*] Running 110k Brute Force hunt...")
    run_cmd("DNS Brute-Force", f"dnsx -d {DOMAIN} -w {WORDLIST} -t 100 -silent -o brute_results.txt")

    # 4. MERGE & DEDUPLICATE
    print("[*] Merging all unique findings...")
    # 'type' is the Windows version of 'cat'
    merge_cmd = "cat verified_discovery.txt brute_results.txt | tr '[:upper:]' '[:lower:]' | sort -u > final_targets.txt"
    run_cmd("Merging Files", merge_cmd)

    # 5. TECH PROBE PHASE
    if not os.path.exists("final_targets.txt"):
        print("[!] No assets found. Check your network or wordlist.")
        return

    with open("final_targets.txt", "r") as f:
        targets = [line.strip() for line in f if line.strip()]

    print(f"[*] Probing {len(targets)} unique assets for Tech Stacks...")
    final_assets_data, final_vulnerability_data, final_ffuf_data, confirmed_paths = resolver.resolve_details(targets)

    # 6. DATABASE SYNC PHASE (The Cloud Link)
    print(f"\n[*] Syncing {len(final_assets_data)} assets to Oracle Cloud VM...")
    
    asset_count = 0
    for asset in final_assets_data:
        try:
            # Pushing to the VM via db_handler
            db_handler.upsert_asset(asset['subdomain'], asset['ip_address'], asset['title'], asset['status_code'], asset['webserver'], asset['tech_stack'], asset['port'], asset['cdn'], asset['url'])
            print(f"    [+] Synced: {asset['subdomain']}")
            asset_count += 1
        except Exception as e:
            print(f"    [!] Failed to sync {asset['subdomain']}: {e}")
            
    vulnerability_count = {}
    for vulnerability in final_vulnerability_data:
        try:
            # Pushing to the VM via db_handler
            subdomain = vulnerability['subdomain']
            db_handler.upsert_vulnerability(vulnerability['subdomain'], vulnerability['vulnerability_id'], vulnerability['type'], vulnerability['severity'], vulnerability['matched_at'], vulnerability['extracted_results'], vulnerability['vulnerability_score'])
            print(f"    [+] Synced: {vulnerability['vulnerability_id']}")
            if subdomain not in vulnerability_count:
                vulnerability_count['subdomain'] = 0
            vulnerability_count['subdomain'] += 1
        except Exception as e:
            print(f"    [!] Failed to sync {vulnerability['subdomain']}: {e}")
            
    path_count = 0
    for path in final_ffuf_data:
        try:
            # Pushing to the VM via db_handler
            db_handler.upsert_url_paths(path['subdomain'], path['url_path'], path['status'], path['size'], path['words'], path['line_count'], path['duration'])
            print(f"    [+] Synced: {path['url_path']}")
            path_count += 1
        except Exception as e:
            print(f"    [!] Failed to sync {path['url_path']}: {e}")
       
    try:
        # Pushing to the VM via db_handler
        subdomain = "shop.redasmsecurity.cloud"
        db_handler.delsert_juice_shop_paths(subdomain, confirmed_paths)
    except Exception as e:
        print(f"    [!] Failed to sync Juice Shop Paths: {e}")

    print(f"**[SUCCESS] Scan Complete!**")
    print("\n" + "="*70)
    print(f"ASSETS")
    print(f"Total Assets Found: {len(targets)}")
    print(f"Successfully Synced to Database: {asset_count}")
    print("="*70)
    
    total_vulnerabilities = sum(vulnerability_count.values())
    total_subdomains = len(vulnerability_count)
    print("\n" + "="*70)
    print(f"VULNERABILITIES")
    print(f"Vulnerability Count By Subdomain:")
    for subdomain, count in vulnerability_count.items():
        print(f"{subdomain}: {count}")
    print(f"Successfully Synced {total_vulnerabilities} for {total_subdomains} subdomains")
    print("="*70)
    
    print("\n" + "="*70)
    print(f"POSSIBLE PATHS")
    print(f"Total Possible Paths Found: {path_count}")
    print(f"Successfully Synced {path_count} total possible paths to legitimize.")
    print("="*70)
    
    print("\n" + "="*70)
    print(f"EXPLOITABLE PATHS")
    print(f"Total Exploitable Paths Found: {confirmed_paths}")
    print(f"Successfully Synced {confirmed_paths} total exploitable paths.")
    print("="*70)

if _name_ == "_main_":
    main()
