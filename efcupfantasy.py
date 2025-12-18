import streamlit as st
import pandas as pd
from datetime import datetime
import streamlit as st

# Load Google Sheets using SECRETS.TOML (your config is perfect)
@st.cache_resource
def load_sheets():
    # Uses your secrets.toml automatically
    gc = st.connection("google_sheets")
    return gc

# YOUR FULL PLAYERS LIST (prices fixed for ₹100 budget)
PLAYERS = [
    {"id": 1, "name": "ROJIT SHRESTHA", "price": 8, "position": "GK", "isCaptain": False, "realTeam": "JOSHI JAGUARS"},
    {"id": 2, "name": "SUJAN BK", "price": 7, "position": "GK", "isCaptain": False, "realTeam": "SOTI SOLDIERS"},
    {"id": 3, "name": "PRASHANNA PAUDEL", "price": 7, "position": "GK", "isCaptain": False, "realTeam": "ACHARYA ATTACKERS"},
    {"id": 4, "name": "TANISHK THAPA", "price": 8, "position": "GK", "isCaptain": False, "realTeam": "ZENITH ZEBRAS"},
    {"id": 5, "name": "AAYUSH ROKA", "price": 7, "position": "GK", "isCaptain": False, "realTeam": "BENZE BULLS"},
    {"id": 6, "name": "SANGAM SHRESTHA", "price": 8, "position": "GK", "isCaptain": False, "realTeam": "GODAR GOATS"},
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
    {"id": 34, "name": "ANUJ THAPA", "price": 7, "position": "DEF", "isCaptain": False, "realTeam": "BENZE BULLS"},
    {"id": 35, "name": "ANUPAM BISTA", "price": 9, "position": "FWD", "isCaptain": False, "realTeam": "BENZE BULLS"},
    {"id": 36, "name": "TASHI SHERPA", "price": 7, "position": "FWD", "isCaptain": False, "realTeam": "BENZE BULLS"},
]
st.title("🏆 EF CUP FANTASY ")
@st.cache_resource
def get_sheet():
    # Direct access to your secrets.toml
    creds = service_account.Credentials.from_service_account_info(
        st.secrets["connections"]["google_sheets"],
        scopes=["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]
    )
    client = gspread.authorize(creds)
    
    # Create/open sheet
    sheet = client.create("EF Cup Fantasy Teams") if "EF Cup Fantasy Teams" not in [s.title for s in client.list_spreadsheet_files()] else client.open("EF Cup Fantasy Teams")
    worksheet = sheet.sheet1
    return worksheet

BUDGET = 100
team_name = st.text_input("🏷️ Team Name")
selected_players = st.multiselect(
    "⚽ Choose 6 players:", 
    [f"{p['name']} ({p['position']}) - ₹{p['price']}" for p in PLAYERS],
    max_selections=6
)

if selected_players:
    total_price = sum(int(sel.split(" - ₹")[1]) for sel in selected_players)
    st.metric("Budget", f"₹{total_price}/100")
    
    if total_price <= 100 and len(selected_players) == 6:
        st.success("✅ READY TO SAVE!")

if st.button("💾 SAVE TEAM", type="primary"):
    if team_name and len(selected_players) == 6:
        total_price = sum(int(sel.split(" - ₹")[1]) for sel in selected_players)
        if total_price <= 100:
            try:
                worksheet = get_sheet()
                
                # Get players
                team_players = []
                for sel in selected_players:
                    name = sel.split(" - ₹")[0].split(" (")[0]
                    player = next(p for p in PLAYERS if p["name"] == name)
                    team_players.append(player)
                
                # SAVE TO SHEETS
                worksheet.append_row([
                    team_name,
                    total_price,
                    "; ".join(p['name'] for p in team_players),
                    "; ".join(p['position'] for p in team_players),
                    datetime.now().strftime("%Y-%m-%d %H:%M")
                ])
                
                st.success("✅ SAVED TO GOOGLE SHEETS!")
                st.balloons()
                st.rerun()
            except Exception as e:
                st.error(f"❌ {e}")
        else:
            st.error("Over budget!")
    else:
        st.error("Need name + 6 players!")

# Show teams
try:
    worksheet = get_sheet()
    df = pd.DataFrame(worksheet.get_all_records())
    st.subheader("📊 Saved Teams")
    st.dataframe(df)
except:
    st.info("Save first team!")
