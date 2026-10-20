from flask import Flask, render_template, request, jsonify
import random

app = Flask(__name__)

# 1. Generate Synthetic Database using pure Python
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
    data = request.json
    rain = data.get('rainfall', 10)
    pipe_up = data.get('pipe_upgrade', 0)
    sewer_up = data.get('sewer_upgrade', 0)
    available_kits = data.get('test_kits', 20)
    available_tankers = data.get('tankers', 5)

    processed_wards = []
    
    # 2. Python Risk Engine & Truth Tap Simulation
    for w in wards:
        sim_septic = w["septic_pct"] * (1 - (sewer_up / 100))
        base_pressure_loss = 1 - (w["supply_days"] / 7)
        sim_pressure_loss = base_pressure_loss * (1 - (pipe_up / 100))

        rain_penalty = (rain / 100) * sim_septic
        base_risk = sim_pressure_loss * sim_septic * (w["population"] / 15000)
        risk_score = min(max(base_risk + rain_penalty, 0.0), 1.0)

        # Truth Tap Anomaly Logic 
        confidence = "High"
        if sim_pressure_loss > 0.8 and sim_septic < 0.2:
            confidence = "Low (Test First)"
        if random.random() > 0.92: # Simulating hardware drift
            confidence = "Low (Test First)"

        processed_wards.append({
            "id": w["id"],
            "lat": w["lat"],
            "lon": w["lon"],
            "risk_score": risk_score,
            "confidence": confidence,
            "sim_septic": sim_septic,
            "kit_assigned": False,
            "tanker_assigned": False
        })

    # 3. Python Greedy Knapsack Optimizer
    # Sort wards by highest risk first
    processed_wards.sort(key=lambda x: x["risk_score"], reverse=True)

    for w in processed_wards:
        if (w["confidence"] == "Low (Test First)" or w["sim_septic"] > 0.6) and available_kits > 0:
            w["kit_assigned"] = True
            available_kits -= 1
            
        if w["risk_score"] > 0.6 and available_tankers > 0:
            w["tanker_assigned"] = True
            available_tankers -= 1

    return jsonify({
        "wards": processed_wards,
        "unused_kits": available_kits,
        "unused_tankers": available_tankers
    })

if __name__ == '__main__':
    app.run(debug=True)