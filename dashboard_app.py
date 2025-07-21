import streamlit as st
import pandas as pd
from kafka import KafkaConsumer
import json
import re
import time

# Page configuration
st.set_page_config(layout="wide")
st.title("📊 Live Internshala Internships Dashboard")

# --- Kafka Consumer Setup ---
# This function creates a single, reusable Kafka consumer connection.
@st.cache_resource
def get_kafka_consumer():
    consumer = KafkaConsumer(
        'internship_postings',
        bootstrap_servers='localhost:9092',
        auto_offset_reset='earliest',
        consumer_timeout_ms=1000, # Important: sets a timeout
        value_deserializer=lambda x: json.loads(x.decode('utf-8'))
    )
    return consumer

# --- Data Fetching Logic ---
# This function fetches new messages in a non-blocking way.
def fetch_data(consumer):
    messages = consumer.poll(timeout_ms=1000, max_records=100)
    records = []
    if messages:
        for topic_partition, consumer_records in messages.items():
            for record in consumer_records:
                records.append(record.value)
    return records

# --- Main Application Logic ---

# Initialize session state to store all scraped data
if 'all_data' not in st.session_state:
    st.session_state.all_data = []

# Get the consumer and fetch any new data
try:
    consumer = get_kafka_consumer()
    new_records = fetch_data(consumer)
    if new_records:
        st.session_state.all_data.extend(new_records)
except Exception as e:
    st.error(f"Could not connect to Kafka. Please ensure it is running. Error: {e}")
    st.stop()


# --- Display Logic ---
if not st.session_state.all_data:
    st.warning("Waiting for data from the scraper... Please run the scraper script.")
else:
    # Create DataFrame from all collected data
    df_live = pd.DataFrame(st.session_state.all_data)

    # --- KPIs ---
    total_internships = len(df_live)
    stipends = df_live['Stipend'].str.extract(r'(\d[\d,]*\d|\d+)')[0]
    cleaned_stipends = stipends.dropna().str.replace(',', '').astype(float)
    avg_stipend = cleaned_stipends.mean() if not cleaned_stipends.empty else 0

    kpi1, kpi2 = st.columns(2)
    kpi1.metric(label="Total Internships Scraped 📈", value=int(total_internships))
    kpi2.metric(label="Approx. Average Stipend (₹) 💵", value=f"{avg_stipend:,.0f}")

    st.markdown("---")

    # --- Charts ---
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Top 10 Hiring Companies")
        company_counts = df_live['Company'].value_counts().head(10)
        st.bar_chart(company_counts)
    with col2:
        st.subheader("Internships by Duration")
        duration_counts = df_live['Duration'].value_counts().head(10)
        st.bar_chart(duration_counts)

    # --- Data Table ---
    st.subheader("Latest Internships Scraped")
    st.dataframe(df_live.tail(10).iloc[::-1])

# --- Auto-Refresh Logic ---
# This will cause the script to rerun every 3 seconds to check for new messages
time.sleep(3)
st.rerun()

