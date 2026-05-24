# feature_engineering.py

import pandas as pd
import numpy as np

import os
class FeatureEngineer:
    def __init__(self, input_file, output_file):
        self.input_file = input_file
        self.output_file = output_file

    def load_data(self):

        print("[INFO] Loading dataset...")

        self.df = pd.read_csv(
            self.input_file
        )

        print(
            f"[INFO] Dataset loaded with {len(self.df)} records."
        )

        # ====================================================
        # REQUIRED COLUMNS VALIDATION
        # ====================================================

        required_columns = [

            "avg_speed",
            "sudden_braking",
            "sharp_turns",
            "panic_button",
            "crash_detected",
            "gps_signal_loss",
            "unexpected_route_change",
            "time"
        ]

        missing = [

            col

            for col in required_columns

            if col not in self.df.columns
        ]

        if missing:

            raise ValueError(
                f"Missing columns: {missing}"
            )

    # ---------------------------------------------------
    # Driving Aggression
    # ---------------------------------------------------
    def create_aggression_score(self):
        print("[INFO] Creating aggression score...")

        self.df["aggression_score"] = (
            (self.df["avg_speed"] / 120) * 0.4 +
            (self.df["sudden_braking"] / 10) * 0.3 +
            (self.df["sharp_turns"] / 10) * 0.3
        )

        self.df["aggression_score"] = self.df["aggression_score"].clip(0, 1)

    # ---------------------------------------------------
    # Driving Stability
    # ---------------------------------------------------
    def create_driving_stability(self):
        print("[INFO] Creating driving stability...")

        self.df["driving_stability"] = (
            1 - (
                (self.df["sudden_braking"] / 10) * 0.5 +
                (self.df["sharp_turns"] / 10) * 0.5
            )
        )

        self.df["driving_stability"] = self.df["driving_stability"].clip(0, 1)

    # ---------------------------------------------------
    # Emergency Risk
    # ---------------------------------------------------
    def create_emergency_risk(self):
        print("[INFO] Creating emergency risk...")

        self.df["emergency_risk"] = (
            self.df["panic_button"] * 0.7 +
            self.df["crash_detected"] * 0.3
        )

        self.df["emergency_risk"] = self.df["emergency_risk"].clip(0, 1)

    # ---------------------------------------------------
    # Telemetry Reliability
    # ---------------------------------------------------
    def create_telemetry_reliability(self):
        print("[INFO] Creating telemetry reliability...")

        self.df["telemetry_reliability"] = (
            1 - (self.df["gps_signal_loss"] * 0.8)
        )

        self.df["telemetry_reliability"] = (
            self.df["telemetry_reliability"].clip(0, 1)
        )

    # ---------------------------------------------------
    # Suspicious Route Score
    # ---------------------------------------------------
    def create_suspicious_route_score(self):
        print("[INFO] Creating suspicious route score...")

        self.df["suspicious_route_score"] = (
            self.df["unexpected_route_change"] * 0.6 +
            (self.df["time"] == 1).astype(int) * 0.4
        )

        self.df["suspicious_route_score"] = (
            self.df["suspicious_route_score"].clip(0, 1)
        )

    # ---------------------------------------------------
    # Overall Risk Score
    # ---------------------------------------------------
    def create_overall_risk_score(self):
        print("[INFO] Creating overall risk score...")

        self.df["overall_risk_score"] = (
            self.df["aggression_score"] * 0.30 +
            self.df["emergency_risk"] * 0.30 +
            self.df["suspicious_route_score"] * 0.20 +
            (1 - self.df["telemetry_reliability"]) * 0.20
        )

        self.df["overall_risk_score"] = (
            self.df["overall_risk_score"].clip(0, 1)
        )

    # ---------------------------------------------------
    # Save Dataset
    # ---------------------------------------------------
    def save_data(self):
        self.df.to_csv(self.output_file, index=False)
        print(f"[INFO] Engineered dataset saved to: {self.output_file}")

    # ---------------------------------------------------
    # Run All
    # ---------------------------------------------------
    def run(self):
        self.load_data()

        self.create_aggression_score()
        self.create_driving_stability()
        self.create_emergency_risk()
        self.create_telemetry_reliability()
        self.create_suspicious_route_score()
        self.create_overall_risk_score()

        self.save_data()

        print("[SUCCESS] Feature engineering completed!")


# ---------------------------------------------------
# MAIN
# ---------------------------------------------------

if __name__ == "__main__":
    
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

    INPUT_FILE = os.path.join(
        BASE_DIR,
        "datasets",
        "dataset.csv"
    )

    OUTPUT_FILE = os.path.join(
        BASE_DIR,
        "datasets",
        "engineered_dataset.csv"
    )
    engineer = FeatureEngineer(INPUT_FILE, OUTPUT_FILE)
    engineer.run()