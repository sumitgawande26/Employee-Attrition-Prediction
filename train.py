import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
import joblib

# ==========================
# 1. Load dataset
# ==========================
df = pd.read_csv("Data/WA_Fn-UseC_-HR-Employee-Attrition.csv")

# Pick 8 important features
features = [
    "Age", "MonthlyIncome", "JobRole", "OverTime",
    "DistanceFromHome", "JobSatisfaction", "WorkLifeBalance", "TotalWorkingYears"
]
target = "Attrition"

# ==========================
# 2. Preprocess data
# ==========================
# Encode target
target_encoder = LabelEncoder()
df[target] = target_encoder.fit_transform(df[target])

# Encode categorical features
label_encoders = {}
for col in ["JobRole", "OverTime"]:
    le = LabelEncoder()
    df[col] = le.fit_transform(df[col])
    label_encoders[col] = le

# ✅ Ensure JobSatisfaction & WorkLifeBalance are clamped to 1–5
df["JobSatisfaction"] = df["JobSatisfaction"].clip(1, 5)
df["WorkLifeBalance"] = df["WorkLifeBalance"].clip(1, 5)

# ==========================
# 3. Train/Test Split
# ==========================
X = df[features]
y = df[target]
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

# ==========================
# 4. Train Model
# ==========================
model = RandomForestClassifier(
    n_estimators=200,          # more trees = more stable
    random_state=42,
    class_weight="balanced"    # handle imbalance in attrition data
)
model.fit(X_train, y_train)

# ==========================
# 5. Evaluate
# ==========================
y_pred = model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
print(f"✅ Model trained with accuracy: {accuracy:.2f}")

# ==========================
# 6. Save Model & Metadata
# ==========================
model_package = {
    "model": model,
    "encoders": label_encoders,
    "target_encoder": target_encoder,  # Save target encoder
    "features": features,
    "importance": model.feature_importances_.tolist()  # JSON serializable
}

joblib.dump(model_package, "model.pkl")
print("📦 Model & metadata saved as model.pkl")
