import requests
from bs4 import BeautifulSoup

def convert_to_int(value):
    try:
        return int(value)
    except ValueError:
        return None  # If it cannot be converted to int, return None

def convert_to_float(value):
    try:
        return float(value)
    except ValueError:
        return None  # If it cannot be converted to float, return None

def convert_percentage(value):
    try:
        # If it's a percentage, convert it to decimal
        if "%" in value:
            return float(value.replace('%', '').strip()) / 100
        return float(value)  # If it's already in decimal format
    except ValueError:
        return 0  # In case of error, return 0

def convert_clutches(value):
    try:
        if "/" in value:
            success, total = value.split('/')
            return {"success": int(success), "total": int(total)}  # Return the numeric values
        return {"success": None, "total": None}  # If not a valid fraction
    except ValueError:
        return {"success": None, "total": None}

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
        
        # Convert stats to appropriate types
        rounds_played = convert_to_int(cols[2].text.strip())
        rating = convert_to_float(cols[3].find('span').text.strip()) if cols[3].find('span') else None
        acs = convert_to_float(cols[4].find('span').text.strip()) if cols[4].find('span') else None
        kd_ratio = convert_to_float(cols[5].find('span').text.strip()) if cols[5].find('span') else None
        kast = convert_percentage(cols[6].find('span').text.strip()) if cols[6].find('span') else None
        adr = convert_to_float(cols[7].find('span').text.strip()) if cols[7].find('span') else None
        kpr = convert_to_float(cols[8].find('span').text.strip()) if cols[8].find('span') else None
        apr = convert_to_float(cols[9].find('span').text.strip()) if cols[9].find('span') else None
        fkpr = convert_to_float(cols[10].find('span').text.strip()) if cols[10].find('span') else None
        fdpr = convert_to_float(cols[11].find('span').text.strip()) if cols[11].find('span') else None
        hs_percentage = convert_percentage(cols[12].find('span').text.strip()) if cols[12].find('span') else None
        clutch_percentage = convert_percentage(cols[13].find('span').text.strip()) if cols[13].find('span') else None
        clutches = convert_clutches(cols[14].text.strip())
        max_kills = convert_to_int(cols[15].text.strip())
        kills = convert_to_int(cols[16].text.strip())
        deaths = convert_to_int(cols[17].text.strip())
        assists = convert_to_int(cols[18].text.strip())
        first_kills = convert_to_int(cols[19].text.strip())
        first_deaths = convert_to_int(cols[20].text.strip())

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
