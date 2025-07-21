import json
from bs4 import BeautifulSoup
from kafka import KafkaProducer
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import time

def create_kafka_producer():
    # This function creates a connection to your running Kafka server
    return KafkaProducer(
        bootstrap_servers='localhost:9092',
        value_serializer=lambda v: json.dumps(v).encode('utf-8')
    )

def scrape_and_produce(pages=1):
    producer = create_kafka_producer()
    driver = webdriver.Chrome()
    base_url = "https://internshala.com/internships/work-from-home-internships"

    print(f"🚀 Starting scrape for {pages} page(s)...")

    for page in range(1, pages + 1):
        url = f"{base_url}/page-{page}"
        print(f"Scraping page: {url}")
        driver.get(url)

        try:
            WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.ID, "internship_list_container"))
            )
        except Exception:
            print(f"Container not found on page {page}. Skipping.")
            continue

        soup = BeautifulSoup(driver.page_source, "html.parser")
        internship_cards = soup.find_all("div", class_="individual_internship")

        for card in internship_cards:
            try:
                # Using the correct selectors from our previous analysis
                title = card.find("h3", class_="job-internship-name").get_text(strip=True)
                company = card.find("p", class_="company-name").get_text(strip=True)
                location = card.find("div", class_="locations").get_text(strip=True)
                duration_icon = card.find("i", class_="ic-16-calendar")
                duration = duration_icon.find_next_sibling("span").get_text(strip=True)
                stipend = card.find("span", class_="stipend").get_text(strip=True)
                posted_date_icon = card.find("i", class_="ic-16-reschedule")
                posted_date = posted_date_icon.find_next_sibling("span").get_text(strip=True)
                link = "https://internshala.com" + card.get("data-href", "")

                internship_record = {
                    "Title": title,
                    "Company": company,
                    "Location": location,
                    "Duration": duration,
                    "Stipend": stipend,
                    "Posted_Date": posted_date,
                    "Link": link
                }
                
                # This line sends the data to your Kafka server
                producer.send('internship_postings', internship_record)
                print(f"Sent to Kafka: {title}")
                
            except Exception as e:
                # Skips any cards that might be ads or have a different structure
                continue
        
        time.sleep(2) # A small delay to be respectful to the website

    producer.flush()
    producer.close()
    driver.quit()
    print("✅ Scraping and sending to Kafka complete.")

if __name__ == "__main__":
    scrape_and_produce(pages=2)
