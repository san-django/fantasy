import streamlit as st
import gspread
from google.oauth2.service_account import Credentials
from datetime import datetime
import json

# FIXED: Define PLAYERS FIRST before any Streamlit code
PLAYERS = [
    # GOALKEEPERS
    {"id": 1, "name": "ROJIT SHRESTHA", "price": 8, "position": "GK", "isCaptain": False, "realTeam": "JOSHI JAGUARS"},
    {"id": 2, "name": "SUJAN BK", "price": 7, "position": "GK", "isCaptain": False, "realTeam": "SOTI SOLDIERS"},
    {"id": 3, "name": "PRASHANNA PAUDEL", "price": 7, "position": "GK", "isCaptain": False, "realTeam": "ACHARYA ATTACKERS"},
    {"id": 4, "name": "TANISHK THAPA", "price": 8, "position": "GK", "isCaptain": False, "realTeam": "ZENITH ZEBRAS"},
    {"id": 5, "name": "AAYUSH ROKA", "price": 7, "position": "GK", "isCaptain": False, "realTeam": "BENZE BULLS"},
    {"id": 6, "name": "SANGAM SHRESTHA", "price": 8, "position": "GK", "isCaptain": False, "realTeam": "GODAR GOATS"},

    # FORWARDS - LOWER PRICES FOR ₹100 BUDGET
    {"id": 7, "name": "SABIN DAHAL", "price": 9, "position": "FWD", "isCaptain": False, "realTeam": "BENZE BULLS"},
    {"id": 8, "name": "SACHIN SEN", "price": 8, "position": "FWD", "isCaptain": False, "realTeam": "ZENITH ZEBRAS"},
    {"id": 9, "name": "SAKAR SUBEDI", "price": 7, "position": "FWD", "isCaptain": False, "realTeam": "BENZE BULLS"},
    {"id": 10, "name": "SANDIL KATUWAL", "price": 8, "position": "FWD", "isCaptain": False, "realTeam": "GODAR GOATS"},
    {"id": 11, "name": "SANJAYA ADHIKARI", "price": 7, "position": "FWD", "isCaptain": False, "realTeam": "ACHARYA ATTACKERS"},
    {"id": 12, "name": "SANKALPA SHARMA", "price": 9, "position": "FWD", "isCaptain": False, "realTeam": "JOSHI JAGUARS"},
    {"id": 13, "name": "SHRIJAN BHUSAL", "price": 9, "position": "FWD", "isCaptain": False, "realTeam": "ZENITH ZEBRAS"},
    {"id": 14, "name": "SHUBHAM SINGH", "price": 8, "position": "FWD", "isCaptain": False, "realTeam": "GODAR GOATS"},
    {"id": 15, "name": "SHUSHANT ADHIKARI", "price": 7, "position": "FWD", "isCaptain": False, "realTeam": "JOSHI JAGUARS"},
    {"id": 16, "name": "SHYAM MAHATO", "price": 8, "position": "FWD", "isCaptain": False, "realTeam": "GODAR GOATS"},
    {"id": 17, "name": "SUDIP BARAL", "price": 8, "position": "FWD", "isCaptain": True, "realTeam": "BENZE BULLS"},
    {"id": 18, "name": "SUJIT GURUNG", "price": 9, "position": "FWD", "isCaptain": False, "realTeam": "ZENITH ZEBRAS"},
    {"id": 19, "name": "SUMAN CHHETRI", "price": 8, "position": "FWD", "isCaptain": False, "realTeam": "SOTI SOLDIERS"},
    {"id": 20, "name": "UNIQUE REGMI", "price": 9, "position": "FWD", "isCaptain": False, "realTeam": "SOTI SOLDIERS"},
    {"id": 21, "name": "SUMAN SHARMA", "price": 9, "position": "FWD", "isCaptain": False, "realTeam": "SOTI SOLDIERS"},
    {"id": 22, "name": "UDHAY THAKUR", "price": 8, "position": "FWD", "isCaptain": False, "realTeam": "GODAR GOATS"},

    # DEFENDERS - LOWEST PRICES
    {"id": 23, "name": "SAJAN ROKAYA", "price": 6, "position": "DEF", "isCaptain": False, "realTeam": "ZENITH ZEBRAS"},
    {"id": 24, "name": "SAMEER ACHARYA", "price": 7, "position": "DEF", "isCaptain": True, "realTeam": "ACHARYA ATTACKERS"},
    {"id": 25, "name": "SAMIR GODAR", "price": 6, "position": "DEF", "isCaptain": True, "realTeam": "GODAR GOATS"},
    {"id": 26, "name": "SANTOSH JOSHI", "price": 7, "position": "DEF", "isCaptain": True, "realTeam": "JOSHI JAGUARS"},
    {"id": 27, "name": "SUJAL PARAJULI", "price": 6, "position": "DEF", "isCaptain": False, "realTeam": "JOSHI JAGUARS"},
    {"id": 28, "name": "SUJAL SOTI", "price": 7, "position": "DEF", "isCaptain": True, "realTeam": "SOTI SOLDIERS"},
    {"id": 29, "name": "SUJAN BHAATTA", "price": 6, "position": "DEF", "isCaptain": False, "realTeam": "SOTI SOLDIERS"},
    {"id": 30, "name": "SUSHAN PANDEY", "price": 7, "position": "DEF", "isCaptain": False, "realTeam": "ACHARYA ATTACKERS"},
    {"id": 31, "name": "SWORNIM TIMILSINA", "price": 7, "position": "DEF", "isCaptain": False, "realTeam": "ACHARYA ATTACKERS"},
    {"id": 32, "name": "VIVEK GAUTAM", "price": 6, "position": "DEF", "isCaptain": False, "realTeam": "ACHARYA ATTACKERS"},
    {"id": 33, "name": "ZENITH SARU", "price": 7, "position": "DEF", "isCaptain": True, "realTeam": "ZENITH ZEBRAS"},

    # FOREIGN PLAYERS
    {"id": 34, "name": "ANUJ THAPA", "price": 7, "position": "DEF", "isCaptain": False, "realTeam": "BENZE BULLS"},
    {"id": 35, "name": "ANUPAM BISTA", "price": 9, "position": "FWD", "isCaptain": False, "realTeam": "BENZE BULLS"},
    {"id": 36, "name": "TASHI SHERPA", "price": 7, "position": "FWD", "isCaptain": False, "realTeam": "BENZE BULLS"},
]

# Google Sheets config - PUT YOUR CREDENTIALS HERE
SCOPE = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
CREDS_JSON = '''
{
  "type": "service_account",
  "project_id": "expanded-dryad-479915-j8",
  "private_key_id": "d4dd5ee9711ecfb6b43cce3bc14c2f518e70c115",
  "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvgIBADANBgkqhkiG9w0BAQEFAASCBKgwggSkAgEAAoIBAQCxGl9nNhwLGyxa\nyBfxhZTugpsHiOXLse9poFONgamMOhxqN+FUUKkwQnSHszlo4Xp5Vap5G1dEGBVJ\nvnyUJs4PnN14pQ1ylXoxcO+eAz3iw6STfaHwSS9geQEMPmspb3J4n45FyM+Vvp7Q\n5xQRSVJbl5f886KmSKSUe8XgMUQjq9f/6XUgJbioTMBBH3Lbogbl1LP5HHF6ruxW\nWc7PYBr00RAk9ERy0U74H9GpWSayvE/Ip1cGPAvo9SZOx2/qL0jNaJoLBSuJLVS/\n25vBcxy0N/LXO8TEpN7cTV1/GNyy5usxY1DmfwYbp9KUWvFCi5GC2wG6jGEXG+iF\n4EwtNQ2JAgMBAAECggEAJV1Ryvn6xSoUu8ty58Ed2ItED30ltEnEX9XUQurb/UqG\nU6+Z8dq5s0WWBco9fr/xgbdd6cKnsOVe2mneqTgdqeQXwrwZ3/ai6trvpvf6nsTV\njEuJdqNOJE2rN6zUmY+aiFHrZ5Q0HZzzr1HNZU9BmbLcPWEei/QQCwapCwGB5X9h\n9WsFb3T30fp96Krjx3PokIRuQB4c8A/fqB/9NRTubVyjo1YT9f3mbk3DLbQKfZm1\nkkuM3ipEb0mlk1URrJ2HVGrkx3/x3VGoMVU6FV8KyncjSTJwwQkCZXqWslu/emQZ\n0AeTW1AIE5j4OhtMvXMqkJBX69loCzJsz8AMvNb9rQKBgQDouTOFZgpzJr52sXb4\n7YO0MRu+IbRmkx86MtN9Vzn5u13qBEC0ybPv9V8ZR6PpP9PYW7DBcMzrAGu028rA\nuQ6vgN7Hyab33DJ3eL0tbVBgImEY1/nr9f9qNtGT5ey/dLs1sewcl+vPiloY7Ro0\n0L4wUprqyMV1hgKrtX9Dex7gPQKBgQDC0QfgZahThwVrI7YKFb74qkCgoEIESED/\nxrBH1L+SQbX4DwQHyJevqrdADxv2HPtNWu/Qak5QVBVbkKUnxC/Z97ju7EPYCBmt\nblgS5ox2arWgbHQaCRHTAetMkZGBJqVr9r2DCxhdWWIhvgjuPE4thfBPOdlmZG1w\nMHzMFIMLPQKBgQDFWvFnKh6ogm24yExlUz6CW7b0KS8MYa10tE+HlqYSsyM0ZkDd\nT8PpNYNdM9S75CXp7+/YS6lrjOLJ8C5j+0uJ59aFROv0e+bMTDbZxD8KF32SDO3j\nfa0JTM20B6MaxYpRQb5CjU8rpF89jizQJ0lyP0si2foh7PBs3zC6cDnB3QKBgGgC\nS289NuHpSzZJKY42z+9YjgpzpOs+XB1ySXkAF4sRNAKMmb1CFeG+hflYV7hM/sns\ny+38Y3U1fvWUwuf5MQbw37YHQ61ZncPfDnyAw+sQy4krfczMnMyH0MTfTsyiAl0i\nrUkCKm7kIqUbHQ97+M0LHiJeIzgsU9U6vdYC+XeNAoGBAN/lrKoWLqkPg1yBZBCY\nLYeR8MNW352Pxa5J4hpedE42hR3O3RYMVQqzy3B7tjMK2RgaGelSoqwNonFum7xJ\nPa0b+GCR7UtySlsNjNVsksrzsRFp50bNV6SqxEIw0gGGaQ4LPsr34yZDbsONE5GX\nSZ5cHEUAOjCBysSIpuylxxT2\n-----END PRIVATE KEY-----\n",
  "client_email": "futsal-prediction@expanded-dryad-479915-j8.iam.gserviceaccount.com",
  "client_id": "102738823036241479968",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/futsal-prediction%40expanded-dryad-479915-j8.iam.gserviceaccount.com",
  "universe_domain": "googleapis.com"
} '''# ← REPLACE WITH YOUR SERVICE ACCOUNT JSON

SHEET_NAME = "efcupfantasy"
WORKSHEET_NAME = "Sheet1"

@st.cache_resource
def connect_sheets():
    creds = Credentials.from_service_account_info(json.loads(CREDS_JSON), scopes=SCOPE)
    client = gspread.authorize(creds)
    sheet = client.create(SHEET_NAME) if SHEET_NAME not in [s.title for s in client.list_spreadsheet_files()] else client.open(SHEET_NAME)
    worksheet = sheet.worksheet(WORKSHEET_NAME) if WORKSHEET_NAME in [ws.title for ws in sheet.worksheets()] else sheet.add_worksheet(WORKSHEET_NAME, 1000, 5)
    return worksheet

def save_team_to_sheets(worksheet, team_data):
    worksheet.append_row([
        team_data['teamName'],
        team_data['totalPrice'],
        "; ".join([p['name'] for p in team_data['players']]),
        "; ".join([p['position'] for p in team_data['players']]),
        team_data['savedAt'][:16]
    ])
    return True

# MAIN APP
st.title("🏆 EF CUP FANTASY \nCreate Your Team")
st.markdown("**Teams SAVED TO GOOGLE SHEETS PERMANENTLY!**")

try:
    worksheet = connect_sheets()
    st.success("✅ Connected to Google Sheets!")
except Exception as e:
    st.error(f"❌ Sheets error: {e}")
    st.stop()

BUDGET = 100
team_name = st.text_input("🏷️ Team Name")
selected_players = st.multiselect(
    "⚽ Choose 6 players:", 
    [f"{p['name']} ({p['position']}) - ₹{p['price']}" for p in PLAYERS],
    max_selections=6
)

if selected_players:
    total_price = sum(int(sel.split(" - ₹")[1]) for sel in selected_players)
    st.metric("Budget", f"₹{total_price}", f"₹{BUDGET-total_price}")
    
    if total_price <= BUDGET and len(selected_players) == 6:
        st.success("✅ READY - Click SAVE!")

# SAVE TO GOOGLE SHEETS
if st.button("💾 SAVE TO GOOGLE SHEETS", type="primary"):
    if not team_name:
        st.error("Enter team name!")
    elif len(selected_players) != 6:
        st.error("Select exactly 6 players!")
    elif total_price > BUDGET:
        st.error("Over budget!")
    else:
        team_players = []
        for sel in selected_players:
            name = sel.split(" - ₹")[0].split(" (")[0]
            player = next(p for p in PLAYERS if p["name"] == name)
            team_players.append(player)
        
        success = save_team_to_sheets(worksheet, {
            "teamName": team_name,
            "players": team_players,
            "totalPrice": total_price,
            "savedAt": datetime.now().isoformat()
        })
        
        if success:
            st.balloons()
            st.success("🎉 TEAM SAVED TO GOOGLE SHEETS!")
            st.rerun()

# SHOW TEAMS FROM SHEETS
st.subheader("📊 Teams from Google Sheets")
try:
    teams_df = worksheet.get_all_records()
    if teams_df:
        st.dataframe(teams_df)
    else:
        st.info("Save your first team!")
except:
    st.info("Loading teams...")
