import os
from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv

from quantum_optimizer import optimize_charging

load_dotenv()

app = Flask(__name__)
APP_NAME = os.getenv("APP_NAME", "Quantum EV Charging Optimizer")
DEMO_MODE = os.getenv("DEMO_MODE", "true").lower() == "true"


@app.get("/")
def index():
    return render_template("index.html", app_name=APP_NAME)


@app.post("/api/optimize")
def optimize():
    data = request.get_json(silent=True) or {}
    try:
        result = optimize_charging(data)
        return jsonify({"success": True, "result": result})
    except ValueError as exc:
        return jsonify({"success": False, "error": str(exc)}), 400
    except Exception:
        app.logger.exception("Optimization failed")
        return jsonify({"success": False, "error": "Optimization failed. Check server logs."}), 500


if __name__ == "__main__":
    port = int(os.getenv("PORT", "5000"))
    app.run(host="0.0.0.0", port=port, debug=DEMO_MODE)
