import pandas as pd
import random

data = []

for _ in range(100):
    time = random.randint(0,1)
    area_risk = random.randint(0,2)
    driver_rating = round(random.uniform(2.5,5.0),1)
    ride_type = random.randint(0,2)
    distance = random.randint(2,15)
    traffic = random.randint(0,2)
    weather = random.randint(0,1)

    # Improved risk logic
    risk_score = 0

    if time == 1:
        risk_score += 1
    if area_risk == 2:
        risk_score += 2
    if driver_rating < 3.5:
        risk_score += 2
    if ride_type == 0:
        risk_score += 1
    if weather == 1:
        risk_score += 1
    if distance > 10:
        risk_score += 1
    if traffic == 2:
        risk_score += 1

    safe = 1 if risk_score < 4 else 0

    data.append([time, area_risk, driver_rating, ride_type, distance, traffic, weather, safe])

df = pd.DataFrame(data, columns=[
    'time','area_risk','driver_rating','ride_type','distance_km','traffic_level','weather','safe'
])

df.to_csv("data/dataset.csv", index=False)
print("Dataset created!")