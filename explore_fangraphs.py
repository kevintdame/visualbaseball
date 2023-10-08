from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from bs4 import BeautifulSoup
import pandas as pd
import time

BASE_URL = 'https://www.fangraphs.com/leaders/major-league?pos=all&stats=pit&lg=all&qual=y&type=8&month=0&ind=0&sortcol=20&sortdir=desc&startdate=&enddate=&season1={year}&season={year}'

options = webdriver.ChromeOptions()
options.add_argument('--headless')  # Setting the browser to headless mode
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36")
driver = webdriver.Chrome(options=options)

all_data_frames = []
SLEEP_INTERVAL = 10

for year in range(1900, 2025):
    time.sleep(SLEEP_INTERVAL)
    print(f"Fetching data for {year}...")
    url = BASE_URL.format(year=year)
    driver.get(url)

    try:
        element_present = EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'td[data-stat="Name"]'))
        WebDriverWait(driver, 60).until(element_present)
    except TimeoutException:
        print(f"Timed out waiting for page to load for the year {year}")
        continue

    soup = BeautifulSoup(driver.page_source, 'html.parser')

    try:
        name_elements = soup.find_all('td', {'data-stat': 'Name'})
        player_names = [name.a.text if name.a else 'N/A' for name in name_elements]
        
        team_elements = soup.find_all('td', {'data-stat': 'Team'})
        teams = [team.a.text if team.a else 'N/A' for team in team_elements]

        war_elements = soup.find_all('td', {'data-stat': 'WAR'})
        war_values = [war.text if war else 'N/A' for war in war_elements]

        df = pd.DataFrame({
            'Year': year,
            'Player Name': player_names,
            'Team': teams,
            'WAR': war_values
        })

        all_data_frames.append(df.head(30))

    except AttributeError as e:
        print(f"Error occurred for the year {year}.")
        continue

driver.quit()  # Using quit() to close the entire browser process
final_df = pd.concat(all_data_frames)
final_df.to_csv('baseball_data_1900_2024.csv', index=False)
print("Data scraping complete. Data saved to 'baseball_data_1900_2024.csv'.")
