import requests
from bs4 import BeautifulSoup
import pandas as pd

# Base URL of vlr.gg
BASE_URL = "https://www.vlr.gg"

# Function to get player stats for a specific event
def get_event_stats(event_url):
    response = requests.get(event_url)
    if response.status_code != 200:
        print("Error accessing the page:", event_url)
        return []

    soup = BeautifulSoup(response.text, 'html.parser')

    # Find the stats table
    stats_table = soup.find('table', class_='wf-table')
    if not stats_table:
        print("Stats table not found on the page.")
        return []

    # Extract table rows
    rows = stats_table.find('tbody').find_all('tr')
    players_stats = []

    for row in rows:
        cols = row.find_all('td')
        if len(cols) < 21:  # Ensure there are enough columns
            continue

        player_name = cols[0].find('div', class_='text-of').text.strip() if cols[0].find('div', class_='text-of') else "Unknown"
        team = cols[0].find('div', class_='stats-player-country').text.strip() if cols[0].find('div', class_='stats-player-country') else "No team"
        agents = ", ".join([img['src'].split('/')[-1].replace('.png', '') for img in cols[1].find_all('img')])
        rounds_played = cols[2].text.strip()
        rating = cols[3].find('span').text.strip() if cols[3].find('span') else "N/A"
        acs = cols[4].find('span').text.strip() if cols[4].find('span') else "N/A"
        kd_ratio = cols[5].find('span').text.strip() if cols[5].find('span') else "N/A"
        kast = cols[6].find('span').text.strip() if cols[6].find('span') else "N/A"
        adr = cols[7].find('span').text.strip() if cols[7].find('span') else "N/A"
        kpr = cols[8].find('span').text.strip() if cols[8].find('span') else "N/A"
        apr = cols[9].find('span').text.strip() if cols[9].find('span') else "N/A"
        fkpr = cols[10].find('span').text.strip() if cols[10].find('span') else "N/A"
        fdpr = cols[11].find('span').text.strip() if cols[11].find('span') else "N/A"
        hs_percentage = cols[12].find('span').text.strip() if cols[12].find('span') else "N/A"
        clutch_percentage = cols[13].find('span').text.strip() if cols[13].find('span') else "N/A"
        clutches = cols[14].text.strip()
        max_kills = cols[15].text.strip()
        kills = cols[16].text.strip()
        deaths = cols[17].text.strip()
        assists = cols[18].text.strip()
        first_kills = cols[19].text.strip()
        first_deaths = cols[20].text.strip()

        players_stats.append({
            "Player": player_name,
            "Team": team,
            "Agents": agents,
            "Rounds Played": rounds_played,
            "Rating": rating,
            "ACS": acs,
            "K/D Ratio": kd_ratio,
            "KAST": kast,
            "ADR": adr,
            "Kills per Round": kpr,
            "Assists per Round": apr,
            "First Kills per Round": fkpr,
            "First Deaths per Round": fdpr,
            "Headshot %": hs_percentage,
            "Clutch Success %": clutch_percentage,
            "Clutches": clutches,
            "Max Kills": max_kills,
            "Kills": kills,
            "Deaths": deaths,
            "Assists": assists,
            "First Kills": first_kills,
            "First Deaths": first_deaths
        })

    return players_stats

# Save player stats to a CSV file
def save_to_csv(data, filename):
    df = pd.DataFrame(data)
    df.to_csv(filename, index=False)
    print(f"Data saved to {filename}")

# Main function - Execute the scraping process
if __name__ == "__main__":
    event_url = "https://www.vlr.gg/event/stats/2278/tixinha-invitational-by-bonoxs" # Replace with the URL of the stats page for the event you want to scrape
    print("Scraping player stats for the event...")
    player_stats = get_event_stats(event_url)
    if player_stats:
        save_to_csv(player_stats, "tixinha_invitational_stats.csv")
        print(f"Scraped stats for {len(player_stats)} players.")
    else:
        print("No stats found for the event.")
