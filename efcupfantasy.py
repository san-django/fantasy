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

st.title("🏆 EF CUP FANTASY LEAGUE")
st.markdown("**Dynamic DEF/FWD - Auto-adjusts max selections!**")

# SHEET CONNECTION (working)
@st.cache_resource
def get_sheet():
    creds = service_account.Credentials.from_service_account_info(
        st.secrets["connections"]["google_sheets"],
        scopes=["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]
    )
    client = gspread.authorize(creds)
    sheet = client.open("efcupfantasy")
    return sheet.sheet1

BUDGET = 100
team_name = st.text_input("🏷️ **Team Name**")
owner_name = st.text_input("👤 **Your Name**")

# DYNAMIC SELECTION COLUMNS
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("### 🧤 **GK**")
    gk_options = [f"{p['name']} (₹{p['price']})" for p in PLAYERS if p['position'] == 'GK']
    selected_gk = st.multiselect("GK", gk_options, max_selections=1)

with col2:
    st.markdown("### ⚽ **FWD**")
    fwd_options = [f"{p['name']} (₹{p['price']})" for p in PLAYERS if p['position'] == 'FWD']
    # DYNAMIC MAX: if 2 DEF selected → max 3 FWD
    def_count = len(st.session_state.get('selected_def', []))
    max_fwd = 3 if def_count >= 2 else 4
    selected_fwd = st.multiselect("FWD", fwd_options, max_selections=max_fwd)

with col3:
    st.markdown("### 🛡️ **DEF**")
    def_options = [f"{p['name']} (₹{p['price']})" for p in PLAYERS if p['position'] == 'DEF']
    # DYNAMIC MAX: if 2 FWD selected → max 3 DEF
    fwd_count = len(selected_fwd)
    max_def = 3 if fwd_count >= 2 else 2
    selected_def = st.multiselect("DEF", def_options, max_selections=max_def)

# Store selections in session for dynamic updates
if 'selected_def' not in st.session_state:
    st.session_state.selected_def = []
if 'selected_fwd' not in st.session_state:
    st.session_state.selected_fwd = []

# Update session state
st.session_state.selected_fwd = selected_fwd
st.session_state.selected_def = selected_def

# Combine all selections
selected_players = selected_gk + selected_fwd + selected_def

# Budget & validation
if selected_players:
    total_price = sum(int(p.split("₹")[1].strip(")")) for p in selected_players)
    budget_left = BUDGET - total_price
    
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Players", len(selected_players), "6")
    col2.metric("Budget", f"₹{total_price}", f"₹{budget_left}")
    
    # Show current limits
    st.info(f"**Max FWD:** {3 if len(selected_def) >= 2 else 4} | **Max DEF:** {3 if len(selected_fwd) >= 2 else 2}")
    
    if budget_left >= 0 and len(selected_players) == 6:
        st.success(f"✅ **VALID TEAM READY!** {len(selected_gk)}GK + {len(selected_fwd)}FWD + {len(selected_def)}DEF")
        st.markdown("### 📋 **Your Team:**")
        for player in selected_players:
            st.write(f"• {player}")
    elif budget_left < 0:
        st.error(f"❌ **Over budget** ₹{-budget_left}!")
    else:
        st.warning("⚠️ **Select exactly 6 players**")

# SAVE BUTTON
if st.button("💾 **SAVE TO efcupfantasy**", type="primary", use_container_width=True):
    if not team_name.strip() or not owner_name.strip():
        st.error("❌ **Team Name & Your Name required!**")
    elif len(selected_players) != 6:
        st.error(f"❌ **Exactly 6 players needed!** (You have {len(selected_players)})")
    else:
        total_price = sum(int(p.split("₹")[1].strip(")")) for p in selected_players)
        if total_price > BUDGET:
            st.error(f"❌ **Over budget**: ₹{total_price}")
        else:
            try:
                worksheet = get_sheet()
                
                # Player details
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
                
                st.success(f"🎉 **{team_name} SAVED!** {len(selected_gk)}-{len(selected_fwd)}-{len(selected_def)}")
                st.balloons()
                st.rerun()
            except Exception as e:
                st.error(f"❌ **Save error:** {str(e)}")

# LIVE LEAGUE TABLE
st.markdown("---")
st.subheader("🏆 **efcupfantasy LIVE LEAGUE**")
try:
    worksheet = get_sheet()
    records = worksheet.get_all_records()
    if records:
        df = pd.DataFrame(records)
        st.dataframe(df.tail(20), use_container_width=True)
        st.success(f"✅ **{len(records)} teams joined!**")
    else:
        st.info("👆 **Be first to save!**")
except Exception as e:
    st.error(f"❌ {e}")
