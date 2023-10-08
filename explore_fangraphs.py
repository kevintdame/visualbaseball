from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from bs4 import BeautifulSoup
import pandas as pd
import time

PITCHERS_URL = 'https://www.fangraphs.com/leaders/major-league?pos=all&stats=pit&lg=all&qual=y&type=8&month=0&ind=0&sortcol=20&sortdir=desc&startdate=&enddate=&season1={year}&season={year}'
# HITTERS_URL = 'https://www.fangraphs.com/leaders/major-league?pos=all&stats=bat&lg=all&qual=y&type=8&month=0&ind=0&startdate=&enddate=&season1={year}&season={year}'

SLEEP_INTERVAL = 10

CHROMEDRIVER_PATH = '/Users/kevindame/Documents/BaseballWebsiteCode/chromedriver'
options = webdriver.ChromeOptions()
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36")
driver = webdriver.Chrome(options=options)


# ... [Your popup handling functions remain the same]

def scrape_fangraphs_data(base_url, category):
    all_data_frames = []
    for year in range(1900, 2025):
        time.sleep(SLEEP_INTERVAL)
        print(f"Fetching {category} data for {year}...")
        url = base_url.format(year=year)
        driver.get(url)

        close_popup(driver)
        close_ad_popup(driver)
        close_third_popup(driver)

        # ... [rest of your existing code for handling pop-ups, waiting for the page, and extracting data]

        df = pd.DataFrame({
            'Year': year,
            'Player Name': player_names,
            'Team': teams,
            'WAR': war_values
        })
        all_data_frames.append(df.head(30))

    return pd.concat(all_data_frames)

# Scrape data for pitchers and save to CSV
pitchers_data = scrape_fangraphs_data(PITCHERS_URL, "pitchers")
pitchers_data.to_csv('baseball_data_pitchers_1900_2024.csv', index=False)
print("Pitchers data scraping complete. Data saved to 'baseball_data_pitchers_1900_2024.csv'.")

# Commented out the hitters scraping part
# hitters_data = scrape_fangraphs_data(HITTERS_URL, "hitters")
# hitters_data.to_csv('baseball_data_hitters_1900_2024.csv', index=False)
# print("Hitters data scraping complete. Data saved to 'baseball_data_hitters_1900_2024.csv'.")

driver.close()
