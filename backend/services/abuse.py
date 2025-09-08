import os, requests

ABUSE_KEY = os.getenv("ABUSEIPDB_API_KEY", "").strip()

def abuse_check(ip: str):
    if not ABUSE_KEY:
        return None
    url = "https://api.abuseipdb.com/api/v2/check"
    headers = {"Key": ABUSE_KEY, "Accept": "application/json"}
    params = {"ipAddress": ip, "maxAgeInDays": 90}
    try:
        r = requests.get(url, headers=headers, params=params, timeout=15)
        if r.status_code != 200:
            return {"error": f"status {r.status_code}"}
        data = r.json().get("data", {})
        return {
            "abuseConfidenceScore": data.get("abuseConfidenceScore", 0),
            "raw": data
        }
    except requests.RequestException as e:
        return {"error": str(e)}
