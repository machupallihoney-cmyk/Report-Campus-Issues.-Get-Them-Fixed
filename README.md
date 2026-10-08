# Quantum EV Charging Optimizer

A professional Flask demo that demonstrates a real-time style EV charging
optimization workflow using a quantum-compatible optimization layer.

## Features

- Flask REST API
- Responsive dashboard
- Manual EV input
- Automatic sample data
- Charging capacity constraint
- Quantum-ready Qiskit integration point
- Deterministic exact fallback for small demo instances
- Environment configuration with `.env`
- Production-friendly Gunicorn entry point

## Project structure

```text
quantum_ev_charging_optimizer/
├── app.py
├── quantum_optimizer.py
├── requirements.txt
├── .env
├── .env.example
├── .gitignore
├── README.md
├── templates/
│   └── index.html
└── static/
    ├── app.js
    └── style.css
```

## Run locally

### 1. Create a virtual environment

Windows:

```bash
python -m venv .venv
.venv\Scripts\activate
```

Linux/macOS:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Start the Flask server

```bash
python app.py
```

Open:

```text
http://127.0.0.1:5000
```

## API

`POST /api/optimize`

Example payload:

```json
{
  "station_capacity": 2,
  "vehicles": [
    {"id": "EV-01", "battery": 28, "target": 80, "priority": 5},
    {"id": "EV-02", "battery": 55, "target": 90, "priority": 3},
    {"id": "EV-03", "battery": 20, "target": 70, "priority": 4}
  ]
}
```

## Important note

This is an educational prototype. The included small-instance solver is
deterministic so the project works out of the box. It exposes a clean
quantum integration point where a genuine QAOA circuit, simulator, or
supported quantum hardware backend can be connected later.

Never commit real API tokens or credentials to Git.
