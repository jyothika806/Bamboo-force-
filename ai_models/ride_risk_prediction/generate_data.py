import os
import pandas as pd
import random

# =========================================================
# DATASET STORAGE
# =========================================================

data = []

# =========================================================
# GENERATE SYNTHETIC DATA
# =========================================================

for _ in range(5000):

    # ============================================
    # BASIC FEATURES
    # ============================================

    time = random.randint(0, 1)
    # 0 = day
    # 1 = night

    area_risk = random.randint(0, 2)
    # 0 = safe
    # 1 = medium
    # 2 = dangerous

    driver_rating = round(
        random.choices([2.5,3,3.5,4,4.5,5],weights=[2,5,10,35,35,13])[0],
        1
    )

    ride_type = random.randint(0, 2)
    # 0 = bike
    # 1 = auto
    # 2 = cab

    distance = random.randint(2, 25)

    traffic = random.choices(
        [0, 1, 2],
        weights=[55,35,10]
    )[0]
    # 0 = low
    # 1 = medium
    # 2 = high

    weather = random.randint(0, 1)
    # 0 = clear
    # 1 = bad weather

    # ============================================
    # NEW FEATURES
    # ============================================

    driver_experience = random.randint(0, 15)

    cancellation_rate = round(
        random.uniform(0, 40),
        1
    )

    emergency_area = random.choices(
        [0, 1],
        weights=[95,5]
    )[0]

    speed_risk = random.choices(
        [0, 1, 2],
        weights=[70,20,10]
    )[0]
    # 0 = safe
    # 1 = moderate
    # 2 = dangerous

    repeated_complaints = random.randint(0, 10)
    ride_duration = random.randint(5, 90)

    avg_speed = random.randint(20, 100)

    speed_variation = round(
        random.uniform(0, 30),
        2
    )
    sharp_turns = random.randint(0, 10)
    crash_detected = random.choices(
        [0, 1],
        weights=[98, 2]
    )[0]
    sudden_accelerations = random.randint(0, 5)
    sudden_braking = random.randint(0, 5)
    stop_frequency = random.randint(0, 10)
    idle_time = random.randint(0, 15)
    gps_signal_loss = random.choices(
        [0,1],
        weights=[97,3]
    )[0]
    camera_occlusion = random.choices(
        [0,1],
        weights=[98,2]
    )[0]
    incorrect_readings = random.choices(
        [0,1],
        weights=[99,1]
    )[0]
    panic_button = random.choices(
        [0,1],
        weights=[99,1]
    )[0]
    unsafe_stop = random.choices(
        [0,1],
        weights=[98,2]
    )[0]
    unexpected_route_change = random.choices(
        [0,1],
        weights=[97,3]
    )[0]
    driver_phone_useage = random.choices(
        [0,1],
        weights=[95,5]
    )[0]

    # ============================================
    # RISK LOGIC
    # ============================================

    risk_score = 0

    if time == 1 and random.random() < 0.6:
        risk_score += 1

    if area_risk == 2:
        risk_score += 2

    if driver_rating < 3.5:
        risk_score += 2

    if ride_type == 0:
        risk_score += 1

    if weather == 1:
        risk_score += 1

    if distance > 15:
        risk_score += 1

    if traffic == 2:
        risk_score += 1

    # ============================================
    # NEW FEATURE IMPACT
    # ============================================

    if driver_experience < 2:
        risk_score += 2

    if cancellation_rate > 25:
        risk_score += 2

    if emergency_area == 1:
        risk_score += 3

    if speed_risk == 2 and random.random() < 0.75:
        risk_score += 3

    if repeated_complaints > 5 and random.random() < 0.8:
        risk_score += 2

    # ============================================
    # FINAL LABEL
    # ============================================

    safe = 1 if risk_score < 6 else 0

    # ============================================
    # STORE ROW
    # ============================================

    data.append([

    time,
    area_risk,
    driver_rating,
    ride_type,
    distance,
    traffic,
    weather,

    driver_experience,
    cancellation_rate,
    emergency_area,
    speed_risk,
    repeated_complaints,

    ride_duration,
    avg_speed,
    speed_variation,
    sharp_turns,
    crash_detected,
    sudden_accelerations,
    sudden_braking,
    stop_frequency,
    idle_time,

    gps_signal_loss,
    camera_occlusion,
    incorrect_readings,

    panic_button,
    unsafe_stop,
    unexpected_route_change,
    driver_phone_usage,

    safe
])
# =========================================================
# CREATE DATAFRAME
# =========================================================

df = pd.DataFrame(data, columns=[

    'time',
    'area_risk',
    'driver_rating',
    'ride_type',
    'distance_km',
    'traffic_level',
    'weather',

    'driver_experience',
    'cancellation_rate',
    'emergency_area',
    'speed_risk',
    'repeated_complaints',

    'ride_duration',
    'avg_speed',
    'speed_variation',
    'sharp_turns',
    'crash_detected',
    'sudden_accelerations',
    'sudden_braking',
    'stop_frequency',
    'idle_time',

    'gps_signal_loss',
    'camera_occlusion',
    'incorrect_readings',

    'panic_button',
    'unsafe_stop',
    'unexpected_route_change',
    'driver_phone_useage',

    'safe'
])
# =========================================================
# CREATE SAVE DIRECTORY
# =========================================================

save_dir = os.path.join(
    "ai_models",
    "ride_risk_prediction",
    "datasets"
)

os.makedirs(
    save_dir,
    exist_ok=True
)
# =========================================================
# SAVE CSV
# =========================================================

save_path = os.path.join(
    save_dir,
    "dataset.csv"
)

df.to_csv(
    save_path,
    index=False
)

print("\nDataset created successfully ✅")
print(f"\nSaved to: {save_path}")

print("\nPreview:\n")
print(df.head())