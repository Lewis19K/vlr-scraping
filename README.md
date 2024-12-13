# Valorant Event Scraper - VLR.gg Scraping

This is a Python script that scrapes player stats for a specific event from [VLR.gg](https://vlr.gg).  
It uses the BeautifulSoup library to parse the HTML and extract the necessary information.  
The script saves the player stats to a CSV file.

## Installation

Before running the script, ensure you have Python installed on your system.  
Follow these steps to set up the environment:

1. Clone the repository:

   ```
   git clone https://github.com/Lewis19K/vlr-scraping.git
   cd vlr-scraping
   ```

2. Create a virtual environment (optional but recommended):

   ```
   python -m venv venv
   source venv/bin/activate    # On Windows: venv\Scripts\activate
   ```

3. Install the required dependencies:

   ```
   pip install -r requirements.txt
   ```

If you don't have a `requirements.txt` file, you can create one with the following content:

```
beautifulsoup4
pandas
requests
seaborn
```

You can generate this file with:

```
pip freeze > requirements.txt
```

## Usage

To use the script, you need to provide the URL of the event's stats page on [VLR.gg](https://vlr.gg).  
You can find the URL for the stats page of a specific event by visiting the event's page on [VLR.gg](https://vlr.gg) and looking for the URL in the address bar.

Once you have the URL, you can run the script by executing the following command:

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

In this example, the script scrapes the player stats for the [Tixinha Invitational by BONOXS](https://www.vlr.gg/event/2278/tixinha-invitational-by-bonoxs) event and saves them to a CSV file named `tixinha_invitational_stats.csv`.  
The script then prints a message indicating that it has scraped the stats for 41 players.

## Dependencies

- Python 3.7 or higher
- `beautifulsoup4`
- `pandas`
- `requests`
- `seaborn` (optional, for data analysis/visualization)

## Future Improvements

- Add support for analyzing the scraped data.
- Include visualizations for better insights.
