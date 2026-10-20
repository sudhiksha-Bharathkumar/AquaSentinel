import os
import random
from flask import Flask, render_template, request, jsonify
from sklearn.ensemble import IsolationForest

base_dir = os.path.abspath(os.path.dirname(__file__))
templates_dir = os.path.join(base_dir, 'templates')

app = Flask(__name__, template_folder=templates_dir)

# Initialize Synthetic Ward Database
random.seed(42)
wards = []
for i in range(1, 61):
    wards.append({
        "id": f"Ward {i}",
        "lat": 12.88 + random.uniform(0, 0.07),
        "lon": 79.10 + random.uniform(0, 0.07),
        "population": random.randint(5000, 15000),
        "supply_days": random.randint(1, 4),
        "septic_pct": random.uniform(0.3, 0.9)
    })

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/simulate', methods=['POST'])
def simulate():
    data = request.json or {}
    rain = data.get('rainfall', 10)
    pipe_up = data.get('pipe_upgrade', 0)
    sewer_up = data.get('sewer_upgrade', 0)
    available_kits = data.get('test_kits', 20)
    available_tankers = data.get('tankers', 5)

    initial_kits = available_kits
    initial_tankers = available_tankers

    processed_wards = []
    feature_matrix = []

    # 1. Compute Infrastructure Vulnerability & Ingress Risk
    for w in wards:
        sim_septic = w["septic_pct"] * (1 - (sewer_up / 100))
        base_pressure_loss = 1 - (w["supply_days"] / 7)
        sim_pressure_loss = base_pressure_loss * (1 - (pipe_up / 100))

        rain_penalty = (rain / 100) * sim_septic
        base_risk = sim_pressure_loss * sim_septic * (w["population"] / 15000)
        risk_score = min(max(base_risk + rain_penalty, 0.0), 1.0)

        feature_matrix.append([risk_score, sim_septic, sim_pressure_loss])

        processed_wards.append({
            "id": w["id"],
            "lat": w["lat"],
            "lon": w["lon"],
            "population": w["population"],
            "supply_days": w["supply_days"],
            "risk_score": risk_score,
            "sim_septic": sim_septic,
            "sim_pressure_loss": sim_pressure_loss,
            "kit_assigned": False,
            "tanker_assigned": False
        })

    # 2. Scikit-Learn IsolationForest Machine Learning Audit ("Truth Tap")
    iso = IsolationForest(contamination=0.1, random_state=42)
    anomalies = iso.fit_predict(feature_matrix)

    for idx, w in enumerate(processed_wards):
        w["confidence"] = "Low (Test First)" if anomalies[idx] == -1 else "High"

    # 3. Greedy Knapsack Optimization for Resource Triage
    processed_wards.sort(key=lambda x: (x["confidence"] == "Low (Test First)", x["risk_score"]), reverse=True)

    red_count = 0
    amber_count = 0
    green_count = 0

    for w in processed_wards:
        if w["risk_score"] > 0.6:
            red_count += 1
        elif w["risk_score"] > 0.3:
            amber_count += 1
        else:
            green_count += 1

        if (w["confidence"] == "Low (Test First)" or w["sim_septic"] > 0.6) and available_kits > 0:
            w["kit_assigned"] = True
            available_kits -= 1

        if w["risk_score"] > 0.6 and available_tankers > 0:
            w["tanker_assigned"] = True
            available_tankers -= 1

    # 4. Automated Public Health & Executive Advisories
    advisories = []
    if rain > 50:
        advisories.append("🌧️ Heavy Rain Warning: Surface run-off intrusion risk elevated. Instruct citizens to flush taps for 3 mins.")
    if red_count > 12:
        advisories.append("⚠️ Contamination Spike: Critical risk in multiple wards. Issued priority boil-water directive.")
    if available_kits == 0:
        advisories.append("🚨 Inventory Exhaustion: Field test kits depleted. Requesting urgent emergency restocking from district lab.")

    return jsonify({
        "wards": processed_wards,
        "summary": {
            "red_wards": red_count,
            "amber_wards": amber_count,
            "green_wards": green_count,
            "kits_deployed": initial_kits - available_kits,
            "tankers_deployed": initial_tankers - available_tankers,
            "unused_kits": available_kits,
            "unused_tankers": available_tankers,
            "avg_risk": round(sum(w["risk_score"] for w in processed_wards) / len(processed_wards), 2)
        },
        "advisories": advisories
    })

if __name__ == '__main__':
    app.run(debug=True)