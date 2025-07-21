# Real-Time-Internship-Market-Analyzer
A real-time data pipeline using Python, Kafka, and Streamlit to scrape and visualize live internship data from Internshala.
# Real-Time Internship Market Analyzer

### [Watch a Live Demo of the Dashboard in Action](https://drive.google.com/file/d/1XJ0-cIIh_hg_XsyPsktV7ouHUtkGIJrp/view?usp=sharing)

---

## Overview

This project is a complete, end-to-end data engineering pipeline that scrapes live internship postings from Internshala, streams the data in real-time using Apache Kafka, and visualizes key insights on a live dashboard built with Streamlit.

The project began with a static data analysis and evolved into a fully automated, real-time system, demonstrating a comprehensive skill set in data collection, processing, analysis, and system design.

---

## Project Workflow & Architecture

The system is designed with a decoupled, producer-consumer architecture, which is a standard pattern for scalable, real-time data processing.

**Scraper (Producer)** `->` **Apache Kafka (Data Pipeline)** `->` **Dashboard (Consumer)**

1.  **Data Collection:** A Python scraper using Selenium and BeautifulSoup extracts the latest internship data from the web.
2.  **Data Streaming:** Instead of saving to a static file, the scraper acts as a Kafka Producer, sending each internship record as a message to a Kafka topic (`internship_postings`).
3.  **Real-Time Visualization:** A Streamlit application acts as a Kafka Consumer, listening to the topic. It processes and displays the data as it arrives, updating KPIs and charts live.
4.  **Automation:** The entire pipeline is made hands-free by a `cron` job that automatically runs the scraper at the top of every hour.

---

## Technology Stack

* **Data Collection:** Python, Selenium, BeautifulSoup
* **Data Streaming:** Apache Kafka
* **Dashboard & Visualization:** Streamlit, Pandas, Matplotlib, Seaborn
* **Data Analysis & Modeling:** Jupyter Notebook, Scikit-learn
* **Automation:** Cron (macOS)

---

## Key Features

* **Live Data Feed:** The dashboard is not a static report; it updates in real-time as new internships are scraped.
* **Dynamic KPIs:** Tracks the total number of internships scraped and the approximate average stipend on the fly.
* **Real-Time Charts:** Visualizes the top hiring companies and the most common internship durations, which update automatically.
* **Automated & Resilient:** The system is fully automated and designed to run continuously without manual intervention.

---

## Project Phases

This project was completed in two major phases:

### Phase 1: Static Data Analysis & Predictive Modeling

The initial phase involved a deep dive into a single scraped dataset to establish a baseline understanding.

* **Data Cleaning & EDA:** A Jupyter Notebook was used to perform extensive data cleaning on messy, real-world data (e.g., parsing varied stipend and duration formats). Key insights were uncovered through exploratory data analysis and visualization.
* **Stipend Prediction:** A predictive model (Random Forest Regressor) was built to forecast internship stipends based on features like category and duration. The model's low R-squared value was a key finding, indicating that these features alone are not sufficient predictors and highlighting the need for more data.

### Phase 2: Real-Time Pipeline and Dashboard

The insights from Phase 1 led to the development of a more advanced, real-time system.

* **Kafka Integration:** The scraper was refactored to act as a Kafka Producer, transitioning the project from batch processing to real-time streaming.
* **Live Dashboard Development:** A Streamlit application was built to act as a Kafka Consumer, providing a live, interactive view of the internship market.
* **Full Automation:** The data collection process was fully automated using a `cron` job, completing the end-to-end pipeline.

---

## How to Run This Project

### Prerequisites

* Python 3.x
* Apache Kafka
* A web browser and a terminal

### 1. Clone the Repository

```bash
git clone [https://github.com/vibhuti970/Real-Time-Internship-Market-Analyzer.git](https://github.com/vibhuti970/Real-Time-Internship-Market-Analyzer.git)
cd Real-Time-Internship-Market-Analyzer
```

### 2. Install Dependencies

```bash
pip install pandas streamlit kafka-python selenium beautifulsoup4
```

### 3. Start the Services

1.  **Start Kafka:** Ensure your Kafka server is running.
2.  **Run the Dashboard:** In a new terminal, run the Streamlit application:
    ```bash
    streamlit run dashboard_app.py
    ```

### 4. Start the Scraper

In another new terminal, run the scraper to begin populating the dashboard:

```bash
python internshala_scraper.py
