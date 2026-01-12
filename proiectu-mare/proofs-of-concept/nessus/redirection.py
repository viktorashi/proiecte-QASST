import requests
import sys


def verify_cleartext_submission(target_url):
    print(f"[*] Testing target: {target_url}")

    payload = {
        "username": "admin",
        "password": "SuperSecretPassword",
        "login": "true",
    }

    if target_url.startswith("https://"):
        print("[-] Target is using HTTPS. Vulnerability may not exist.")
        return

    try:
        response = requests.post(target_url, data=payload, allow_redirects=False)

        print(f"[*] Request sent to: {response.url}")
        print(f"[*] Response Status Code: {response.status_code}")

        if "http://" in response.url and response.status_code != 301:
            print("[!] VULNERABILITY CONFIRMED: Credentials sent over cleartext HTTP.")
            print("[!] Data exposed on the wire:")
            print(f"    {payload}")
        elif response.status_code in [301, 302] and "https" in response.headers.get(
            "Location", ""
        ):
            print("[-] Server redirects to HTTPS. Mitigated.")
        else:
            print("[?] Inconclusive response.")

    except Exception as e:
        print(f"[!] Error executing exploit test: {e}")


if __name__ == "__main__":
    TARGET = "http://www.vulnbank.org/login"
    verify_cleartext_submission(TARGET)
