from flask import Flask, render_template, request
import pandas as pd
import joblib
import json
import os
from datetime import datetime

app = Flask(__name__)

# Load model & preprocessing objects
data = joblib.load("model.pkl")
model = data["model"]
encoders = data["encoders"]
features = data["features"]
importance = data["importance"]

# Storage file path
STORAGE_FILE = "storage/predictions.csv"
os.makedirs("storage", exist_ok=True)  # Ensure folder exists

@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        # Collect form input
        employee_data = {
            "Age": int(request.form["Age"]),
            "MonthlyIncome": int(request.form["MonthlyIncome"]),
            "JobRole": request.form["JobRole"],
            "OverTime": request.form["OverTime"],
            "DistanceFromHome": int(request.form["DistanceFromHome"]),
            "JobSatisfaction": max(1, min(5, int(request.form["JobSatisfaction"]))),  # 1–5
            "WorkLifeBalance": max(1, min(5, int(request.form["WorkLifeBalance"]))),  # 1–5
            "TotalWorkingYears": int(request.form["TotalWorkingYears"])
        }

        # Convert to DataFrame
        df = pd.DataFrame([employee_data])

        # Encode categorical features
        for col, le in encoders.items():
            df[col] = le.transform(df[col])

        df = df[features]

        # Make prediction
        pred = model.predict(df)[0]
        proba = model.predict_proba(df)[0][1] * 100  # probability in %

        # Prediction message
        result = "⚠️ Yes, Employee may leave" if pred == 1 else "✅ No, Employee is likely to stay"

        # Risk level for UI
        if proba > 60:
            risk_level = "danger"   # High risk
        elif proba > 30:
            risk_level = "warning"  # Medium risk
        else:
            risk_level = "success"  # Low risk

        # Feature importance
        feature_importance = [
            {"feature": f, "importance": round(float(im), 4)}
            for f, im in zip(features, importance)
        ]

        # Top 3 factors
        top_features = sorted(feature_importance, key=lambda x: x["importance"], reverse=True)[:3]
        for f in top_features:
            f["color"] = risk_level

        # Explanations
        explanations = []
        for f in top_features:
            if pred == 1:
                explanations.append(f"Higher {f['feature']} seems to increase attrition risk.")
            else:
                explanations.append(f"{f['feature']} is contributing positively to employee retention.")

        # ===============================
        # Save prediction to storage file
        # ===============================
        record = employee_data.copy()
        record.update({
            "Prediction": result,
            "Probability": round(proba, 2),
            "RiskLevel": risk_level,
            "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })

        # Append to CSV
        if not os.path.exists(STORAGE_FILE):
            pd.DataFrame([record]).to_csv(STORAGE_FILE, index=False)
        else:
            pd.DataFrame([record]).to_csv(STORAGE_FILE, mode="a", header=False, index=False)

        # Render results page
        return render_template(
            "result.html",
            result=result,
            probability=round(proba, 2),
            risk_level=risk_level,
            details=employee_data,
            importance=json.dumps(feature_importance),
            top_features=top_features,
            explanations=explanations
        )

    # Render input page
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
