
import json
from flask_cors import CORS
from flask import Flask, jsonify, request

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

# Sample player data
players = [

    # GOALKEEPERS
    {"id": 1, "name": "ROJIT SHRESTHA", "price": 10, "position": "GK",
        "isCaptain": False, "realTeam": "JOSHI JAGUARS"},
    {"id": 2, "name": "SUJAN BK", "price": 8, "position": "GK",
        "isCaptain": False, "realTeam": "SOTI SOLDIERS"},
    {"id": 3, "name": "PRASHANNA PAUDEL", "price": 7, "position": "GK",
        "isCaptain": False, "realTeam": "ACHARYA ATTACKERS"},
    {"id": 4, "name": "TANISHK THAPA", "price": 9, "position": "GK",
        "isCaptain": False, "realTeam": "ZENITH ZEBRAS"},
    {"id": 5, "name": "AAYUSH ROKA", "price": 8, "position": "GK",
        "isCaptain": False, "realTeam": "BENZE BULLS"},
    {"id": 6, "name": "SANGAM SHRESTHA", "price": 10, "position": "GK",
        "isCaptain": False, "realTeam": "GODAR GOATS"},

    # FORWARDS
    {"id": 7, "name": "SABIN DAHAL", "price": 10, "position": "FWD",
        "isCaptain": False, "realTeam": "BENZE BULLS"},
    {"id": 8, "name": "SACHIN SEN", "price": 8, "position": "FWD",
        "isCaptain": False, "realTeam": "ZENITH ZEBRAS"},
    {"id": 9, "name": "SAKAR SUBEDI", "price": 7, "position": "FWD",
        "isCaptain": False, "realTeam": "BENZE BULLS"},
    {"id": 10, "name": "SANDIL KATUWAL", "price": 9, "position": "FWD",
        "isCaptain": False, "realTeam": "GODAR GOATS"},
    {"id": 11, "name": "SANJAYA ADHIKARI", "price": 8, "position": "FWD",
        "isCaptain": False, "realTeam": "ACHARYA ATTACKERS"},
    {"id": 12, "name": "SANKALPA SHARMA", "price": 10, "position": "FWD",
        "isCaptain": False, "realTeam": "JOSHI JAGUARS"},
    {"id": 13, "name": "SHRIJAN BHUSAL", "price": 10, "position": "FWD",
        "isCaptain": False, "realTeam": "ZENITH ZEBRAS"},
    {"id": 14, "name": "SHUBHAM SINGH", "price": 8, "position": "FWD",
        "isCaptain": False, "realTeam": "GODAR GOATS"},
    {"id": 15, "name": "SHUSHANT ADHIKARI", "price": 7, "position": "FWD",
        "isCaptain": False, "realTeam": "JOSHI JAGAURS"},
    {"id": 16, "name": "SHYAM MAHATO", "price": 9, "position": "FWD",
        "isCaptain": False, "realTeam": "GODAR GOATS"},
    {"id": 17, "name": "SUDIP BARAL", "price": 8, "position": "FWD",
        "isCaptain": True, "realTeam": "BENZE BULLS"},
    {"id": 18, "name": "SUJIT GURUNG", "price": 10, "position": "FWD",
        "isCaptain": False, "realTeam": "ZENITH ZEBRAS"},
    {"id": 19, "name": "SUMAN CHHETRI", "price": 8, "position": "FWD",
        "isCaptain": False, "realTeam": "SOTI SOLDIERS"},
    {"id": 20, "name": "UNIQUE REGMI", "price": 10, "position": "FWD",
        "isCaptain": False, "realTeam": "SOTI SOLDIERS"},
    {"id": 21, "name": "SUMAN SHARMA", "price": 10, "position": "FWD",
        "isCaptain": False, "realTeam": "SOTI SOLDIERS"},
    {"id": 22, "name": "UDHAY THAKUR", "price": 8, "position": "FWD",
        "isCaptain": False, "realTeam": "GODAR GOATS"},


    # DEFENDERS
    {"id": 23, "name": "SAJAN ROKAYA", "price": 7, "position": "DEF",
        "isCaptain": False, "realTeam": "ZENITH ZEBRAS"},
    {"id": 24, "name": "SAMEER ACHARYA", "price": 9, "position": "DEF",
        "isCaptain": True, "realTeam": "ACHARYA ATTACKERS"},
    {"id": 25, "name": "SAMIR GODAR", "price": 8, "position": "DEF",
        "isCaptain": True, "realTeam": "GODAR GOATS"},
    {"id": 26, "name": "SANTOSH JOSHI", "price": 10, "position": "DEF",
        "isCaptain": True, "realTeam": "JOSHI JAGUARS"},
    {"id": 27, "name": "SUJAL PARAJULI", "price": 7, "position": "DEF",
        "isCaptain": False, "realTeam": "JOSHI JAGUARS"},
    {"id": 28, "name": "SUJAL SOTI", "price": 9, "position": "DEF",
        "isCaptain": True, "realTeam": "SOTI SOLDIERS"},
    {"id": 29, "name": "SUJAN BHAATTA", "price": 8, "position": "DEF",
        "isCaptain": False, "realTeam": "SOTI SOLDIERS"},
    {"id": 30, "name": "SUSHAN PANDEY", "price": 10, "position": "DEF",
        "isCaptain": False, "realTeam": "ACHARYA ATTACKERS"},
    {"id": 31, "name": "SWORNIM TIMILSINA", "price": 10, "position": "DEF",
        "isCaptain": False, "realTeam": "ACHARYA ATTACKERS"},
    {"id": 32, "name": "VIVEK GAUTAM", "price": 7, "position": "DEF",
        "isCaptain": False, "realTeam": "ACHARYA ATTACKERS"},
    {"id": 33, "name": "ZENITH SARU", "price": 9, "position": "DEF",
        "isCaptain": True, "realTeam": "ZENITH ZEBRAS"},

    # FOREIGN PLAYERS
    {"id": 34, "name": "ANUJ THAPA", "price": 8, "position": "DEF",
        "isCaptain": False, "realTeam": "BENZE BULLS"},
    {"id": 35, "name": "ANUPAM BISTA", "price": 10, "position": "FWD",
        "isCaptain": False, "realTeam": "BENZE BULLS"},
    {"id": 36, "name": "TASHI SHERPA", "price": 7, "position": "FWD",
        "isCaptain": False, "realTeam": "BENZE BULLS"},
]


@app.route("/player", methods=["GET"])
def get_players():
    return jsonify(players)


@app.route("/save_team", methods=["POST"])
def save_team():
    data = request.get_json()
    with open('saved_teams.json', 'a') as f:
        json.dump(data, f)
        f.write('\n')
    print(f"💾 SAVED to saved_teams.json")
    print("Received team:", data)
    return jsonify({"status": "success"})


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
