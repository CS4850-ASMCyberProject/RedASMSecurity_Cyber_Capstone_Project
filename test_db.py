from db_handler import initialize_db, upsert_asset

# 1. Setup the database
print("--- Step 1: Initializing Database ---")
initialize_db()

# 2. Simulate finding a NEW asset
print("\n--- Step 2: Simulating New Discovery ---")
upsert_asset("dev.redasm.com", "1.1.1.1", "Nginx")

# 3. Simulate finding the SAME asset (No change)
print("\n--- Step 3: Simulating Same Asset (Should do nothing) ---")
upsert_asset("dev.redasm.com", "1.1.1.1", "Nginx")

# 4. Simulate IP DRIFT
print("\n--- Step 4: Simulating IP Drift ---")
upsert_asset("dev.redasm.com", "2.2.2.2", "Nginx")

# 5. Simulate TECH DRIFT
print("\n--- Step 5: Simulating Tech Drift ---")
upsert_asset("dev.redasm.com", "2.2.2.2", "Apache")