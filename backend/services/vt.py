import os, requests

VT_API_KEY = os.getenv("VT_API_KEY", "").strip()

def vt_search(query: str):
    if not VT_API_KEY:
        return None
    url = f"https://www.virustotal.com/api/v3/search?query={query}"
    headers = {"x-apikey": VT_API_KEY}
    try:
        r = requests.get(url, headers=headers, timeout=15)
        if r.status_code != 200:
            return {"error": f"status {r.status_code}"}
        data = r.json()
        try:
            attrs = (data.get("data") or [])[0].get("attributes") or {}
            stats = attrs.get("last_analysis_stats") or {}
        except Exception:
            stats = {}
        return {"raw": data, "stats": stats}
    except requests.RequestException as e:
        return {"error": str(e)}
