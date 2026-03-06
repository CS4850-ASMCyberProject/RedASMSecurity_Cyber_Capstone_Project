from modules.resolver import resolve_details, save_to_json

TARGET_SITES = [
    'google.com',
    'github.com',
    'wikipedia.org',
    'localhost',
]

print("\n" + "="*70)
print(f"{'SUBDOMAIN':<25} | {'IP ADDRESS':<15} | {'TECHNOLOGY':<15}")
print("="*70)

results = resolve_details(TARGET_SITES)

# String slicing so that the data in the table is always readable
for r in results:
    sub = str(r['subdomain'])[:25]
    ip = str(r['ip']) if r['ip'] else "FAILED"
    tech = str(r['tech'])[:15] 

    print(f"{sub:<25} | {ip:<15} | {tech:<15}")

print("="*70)
print(f"Scan complete. Processed {len(TARGET_SITES)} targets\n")

save_to_json(results)   