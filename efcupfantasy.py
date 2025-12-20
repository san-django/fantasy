import streamlit as st
import pandas as pd
from datetime import datetime
from google.oauth2 import service_account
import gspread

# COMPLETE 36 PLAYERS LIST
PLAYERS = [
    {"id": 1, "name": "ROJIT SHRESTHA", "price": 8, "position": "GK", "realTeam": "JOSHI JAGUARS"},
    {"id": 2, "name": "SUJAN BK", "price": 7, "position": "GK", "realTeam": "SOTI SOLDIERS"},
    {"id": 3, "name": "PRASHANNA PAUDEL", "price": 7, "position": "GK", "realTeam": "ACHARYA ATTACKERS"},
    {"id": 4, "name": "TANISHK THAPA", "price": 8, "position": "GK", "realTeam": "ZENITH ZEBRAS"},
    {"id": 5, "name": "AAYUSH ROKA", "price": 7, "position": "GK", "realTeam": "BENZE BULLS"},
    {"id": 6, "name": "SANGAM SHRESTHA", "price": 8, "position": "GK", "realTeam": "GODAR GOATS"},
    {"id": 7, "name": "SABIN DAHAL", "price": 9, "position": "FWD", "realTeam": "BENZE BULLS"},
    {"id": 8, "name": "SACHIN SEN", "price": 8, "position": "FWD", "realTeam": "ZENITH ZEBRAS"},
    {"id": 9, "name": "SAKAR SUBEDI", "price": 7, "position": "FWD", "realTeam": "BENZE BULLS"},
    {"id": 10, "name": "SANDIL KATUWAL", "price": 8, "position": "FWD", "realTeam": "GODAR GOATS"},
    {"id": 11, "name": "SANJAYA ADHIKARI", "price": 7, "position": "FWD", "realTeam": "ACHARYA ATTACKERS"},
    {"id": 12, "name": "SANKALPA SHARMA", "price": 9, "position": "FWD", "realTeam": "JOSHI JAGUARS"},
    {"id": 13, "name": "SHRIJAN BHUSAL", "price": 9, "position": "FWD", "realTeam": "ZENITH ZEBRAS"},
    {"id": 14, "name": "SHUBHAM SINGH", "price": 8, "position": "FWD", "realTeam": "GODAR GOATS"},
    {"id": 15, "name": "SHUSHANT ADHIKARI", "price": 7, "position": "FWD", "realTeam": "JOSHI JAGUARS"},
    {"id": 16, "name": "SHYAM MAHATO", "price": 8, "position": "FWD", "realTeam": "GODAR GOATS"},
    {"id": 17, "name": "SUDIP BARAL", "price": 8, "position": "FWD", "realTeam": "BENZE BULLS"},
    {"id": 18, "name": "SUJIT GURUNG", "price": 9, "position": "FWD", "realTeam": "ZENITH ZEBRAS"},
    {"id": 19, "name": "SUMAN CHHETRI", "price": 8, "position": "FWD", "realTeam": "SOTI SOLDIERS"},
    {"id": 20, "name": "UNIQUE REGMI", "price": 9, "position": "FWD", "realTeam": "SOTI SOLDIERS"},
    {"id": 21, "name": "SUMAN SHARMA", "price": 9, "position": "FWD", "realTeam": "SOTI SOLDIERS"},
    {"id": 22, "name": "UDHAY THAKUR", "price": 8, "position": "FWD", "realTeam": "GODAR GOATS"},
    {"id": 23, "name": "SAJAN ROKAYA", "price": 6, "position": "DEF", "realTeam": "ZENITH ZEBRAS"},
    {"id": 24, "name": "SAMEER ACHARYA", "price": 7, "position": "DEF", "realTeam": "ACHARYA ATTACKERS"},
    {"id": 25, "name": "SAMIR GODAR", "price": 6, "position": "DEF", "realTeam": "GODAR GOATS"},
    {"id": 26, "name": "SANTOSH JOSHI", "price": 7, "position": "DEF", "realTeam": "JOSHI JAGUARS"},
    {"id": 27, "name": "SUJAL PARAJULI", "price": 6, "position": "DEF", "realTeam": "JOSHI JAGUARS"},
    {"id": 28, "name": "SUJAL SOTI", "price": 7, "position": "DEF", "realTeam": "SOTI SOLDIERS"},
    {"id": 29, "name": "SUJAN BHAATTA", "price": 6, "position": "DEF", "realTeam": "SOTI SOLDIERS"},
    {"id": 30, "name": "SUSHAN PANDEY", "price": 7, "position": "DEF", "realTeam": "ACHARYA ATTACKERS"},
    {"id": 31, "name": "SWORNIM TIMILSINA", "price": 7, "position": "DEF", "realTeam": "ACHARYA ATTACKERS"},
    {"id": 32, "name": "VIVEK GAUTAM", "price": 6, "position": "DEF", "realTeam": "ACHARYA ATTACKERS"},
    {"id": 33, "name": "ZENITH SARU", "price": 7, "position": "DEF", "realTeam": "ZENITH ZEBRAS"},
    {"id": 34, "name": "ANUJ THAPA", "price": 7, "position": "DEF", "realTeam": "BENZE BULLS"},
    {"id": 35, "name": "ANUPAM BISTA", "price": 9, "position": "FWD", "realTeam": "BENZE BULLS"},
    {"id": 36, "name": "TASHI SHERPA", "price": 7, "position": "FWD", "realTeam": "BENZE BULLS"},
]

# SHEET CONNECTION (your "efcupfantasy")
@st.cache_resource
def get_sheet():
    creds = service_account.Credentials.from_service_account_info(
        st.secrets["connections"]["google_sheets"],
        scopes=["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]
    )
    client = gspread.authorize(creds)
    sheet = client.open("efcupfantasy")
    return sheet.sheet1

st.title("🏆 EF CUP FANTASY LEAGUE")
st.markdown("**Dynamic DEF/FWD - Selections STAY!**")

BUDGET = 100
team_name = st.text_input("🏷️ **Team Name**")
owner_name = st.text_input("👤 **Your Name**")

# Initialize session state for selections
if 'selected_gk' not in st.session_state:
    st.session_state.selected_gk = []
if 'selected_fwd' not in st.session_state:
    st.session_state.selected_fwd = []
if 'selected_def' not in st.session_state:
    st.session_state.selected_def = []

# POSITION COLUMNS - FIXED SESSION STATE
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("### 🧤 **GK (1)**")
    gk_options = [f"{p['name']} (₹{p['price']})" for p in PLAYERS if p['position'] == 'GK']
    new_gk = st.multiselect("GK", gk_options, default=st.session_state.selected_gk, max_selections=1)
    st.session_state.selected_gk = new_gk

with col2:
    st.markdown("### ⚽ **FWD**")
    fwd_options = [f"{p['name']} (₹{p['price']})" for p in PLAYERS if p['position'] == 'FWD']
    # Dynamic max based on DEF count
    def_count = len(st.session_state.selected_def)
    max_fwd = 3 if def_count == 2 else 4
    st.caption(f"Max: {max_fwd} FWD")
    new_fwd = st.multiselect("FWD", fwd_options, default=st.session_state.selected_fwd, max_selections=max_fwd)
    st.session_state.selected_fwd = new_fwd

with col3:
    st.markdown("### 🛡️ **DEF**")
    def_options = [f"{p['name']} (₹{p['price']})" for p in PLAYERS if p['position'] == 'DEF']
    # Dynamic max based on FWD count
    fwd_count = len(st.session_state.selected_fwd)
    max_def = 3 if fwd_count >= 2 else 2
    st.caption(f"Max: {max_def} DEF")
    new_def = st.multiselect("DEF", def_options, default=st.session_state.selected_def, max_selections=max_def)
    st.session_state.selected_def = new_def

# Combine selections
selected_players = (st.session_state.selected_gk + 
                   st.session_state.selected_fwd + 
                   st.session_state.selected_def)

# Budget & Status
if selected_players:
    total_price = sum(int(p.split("₹")[1].strip(")")) for p in selected_players)
    budget_left = BUDGET - total_price
    
    col1, col2, col3 = st.columns(3)
    col1.metric("Total", len(selected_players), "6")
    col2.metric("Budget", f"₹{total_price}", f"₹{budget_left}")
    col3.metric("Status", "✅ READY" if budget_left >= 0 and len(selected_players) == 6 else "⚠️ FIX")
    
    # Live limits display
    st.info(f"**Limits:** FWD max={3 if len(st.session_state.selected_def)==2 else 4} | DEF max={3 if len(st.session_state.selected_fwd)>=2 else 2}")
    
    if budget_left >= 0 and len(selected_players) == 6:
        st.success(f"✅ **{len(st.session_state.selected_gk)}-{len(st.session_state.selected_fwd)}-{len(st.session_state.selected_def)} READY!**")
        st.markdown("### 📋 **Team:**")
        for player in selected_players:
            st.write(f"• {player}")

# SAVE TO SHEET
if st.button("💾 **SAVE TO efcupfantasy**", type="primary", use_container_width=True):
    if not team_name.strip() or not owner_name.strip():
        st.error("❌ Name fields required!")
    elif len(selected_players) != 6:
        st.error(f"❌ Need 6 players! (Have {len(selected_players)})")
    else:
        total_price = sum(int(p.split("₹")[1].strip(")")) for p in selected_players)
        if total_price > BUDGET:
            st.error(f"❌ Over budget: ₹{total_price}")
        else:
            try:
                worksheet = get_sheet()
                # Player details extraction
                team_players = []
                positions = []
                real_teams = []
                for sel in selected_players:
                    name = sel.split(" (")[0]
                    player = next(p for p in PLAYERS if p["name"] == name)
                    team_players.append(player['name'])
                    positions.append(player['position'])
                    real_teams.append(player['realTeam'])
                
                worksheet.append_row([
                    team_name.strip(),
                    total_price,
                    ", ".join(team_players),
                    ", ".join(positions),
                    ", ".join(real_teams),
                    datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    owner_name.strip()
                ])
                
                st.success(f"🎉 **SAVED!** {len(st.session_state.selected_gk)}-{len(st.session_state.selected_fwd)}-{len(st.session_state.selected_def)}")
                st.balloons()
                st.rerun()
            except Exception as e:
                st.error(f"❌ {str(e)}")

# LIVE LEAGUE TABLE
st.markdown("---")
st.subheader("🏆 **efcupfantasy LEAGUE**")
try:
    worksheet = get_sheet()
    records = worksheet.get_all_records()
    if records:
        df = pd.DataFrame(records)
        st.dataframe(df.tail(20), use_container_width=True)
    else:
        st.info("👆 Save first team!")
except Exception as e:
    st.error(f"❌ {e}")
