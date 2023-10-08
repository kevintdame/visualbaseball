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
options.binary_location = 'Documents/BaseballWebsiteCode/chromedriver'
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36")
driver = webdriver.Chrome(options=options)

def close_popup(driver):
    try:
        close_button = driver.find_element_by_css_selector('[aria-label="close"]')
        close_button.click()
        print("Primary pop-up closed.")
    except:
        pass

def close_ad_popup(driver):
    try:
        ad_element = driver.find_element_by_css_selector('a.cnx-ad-slot')
        if ad_element:
            print("Detected the second type of ad pop-up. Refreshing the page.")
            driver.refresh()
    except:
        pass

def close_third_popup(driver):
    try:
        ad_element = driver.find_element_by_css_selector('div[id="logo"]')
        if ad_element:
            print("Detected the third type of pop-up. Refreshing the page.")
            driver.refresh()
    except:
        pass

def check_failure_to_load(driver):
    try:
        body_text = driver.find_element_by_tag_name('body').text
        if "error loading data" in body_text:
            return True
    except:
        pass
    return False

all_data_frames = []
SLEEP_INTERVAL = 10

for year in range(1900, 2025):
    time.sleep(SLEEP_INTERVAL)
    print(f"Fetching data for {year}...")
    url = BASE_URL.format(year=year)
    driver.get(url)

    close_popup(driver)
    close_ad_popup(driver)
    close_third_popup(driver)

    try:
        element_present = EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'td[data-stat="Name"]'))
        WebDriverWait(driver, 60).until(element_present)
    except TimeoutException:
        print(f"Timed out waiting for page to load for the year {year}")
        if "429 Too Many Requests" in driver.page_source:
            SLEEP_INTERVAL += 5
            print(f"Encountered rate limit. Increasing sleep interval to {SLEEP_INTERVAL} seconds.")
            continue
        elif check_failure_to_load(driver):
            print("Encountered 'error loading data' message. Retrying...")
            driver.refresh()
            continue
        else:
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

driver.close()
final_df = pd.concat(all_data_frames)
final_df.to_csv('baseball_data_1900_2024.csv', index=False)
print("Data scraping complete. Data saved to 'baseball_data_1900_2024.csv'.")

# Code that creates a list of all players and their career start and end years:

import requests
from bs4 import BeautifulSoup
import csv

def get_players(letter):
    url = f"https://www.baseball-reference.com/players/{letter}/"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")

    players = []
    for item in soup.select("p"):
        link = item.find('a')
        if link:
            name = link.text
            years = item.text.replace(name, '').strip().strip("()")
            players.append((name, years))
    return players

def save_to_csv(players):
    with open("all_players.csv", "w", newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Player Name", "Years"])
        for player in players:
            writer.writerow(player)

def main():
    all_players = []
    for letter in 'abcdefghijklmnopqrstuvwxyz':
        print(f"Processing players with last names starting with '{letter}'...")
        all_players.extend(get_players(letter))

    # Filter out unwanted entries
    unwanted_entries = ["Professional Baseball", "Other Personnel", "Managers Directory", "Bullpen Wiki"]
    all_players = [player for player in all_players if not any(unwanted in player[0] for unwanted in unwanted_entries)]

    save_to_csv(all_players)
    print("All players saved to all_players.csv")

if __name__ == "__main__":
    main()
