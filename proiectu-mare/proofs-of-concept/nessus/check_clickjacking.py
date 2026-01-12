import requests


def check_clickjacking_headers(url):
    print(f"[*] Analyzing headers for: {url}")
    print("-" * 60)

    try:
        response = requests.get(url, timeout=10)
        headers = response.headers

        xfo = headers.get("X-Frame-Options", None)

        if xfo:
            print(f"[+] X-Frame-Options header found: {xfo}")
            if xfo.upper() in ["DENY", "SAMEORIGIN"]:
                print("    -> Status: SECURE (TC-CJ-01 Passed)")
            else:
                print(
                    "    -> Status: WEAK (Header present but value might be insufficient)"
                )
        else:
            print("[-] X-Frame-Options header MISSING")
            print("    -> Status: VULNERABLE (TC-CJ-01 Failed)")

        print("-" * 60)

        csp = headers.get("Content-Security-Policy", None)

        if csp:
            print(f"[+] Content-Security-Policy header found.")

            if "frame-ancestors" in csp:
                print(f"    -> Directive 'frame-ancestors' found: {csp}")
                print("    -> Status: SECURE (TC-CJ-02 Passed)")
            else:
                print("    -> 'frame-ancestors' directive MISSING in CSP.")
                print("    -> Status: POTENTIALLY VULNERABLE (TC-CJ-02 Failed)")
        else:
            print("[-] Content-Security-Policy header MISSING")
            print("    -> Status: VULNERABLE (TC-CJ-02 Failed)")

        print("-" * 60)

        if not xfo and (not csp or "frame-ancestors" not in csp):
            print("[!] CRITICAL: No clickjacking protections detected.")
            print("    The site is likely vulnerable to UI Redress Attacks.")
        elif xfo or (csp and "frame-ancestors" in csp):
            print("[*] PASS: At least one protection mechanism is in place.")

    except requests.exceptions.RequestException as e:
        print(f"[!] Error connecting to target: {e}")


if __name__ == "__main__":
    TARGET_URL = "http://www.vulnbank.org"
    check_clickjacking_headers(TARGET_URL)
