import subprocess
import os
import resolver 

#  CONFIGURATION 
DOMAIN = "redasmsecurity.cloud"
WORDLIST = r"C:\Tools\wordlists\top1million.txt"

def run_cmd(step_name, command):
    print(f"\n[*] STEP: {step_name}")
    try:
        subprocess.run(command, shell=True, check=True)
    except subprocess.CalledProcessError as e:
        print(f"[!] Error in {step_name}: {e}")

def main():
    print(f"=== RedASM Full Discovery Scanner: {DOMAIN} ===")

    # 1. PASSIVE DISCOVERY PHASE
    # Creates the discovery.txt file
    run_cmd("Subfinder Discovery", f"subfinder -d {DOMAIN} -silent > discovery.txt")
    # Appends (>>) to the discovery.txt file
    run_cmd("Amass Passive Scan", f"amass enum -passive -d {DOMAIN} -silent >> discovery.txt")

    # 2. VERIFICATION PHASE
    # Filter the discovery.txt to see what's actually live
    print("[*] Filtering passive results for active hosts...")
    run_cmd("DNS Verification", "dnsx -l discovery.txt -silent -o verified_discovery.txt")

    # 3. ACTIVE BRUTE FORCE PHASE
    # Now hunt for the stuff that wasn't in the passive records
    print("[*] Running 110k Brute Force hunt...")
    run_cmd("DNS Brute-Force", f"dnsx -d {DOMAIN} -w {WORDLIST} -t 100 -silent -o brute_results.txt")

    # 4. MERGE & DEDUPLICATE
    # Combine everything into one unique list for the resolver
    print("[*] Merging all unique findings...")
    merge_cmd = "type verified_discovery.txt brute_results.txt | sort /unique > final_targets.txt"
    run_cmd("Merging Files", merge_cmd)

    # 5. TECH PROBE PHASE
    if not os.path.exists("final_targets.txt"):
        print("[!] No assets found.")
        return

    with open("final_targets.txt", "r") as f:
        targets = [line.strip() for line in f if line.strip()]

    print(f"[*] Probing {len(targets)} unique assets for Tech Stacks...")
    final_data = resolver.resolve_details(targets)

    # 6. DISPLAY RESULTS (Dry Run Mode)
    print("\n" + "="*70)
    print(f"{'SUBDOMAIN':<35} | {'IP ADDRESS':<15} | {'TECH'}")
    print("-"*70)
    for asset in final_data:
        print(f"{asset['subdomain']:<35} | {asset['ip']:<15} | {asset['tech']}")
    print("="*70)

if __name__ == "__main__":
    main()