# Real-Time-Internship-Market-Analyzer
A real-time data pipeline using Python, Kafka, and Streamlit to scrape and visualize live internship data from Internshala.
# Real-Time Internship Market Analyzer

### [Watch a Live Demo of the Dashboard in Action](https://drive.google.com/file/d/1WCeF4rgk-OUwOVZbcTVOA-USUVGlQZP5/view?usp=sharing)

---

## Overview

This project is a complete, end-to-end data engineering pipeline that scrapes live internship postings from Internshala, streams the data in real-time using Apache Kafka, and visualizes key insights on a live, interactive dashboard built with Streamlit.

What began as a static data analysis project evolved into a fully automated, real-time system with a practical reminder feature, demonstrating a comprehensive skill set in web scraping, data streaming, real-time data processing, and application development.

---

## Project Workflow & Architecture

The system is designed with a decoupled, producer-consumer architecture, which is a standard pattern for scalable, real-time data processing.

**Scraper (Producer)** `->` **Apache Kafka (Data Pipeline)** `->` **Dashboard (Consumer)**

1.  **Data Collection:** A Python scraper using Selenium and BeautifulSoup extracts the latest internship data from the web. The scraper is designed to run "headlessly" in the background.
2.  **Data Streaming:** Instead of saving to a static file, the scraper acts as a Kafka Producer, sending each internship record as a message to a Kafka topic (`internship_postings`).
3.  **Real-Time Visualization:** A Streamlit application acts as a Kafka Consumer, listening to the topic. It processes and displays the data as it arrives, updating KPIs and charts live.
4.  **Automation:** The entire pipeline is made hands-free by a `cron` job that automatically runs the scraper at the top of every hour, ensuring the dashboard is always up-to-date.

---

## Technology Stack

* **Data Collection:** Python, Selenium, BeautifulSoup, webdriver-manager
* **Data Streaming:** Apache Kafka
* **Dashboard & Visualization:** Streamlit, Pandas
* **Data Analysis & Modeling:** Jupyter Notebook, Scikit-learn
* **Automation:** Cron (macOS)

---

## Key Features

* **Live Data Feed:** The dashboard is not a static report; it updates in real-time as new internships are scraped.
* **Dynamic KPIs:** Tracks the total number of internships scraped, the approximate average stipend, and the number of urgent opportunities.
* **"Expiring Soon" Reminders:** A key feature that identifies and displays internships with an estimated application deadline of 3 days or less, helping users prioritize applications.
* **Real-Time Charts:** Visualizes the top hiring companies and the most common internship durations, which update automatically.
* **Automated & Resilient:** The system is fully automated to run 24/7 and includes logging for monitoring and debugging the background scraper.

---

## Project Phases

This project was completed in three major phases, showing a clear progression from analysis to a full-fledged data product.

### Phase 1: Static Data Analysis & Predictive Modeling

The initial phase involved a deep dive into a single scraped dataset to establish a baseline understanding.

* **Data Cleaning & EDA:** A Jupyter Notebook was used to perform extensive data cleaning on messy, real-world data (e.g., parsing varied stipend and duration formats). Key insights were uncovered through exploratory data analysis and visualization.
* **Stipend Prediction:** A predictive model (Random Forest Regressor) was built to forecast internship stipends. The model's low R-squared value was a key finding, indicating that category and duration alone are not sufficient predictors and highlighting the need for a more dynamic approach.

### Phase 2: Real-Time Pipeline and Dashboard

The insights from Phase 1 led to the development of a more advanced, real-time system.

* **Kafka Integration:** The scraper was refactore  to act as a Kafka Producer, transitioning the project from batch processing to real-time streaming.
* **Live Dashboard Development:** A Streamlit application was built to act as a Kafka Consumer, providing a live, interactive view of the internship market.
* **Full Automation:** The data collection process was fully automated using a `cron` job and the scraper was configured to run headlessly in the background.

### Phase 3: Feature Enhancement

The final phase focused on adding practical, value-added features to the dashboard.

* **Reminder System:** An "Expiring Soon" feature was implemented. This system uses the `Posted_Date` to estimate an application deadline and alerts the user to opportunities that are closing soon, making the dashboard a more actionable tool.

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
pip install pandas streamlit kafka-python selenium beautifulsoup4 webdriver-manager
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

