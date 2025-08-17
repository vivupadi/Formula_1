## Formula 1 Dashboard

# 🔎 Overview

This project demonstrates an ETL workflow using Python and Streamlit, powered by the Open F1 API.

Extract: Pull race data from the API (leaders, track temperature, humidity).

Transform: Clean, sort, and structure the data for each race track.

Load/Visualize: Display insights in an interactive Streamlit dashboard where users can select a track and view the leader and race-day conditions.

Although currently implemented in a batch mode, this project will be expanded to include real-time data ingestion and streaming ETL pipelines (Kafka/Spark).

<img width="1901" height="1008" alt="image" src="https://github.com/user-attachments/assets/eab16a2e-2b79-4e12-a6a6-5dff145bffd9" />
<img width="1900" height="996" alt="image" src="https://github.com/user-attachments/assets/a5dcca38-aa69-4a85-97f7-7c90719ffc2b" />

## 🛠️ Tech Stack

Python (data extraction + cleaning)

Streamlit (interactive dashboard)

Open F1 API (data source)

## 📊 Features

Dropdown selection of track (2024 races).

Display of race leader, track temperature, and humidity.

Simple data cleaning pipeline before visualization.

## 🚀 Next Steps (Roadmap)

Implement scheduling for automated daily ingestion.

Build a real-time ETL version using Kafka/Spark/Flink.

Add database support (Postgres/DuckDB).

Enhance dashboard with live updating leaderboards and team stats.

## ▶️ Run It Locally
git clone https://github.com/vivupadi/Formula_1.git
pip install -r requirements.txt
streamlit run Formula_1.py
