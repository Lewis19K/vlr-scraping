import os
from dotenv import load_dotenv
from flask import Flask, jsonify, request
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from scraper import get_event_stats

# Load environment variables
load_dotenv()

# Connect to MongoDB
uri = os.getenv("MONGO_URI")
if not uri:
    raise ValueError("MONGO_URI environment variable not set")

client = MongoClient(uri, server_api=ServerApi('1'))

# Get database and collection
db = client['vlr-event-stats']
collection = db['event-stats']

app = Flask(__name__)

# Route to scrape player stats from an event and save to MongoDB
@app.route('/api/stats/scrape', methods=['POST'])
def scrape_and_save():
    event_url = request.json.get('event_url')
    if not event_url:
        return jsonify({"error": "Missing event_url parameter"}), 400

    # Scrape player stats using the provided URL
    player_stats = get_event_stats(event_url)
    if not player_stats:
        return jsonify({"error": "No stats found for the event"}), 404

    # Update or insert player stats to MongoDB
    try:
        for player in player_stats:
            collection.update_one(
                {"Player": player["Player"], "Team": player["Team"]},  # Filter by player name and team
                {"$set": player},  # Update the fields with new data
                upsert=True  # Insert if the player doesn't exist
            )
    except Exception as e:
        return jsonify({"error": str(e)}), 500

    return jsonify({
        "message": "Scraped stats updated successfully"
    })

# Route to get player stats from MongoDB
@app.route('/api/stats', methods=['GET'])
def get_stats_from_mongo():
    name = request.args.get('name')
    team = request.args.get('team')

    query = {}
    if name:
        query["Player"] = {"$regex": name, "$options": "i"}
    if team:
        query["Team"] = {"$regex": team, "$options": "i"}

    try:
        results = list(collection.find(query, {"_id": 0}))  # Exclude _id field
    except Exception as e:
        return jsonify({"error": str(e)}), 500

    if not results:
        return jsonify({"error": "No stats found with the given filters"}), 404

    return jsonify(results)

# Route to delete all player stats from MongoDB
@app.route('/api/stats', methods=['DELETE'])
def delete_all_stats():
    try:
        result = collection.delete_many({})  # Delete all documents
    except Exception as e:
        return jsonify({"error": str(e)}), 500

    return jsonify({"message": f"{result.deleted_count} documents deleted successfully"})

# --- Endpoints for data analysis ---
# Route to get top 5 players by ACS
@app.route('/api/stats/top/acs', methods=['GET'])
def get_top_acs():
    try:
        top_acs = list(collection.find({}, {"_id": 0}).sort("ACS", -1).limit(5))  # Sort by ACS in descending order
    except Exception as e:
        return jsonify({"error": str(e)}), 500

    if not top_acs:
        return jsonify({"error": "No stats found"}), 404

    return jsonify(top_acs)

# Route to get top 5 players by Rating
@app.route('/api/stats/top/rating', methods=['GET'])
def get_top_rating():
    try:
        top_rating = list(collection.find({}, {"_id": 0}).sort("Rating", -1).limit(5))  # Sort by Rating in descending order
    except Exception as e:
        return jsonify({"error": str(e)}), 500

    if not top_rating:
        return jsonify({"error": "No stats found"}), 404

    return jsonify(top_rating)

# Route to get top 5 players by K/D Ratio
@app.route('/api/stats/top/kd', methods=['GET'])
def get_top_kd():
    try:
        top_kd = list(collection.find({}, {"_id": 0}).sort("K/D Ratio", -1).limit(5))  # Sort by K/D Ratio in descending order
    except Exception as e:
        return jsonify({"error": str(e)}), 500

    if not top_kd:
        return jsonify({"error": "No stats found"}), 404

    return jsonify(top_kd)

if __name__ == "__main__":
    app.run(debug=True)