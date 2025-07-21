import streamlit as st
import pandas as pd
from kafka import KafkaConsumer
import json
import re
import time
from datetime import datetime, timedelta

# Page configuration
st.set_page_config(layout="wide")
st.title("📊 Live Internshala Internships Dashboard")

# --- Kafka Consumer Setup ---
@st.cache_resource
def get_kafka_consumer():
    consumer = KafkaConsumer(
        'internship_postings',
        bootstrap_servers='localhost:9092',
        auto_offset_reset='earliest',
        consumer_timeout_ms=1000,
        value_deserializer=lambda x: json.loads(x.decode('utf-8'))
    )
    return consumer

# --- Data Fetching Logic ---
def fetch_data(consumer):
    messages = consumer.poll(timeout_ms=1000, max_records=100)
    records = []
    if messages:
        for topic_partition, consumer_records in messages.items():
            for record in consumer_records:
                records.append(record.value)
    return records

# --- NEW: Function to estimate deadline ---
def get_estimated_deadline(posted_date_str):
    posted_date_str = str(posted_date_str).lower()
    today = datetime.now()
    
    if 'just now' in posted_date_str or 'today' in posted_date_str:
        post_date = today
    elif 'day' in posted_date_str:
        days_ago = int(re.findall(r'\d+', posted_date_str)[0])
        post_date = today - timedelta(days=days_ago)
    elif 'week' in posted_date_str:
        weeks_ago = int(re.findall(r'\d+', posted_date_str)[0])
        post_date = today - timedelta(weeks=weeks_ago)
    else: # Fallback for other formats like 'month'
        return None

    # Assume application deadline is 7 days after posting
    return post_date + timedelta(days=7)

# --- Main Application Logic ---
if 'all_data' not in st.session_state:
    st.session_state.all_data = []

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
    df_live = pd.DataFrame(st.session_state.all_data)

    # --- NEW: Calculate deadlines and days remaining ---
    df_live['Estimated_Deadline'] = df_live['Posted_Date'].apply(get_estimated_deadline)
    df_live.dropna(subset=['Estimated_Deadline'], inplace=True)
    df_live['Days_Remaining'] = (df_live['Estimated_Deadline'] - datetime.now()).dt.days
    
    # Filter for internships expiring in 3 days or less
    expiring_soon_df = df_live[df_live['Days_Remaining'].between(0, 3)].sort_values(by='Days_Remaining')

    # --- KPIs ---
    total_internships = len(df_live)
    stipends = df_live['Stipend'].str.extract(r'(\d[\d,]*\d|\d+)')[0]
    cleaned_stipends = stipends.dropna().str.replace(',', '').astype(float)
    avg_stipend = cleaned_stipends.mean() if not cleaned_stipends.empty else 0

    kpi1, kpi2, kpi3 = st.columns(3)
    kpi1.metric(label="Total Internships Scraped 📈", value=int(total_internships))
    kpi2.metric(label="Approx. Average Stipend (₹) 💵", value=f"{avg_stipend:,.0f}")
    kpi3.metric(label="Expiring Soon 🔥", value=len(expiring_soon_df))


    st.markdown("---")

    # --- NEW: Reminder Section ---
    if not expiring_soon_df.empty:
        st.subheader("🔥 Internships Expiring Soon (Apply Now!)")
        st.dataframe(expiring_soon_df[['Title', 'Company', 'Stipend', 'Days_Remaining', 'Link']])
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
    st.subheader("All Scraped Internships")
    st.dataframe(df_live.tail(10).iloc[::-1])

# --- Auto-Refresh Logic ---
time.sleep(3)
st.rerun()

