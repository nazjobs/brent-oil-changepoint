from flask import Flask, jsonify
from flask_cors import CORS
import pandas as pd
import os

app = Flask(__name__)
CORS(app)  # Allow React to fetch data

# Path to the CSV we generated in the notebook
DATA_PATH = os.path.join(
    os.path.dirname(__file__), "../../data/processed_dashboard_data.csv"
)


@app.route("/api/oil-prices", methods=["GET"])
def get_oil_prices():
    try:
        if not os.path.exists(DATA_PATH):
            return jsonify(
                {"error": "Data file not found. Run notebook 02 first."}
            ), 404

        df = pd.read_csv(DATA_PATH)
        # Convert date to string for JSON serialization
        results = df[["Date", "Price", "Regime", "Regime_Mean"]].to_dict(
            orient="records"
        )
        return jsonify(results)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/stats", methods=["GET"])
def get_stats():
    # Simple endpoint for summary stats
    if not os.path.exists(DATA_PATH):
        return jsonify({}), 404
    df = pd.read_csv(DATA_PATH)
    stats = {
        "start_date": df["Date"].min(),
        "end_date": df["Date"].max(),
        "current_price": df["Price"].iloc[-1],
        "regimes_detected": 3,
    }
    return jsonify(stats)


if __name__ == "__main__":
    app.run(debug=True, port=5000)
