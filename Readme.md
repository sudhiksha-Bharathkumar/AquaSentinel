# 💧 AquaSentinel: NeerGap Vellore

> **A Trust-Aware Water-Safety Early-Warning & Resource Triage Platform for Intermittent Supply Networks**  
> *Pilot Region: Vellore, Tamil Nadu | PySustain-2026 | Track 2: Clean Water & Sanitation (SDG 6)*

---

## 👥 Team & Citation
* **Sudhiksha P B** (26BVD0064)
* **Lakshithaa M** (26BVD0176)
* **Guhan Ravikumar** (26BVD0045)

---

## 📌 Problem Statement & Context

In cities like **Vellore**, municipal piped water is delivered intermittently (sometimes as infrequently as once every 10 days in wards like Ward 46). When piped supply shuts off, pipeline pressure drops below atmospheric level, creating a **negative pressure vacuum**. Where unpressurized, aging pipes cross leaking drains or septic tanks, wastewater and sewage are drawn directly into the drinking water supply.

Furthermore, field screening tools (such as $H_2S$ test vials and low-cost IoT sensors) exhibit high noise and drift (up to 5–8% daily drift). Standard monitoring systems treat every signal with equal weight, leading to false alarms or undetected contamination during infrastructure transition phases.

**AquaSentinel** addresses this by providing a Python-driven decision-support tool that:
1. **Predicts** contamination ingress risks before public health outbreaks occur.
2. **Audits** signal reliability using machine learning to separate *contamination risk* from *data confidence*.
3. **Optimizes** daily municipal triage assets (field test kits, repair crews, and water tankers) via a Greedy Knapsack algorithm.

---

## ✨ Key Innovations & Architecture

```
                       ┌──────────────────────────────┐
                       │   Environmental Context      │
                       │   (Rainfall, Supply Days)    │
                       └──────────────┬───────────────┘
                                      │
                                      ▼
┌──────────────────────┐   ┌──────────────────────────┐   ┌──────────────────────────────┐
│  Truth Tap Layer     ├──►│  Ingress Risk Engine     ├──►│ Greedy Knapsack Optimizer    │
│  (IsolationForest)   │   │  (Baseline Vulnerability)│   │ (Resource Triage Queue)      │
└──────────────────────┘   └──────────────────────────┘   └──────────────┬───────────────┘
                                                                         │
                                                                         ▼
                                                          ┌──────────────────────────────┐
                                                          │   Interactive Dashboard &    │
                                                          │   Public Health Advisories   │
                                                          └──────────────────────────────┘
```

### 1. Ingress Risk Engine
Calculates ward-level vulnerability mathematically based on intermittent supply schedules, exposed population, septic tank reliance, and surface run-off penalties from rainfall:

$$\text{Risk Score} = \min\left(1.0, \left(\text{PressureLossProb} \times \text{SepticReliance} \times \frac{\text{Population}}{15,000}\right) + \text{RainfallPenalty}\right)$$

### 2. "Truth Tap" Confidence Layer
Uses an **Isolation Forest** machine learning algorithm to audit incoming telemetry and survey data for statistical anomalies or sensor drift. Rather than assuming all data is reliable:
* **High Confidence:** Data conforms to expected physical distributions.
* **Low Confidence ("Test First"):** Anomalous reading detected; forces the system to dispatch a field validation test kit before taking heavy action.

### 3. Greedy Knapsack Resource Optimizer
Municipal relief assets are finite. AquaSentinel treats daily triage allocation as a Knapsack Problem, ranking wards by population-weighted risk and evidence uncertainty to allocate available test kits and tanker trucks without wasting resources.

### 4. Interactive "What-If" Infrastructure Simulator
Allows engineers to simulate infrastructure rollouts (such as new AMRUT pipeline extensions or sewerage networks) to observe real-time risk reduction across the 60 municipal wards.

---

## 🛠️ Tech Stack & Dependencies

* **Language:** Python 3.12 / JavaScript (ES6)
* **Backend Framework:** Flask
* **Machine Learning:** `scikit-learn` (`IsolationForest`)
* **Frontend / UI:** Tailwind CSS, Leaflet.js (OpenStreetMap engine)
* **Deployment:** Netlify / Render / Vercel

---

## 📂 Repository Structure

```text
AquaSentinel/
├── index.html          # Netlify-ready single-page application dashboard
├── app.py              # Pure Python Flask application backend
├── requirements.txt    # Python dependencies (Flask, scikit-learn)
├── templates/
│   └── index.html      # Flask Jinja2 frontend template
└── README.md           # Project documentation
```

---

## 🚀 Local Setup & Run Instructions

### Running the Python Flask Backend
1. Clone the repository:
   ```bash
   git clone https://github.com/YOUR_USERNAME/AquaSentinel.git
   cd AquaSentinel
   ```
2. Set up a virtual environment and install dependencies:
   ```bash
   python -m venv .venv
   # On Windows:
   .venv\Scripts\activate
   # On macOS/Linux:
   source .venv/bin/activate

   pip install -r requirements.txt
   ```
3. Run the application:
   ```bash
   python app.py
   ```
4. Open your browser and navigate to `http://127.0.0.1:5000`.

### Running Static Web Version
Simply open `index.html` directly in any standard web browser or deploy directly to Netlify.

---

## 🎯 Alignment with Sustainable Development Goals (SDGs)

* **SDG 6.1:** Safe and affordable drinking water for all.
* **SDG 6.3:** Improving water quality by reducing pollution and eliminating dumping.
* **SDG 11.B:** Enhancing disaster risk management in human settlements.

---

## 📄 References & Research Base
1. Kumpel, E., & Nelson, K. L. (2013). *Comparing water quality in intermittent and continuous supply systems.* Water Research.
2. Kulinkina, A. V., et al. (2016). *Piped water consumption and gastrointestinal disease in Vellore District.* Scientific Reports.
3. Ministry of Jal Shakti (2024). *Functionality Assessment National Report.* Government of India.
