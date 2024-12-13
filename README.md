# Valorant Event Scraper - VLR.gg Scraping

This is a Python script that scrapes player stats for a specific event from [VLR.gg](https://vlr.gg).
It uses the BeautifulSoup library to parse the HTML and extract the necessary information. The script saves the player stats to a CSV file.

## Usage

To use the script, you need to provide the URL of the event's stats page on [VLR.gg](https://vlr.gg). You can find the URL for the stats page of a specific event by visiting the event's page on [VLR.gg](https://vlr.gg) and looking for the URL in the address bar.

Once you have the URL, you can run the script by executing the following command in your terminal or command prompt:

```
python scraper.py
```

## Example Output

Here's an example of the output of the script when run on the event's stats page:

```
Scraping player stats for the event...
Data saved to tixinha_invitational_stats.csv
Scraped stats for 41 players.
```

In this example, the script scrapes the player stats for the [Tixinha Invitational by BONOXS](https://www.vlr.gg/event/2278/tixinha-invitational-by-bonoxs) event and saves them to a CSV file named `tixinha_invitational_stats.csv`. The script then prints a message indicating that it has scraped the stats for 41 players.
