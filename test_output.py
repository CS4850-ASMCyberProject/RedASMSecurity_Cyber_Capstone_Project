from modules.resolver import resolve_details

TARGET_SITES = [
    'google.com',
    'github.com',
    'wikipedia.org',
    'localhost',
]

print("\n" + "="*110)
print(f"{'SUBDOMAIN':<25} | {'IP ADDRESS':<15} | {'TECHNOLOGY':<15} | {'CODE':<5} | {'PAGE TITLE'}")
print("="*110)

results = resolve_details(TARGET_SITES)

# String slicing so that the data in the table is always readable
for r in results:
    sub = str(r['subdomain'])[:25]
    ip = str(r['ip']) if r['ip'] else "FAILED"
    tech = str(r['tech'])[:15]
    status = str(r['status']) if r['status'] else "---"
    title = str(r['title'])[:40]

    print(f"{sub:<25} | {ip:<15} | {tech:<15} | {status:<5} | {title}")

print("="*110)
print(f"Scan complete. Processed {len(TARGET_SITES)} targets\n")
