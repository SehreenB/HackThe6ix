import requests
import json
import time
from datetime import datetime
import os

BASE_URL = "https://hackthe6ix-production.up.railway.app"
API_KEY = "6LRVZJLO1ID0r2Ec22ZqtAfrbGZNUcS3"
OUTPUT_DIR = "freesolo_data"

os.makedirs(OUTPUT_DIR, exist_ok=True)

training_pairs = []
pair_count = 0

print("Generating Freesolo training data...")
print(f"Using API Key: {API_KEY[:20]}..." if API_KEY else "No API key found!")
print("Target: 75-150 scenario-brief pairs\n")

headers = {
    "X-API-Key": API_KEY,
    "Content-Type": "application/json"
}

for n in range(1, 11):
    for iter in range(1, 9):
        pair_count += 1
        print(f"Generating pair {pair_count}: n={n} (iteration {iter})...")
        
        try:
            opt_response = requests.post(
                f"{BASE_URL}/api/optimize",
                headers=headers,
                json={"n": n},
                timeout=60
            )
            opt_response.raise_for_status()
            opt_data = opt_response.json()
            
            brief_body = {
                "stats": opt_data["updated_stats"],
                "optimizer_results": opt_data["locations"]
            }
            
            brief_response = requests.post(
                f"{BASE_URL}/api/brief",
                headers=headers,
                json=brief_body,
                timeout=60
            )
            brief_response.raise_for_status()
            brief_text = brief_response.text
            
            pair = {
                "input": {
                    "n_facilities": n,
                    "total_pop": opt_data["updated_stats"]["total_pop"],
                    "within_2hr": opt_data["updated_stats"]["within_2hr"],
                    "pct_covered": opt_data["updated_stats"]["pct_covered"]
                },
                "output": brief_text
            }
            
            training_pairs.append(pair)
            print(f"  ✓ Generated brief (total: {pair_count} pairs)\n")
            time.sleep(3)
            
        except Exception as e:
            print(f"  ✗ Error: {e}\n")
            time.sleep(5)

print(f"Generated {len(training_pairs)} total training pairs\n")

output = {
    "metadata": {
        "dataset_name": "Apogee Canada - Surgical Access Policy Briefs",
        "total_pairs": len(training_pairs),
        "generated_date": datetime.now().isoformat()
    },
    "training_data": training_pairs
}

with open(f"{OUTPUT_DIR}/training_data.json", "w") as f:
    json.dump(output, f, indent=2)

print(f"✓ Saved to: {OUTPUT_DIR}/training_data.json")