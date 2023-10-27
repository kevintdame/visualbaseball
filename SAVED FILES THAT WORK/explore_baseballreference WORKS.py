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
