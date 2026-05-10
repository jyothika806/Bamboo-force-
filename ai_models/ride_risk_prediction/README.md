## 📊 Dataset Overview

This dataset is **synthetically generated** to simulate real-world ride safety conditions.

It is used to train the AI model to predict whether a ride is **safe or unsafe**.

---
## 📸 Dataset Preview

![Dataset Preview](dataset_preview1.jpeg)
![Dataset Preview](dataset_preview2.jpeg)
![Dataset Preview](dataset_preview3.jpeg)
![Dataset Preview](dataset_preview4.jpeg)

---
## 🔗 Interactive Dataset

View the dataset in interactive format:

👉 https://docs.google.com/spreadsheets/d/1VyY4ONTvQa892PweqSD2IiS0xTs8qvxqguMQgIx_iMs/edit?usp=sharing

---

## 📁 File

* `dataset.csv` → Main dataset used for training

---

## 🧠 Features Description

| Column        | Description                                  |
| ------------- | -------------------------------------------- |
| time          | 0 = Day, 1 = Night                           |
| area_risk     | 0 = Low risk, 1 = Medium risk, 2 = High risk |
| driver_rating | Driver rating (range: 1 to 5)                |
| ride_type     | 0 = Bike, 1 = Auto, 2 = Car                  |
| distance_km   | Distance of ride in kilometers               |
| traffic_level | 0 = Low, 1 = Medium, 2 = High                |
| weather       | 0 = Clear, 1 = Rain                          |
| safe          | 1 = Safe ride, 0 = Unsafe ride               |

---

## ⚙️ Data Generation Logic

The dataset is generated using a rule-based system that mimics real-world risk factors:

* Night time increases risk
* High-risk areas increase risk
* Low driver rating increases risk
* Bike rides are less safe compared to cars
* Rainy weather increases risk
* Long distances and high traffic may increase risk

A **risk score** is calculated using these conditions, and the final label (`safe`) is assigned accordingly.

---

## 🎯 Purpose

This dataset helps the model learn patterns between ride conditions and safety, enabling:

* Safety prediction
* Risk analysis
* Intelligent ride recommendations

---

## 🏆 Note

This is a **synthetic dataset**, created for demonstration and hackathon purposes, but designed to reflect realistic scenarios.
