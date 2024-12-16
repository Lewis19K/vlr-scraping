from flask import Flask, jsonify, request
from scraper import get_event_stats
import pandas as pd

app = Flask(__name__)

# Route to scrape player stats for a specific event
@app.route('/api/stats', methods=['GET'])
def get_stats():
    event_url = request.args.get('event_url')
    if not event_url:
        return jsonify({"error": "Missing event_url parameter"}), 400

    player_stats = get_event_stats(event_url)
    if not player_stats:
        return jsonify({"error": "No stats found for the event"}), 404

    # Save player stats to a CSV file
    try:
        pd.DataFrame(player_stats).to_csv('data/event_stats.csv', index=False)
    except FileNotFoundError:
        return jsonify({"error": "Data file not found"}), 404
    return jsonify(player_stats)

# Route to filter player stats by name or team
@app.route('/api/stats/player', methods=['GET'])
def get_player_stats():
    name = request.args.get('name')
    team = request.args.get('team')

    if not name and not team:
        return jsonify({"error": "At least one of 'name' or 'team' must be provided"}), 400

    # Load data from CSV file
    try:
        data = pd.read_csv('data/event_stats.csv')
    except FileNotFoundError:
        return jsonify({"error": "Data file not found"}), 404

    # Filter data based on name and team
    filtered_data = data
    if name:
        filtered_data = filtered_data[filtered_data['Player'].str.contains(name, case=False, na=False)]
    if team:
        filtered_data = filtered_data[filtered_data['Team'].str.contains(team, case=False, na=False)]

    if filtered_data.empty:
        return jsonify({"error": "No players found with the specified filters"}), 404

    return jsonify(filtered_data.to_dict(orient='records'))

if __name__ == "__main__":
    app.run(debug=True)
