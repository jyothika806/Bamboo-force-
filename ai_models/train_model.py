# Train a model to predict ride safety

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
import joblib

# 1) Load dataset
df = pd.read_csv("data/dataset.csv")

# 2) Features (X) and target (y)
X = df.drop("safe", axis=1)
y = df["safe"]

# 3) Split data
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# 4) Train model
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# 5) Evaluate
y_pred = model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)

print(f"Model Accuracy: {accuracy * 100:.2f}%")

# 6) Save model
joblib.dump(model, "model/safety_model.pkl")
print("Model saved as model/safety_model.pkl")