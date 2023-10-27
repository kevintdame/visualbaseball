from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd
import time

PITCHERS_URL = 'https://www.fangraphs.com/leaders/major-league?pos=all&stats=pit&lg=all&qual=y&type=8&month=0&ind=0&sortcol=20&sortdir=desc&startdate=&enddate=&season1={year}&season={year}'
HITTERS_URL = 'https://www.fangraphs.com/leaders/major-league?pos=all&stats=bat&lg=all&qual=y&type=8&month=0&ind=0&startdate=&enddate=&season1={year}&season={year}'

options = webdriver.ChromeOptions()
options.add_argument('--headless')
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36")
driver = webdriver.Chrome(options=options)

def scrape_fangraphs_data(base_url, category):
    all_data_frames = []
    
    for year in range(1900, 2024):
        print(f"Fetching {category} data for {year}...")
        url = base_url.format(year=year)
        driver.get(url)
        time.sleep(5)

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

    return pd.concat(all_data_frames)

pitchers_data = scrape_fangraphs_data(PITCHERS_URL, "pitchers")
hitters_data = scrape_fangraphs_data(HITTERS_URL, "hitters")

driver.quit()

pitchers_data.to_csv('baseball_pitchers_1900_2024.csv', index=False)
hitters_data.to_csv('baseball_hitters_1900_2024.csv', index=False)

print("Data scraping complete.")
