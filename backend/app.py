from flask import Flask, request, jsonify
from flask_cors import CORS
from utils.db import init_db, fetch_recent, insert_lookup, get_counts
from services.vt import vt_search
from services.abuse import abuse_check
import ipaddress

app = Flask(__name__)
CORS(app)

DB_PATH = "data/cti.db"
init_db(DB_PATH)

@app.get("/api/dashboard")
def dashboard():
    counts = get_counts(DB_PATH)
    return jsonify(counts)

@app.get("/api/recent")
def recent():
    try:
        limit = int(request.args.get("limit", "20"))
    except ValueError:
        limit = 20
    rows = fetch_recent(DB_PATH, limit=limit)
    return jsonify(rows)

@app.post("/api/lookup")
def lookup():
    payload = request.get_json(silent=True) or {}
    indicator = (payload.get("indicator") or "").strip()
    if not indicator:
        return jsonify({"error": "indicator is required"}), 400

    vt = vt_search(indicator)

    abuse = None
    try:
        ipaddress.ip_address(indicator)
        abuse = abuse_check(indicator)
        ioc_type = "ip"
    except ValueError:
        ioc_type = "domain_or_hash_or_url"

    vt_mal = (vt.get("stats", {}).get("malicious") or 0) if vt else 0
    vt_total = sum(vt.get("stats", {}).values()) if vt and vt.get("stats") else 0
    abuse_score = (abuse or {}).get("abuseConfidenceScore", 0)

    severity = "low"
    if vt_mal >= 3 or abuse_score >= 50:
        severity = "high"
    elif vt_mal == 1 or 10 <= abuse_score < 50:
        severity = "medium"

    row = {
        "indicator": indicator,
        "type": ioc_type,
        "vt_positives": vt_mal,
        "vt_total": vt_total,
        "abuse_score": abuse_score,
        "severity": severity,
        "vt_raw": vt,
        "abuse_raw": abuse,
    }
    insert_lookup(DB_PATH, row)
    return jsonify(row)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
