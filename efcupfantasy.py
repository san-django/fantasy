import streamlit as st
import pandas as pd
from datetime import datetime
from google.oauth2 import service_account
import gspread

# COMPLETE 36 PLAYERS LIST
PLAYERS = [
    {"id": 1, "name": "ROJIT SHRESTHA", "price": 13, "position": "GK", "realTeam": "JOSHI JAGUARS",},
    {"id": 2, "name": "SUJAN BK", "price": 15, "position": "GK", "realTeam": "SOTI SOLDIERS"},
    {"id": 3, "name": "PRASHANNA PAUDEL", "price": 15, "position": "GK", "realTeam": "ACHARYA ATTACKERS"},
    {"id": 4, "name": "TANISHK THAPA", "price": 11, "position": "GK", "realTeam": "ZENITH ZEBRAS"},
    {"id": 5, "name": "AAYUSH ROKA", "price": 14, "position": "GK", "realTeam": "BENZE BULLS"},
    {"id": 6, "name": "SANGAM SHRESTHA", "price": 10, "position": "GK", "realTeam": "GODAR GOATS"},
    {"id": 7, "name": "SABIN DAHAL", "price": 5, "position": "FWD", "realTeam": "BENZE BULLS"},
    {"id": 8, "name": "SACHIN SEN", "price": 17, "position": "FWD", "realTeam": "ZENITH ZEBRAS"},
    {"id": 9, "name": "SAKAR SUBEDI", "price": 7, "position": "FWD", "realTeam": "BENZE BULLS"},
    {"id": 10, "name": "SANDIL KATUWAL", "price": 4, "position": "FWD", "realTeam": "GODAR GOATS"},
    {"id": 11, "name": "SANJAYA ADHIKARI", "price": 4, "position": "FWD", "realTeam": "ACHARYA ATTACKERS"},
    {"id": 12, "name": "SANKALPA SHARMA", "price": 11, "position": "FWD", "realTeam": "JOSHI JAGUARS"},
    {"id": 13, "name": "SHRIJAN BHUSAL", "price": 15, "position": "FWD", "realTeam": "ZENITH ZEBRAS"},
    {"id": 14, "name": "SHUBHAM SINGH", "price": 12, "position": "FWD", "realTeam": "GODAR GOATS"},
    {"id": 15, "name": "SHUSHANT ADHIKARI", "price": 11, "position": "FWD", "realTeam": "JOSHI JAGUARS"},
    {"id": 16, "name": "SHYAM MAHATO", "price": 8, "position": "FWD", "realTeam": "GODAR GOATS"},
    {"id": 17, "name": "SUDIP BARAL", "price": 18, "position": "FWD", "realTeam": "BENZE BULLS"},
    {"id": 18, "name": "SUJIT GURUNG", "price": 10, "position": "FWD", "realTeam": "ZENITH ZEBRAS"},
    {"id": 19, "name": "SUMAN CHHETRI", "price": 15, "position": "FWD", "realTeam": "SOTI SOLDIERS"},
    {"id": 20, "name": "UNIQUE REGMI", "price": 6, "position": "FWD", "realTeam": "SOTI SOLDIERS"},
    {"id": 21, "name": "SUMAN SHARMA", "price": 5, "position": "FWD", "realTeam": "SOTI SOLDIERS"},
    {"id": 22, "name": "UDHAY THAKUR", "price": 9, "position": "FWD", "realTeam": "GODAR GOATS"},
    {"id": 23, "name": "SAJAN ROKAYA", "price": 4, "position": "DEF", "realTeam": "ZENITH ZEBRAS"},
    {"id": 24, "name": "SAMEER ACHARYA", "price": 18, "position": "DEF", "realTeam": "ACHARYA ATTACKERS"},
    {"id": 25, "name": "SAMIR GODAR", "price": 18, "position": "DEF", "realTeam": "GODAR GOATS"},
    {"id": 26, "name": "SANTOSH JOSHI", "price": 18, "position": "DEF", "realTeam": "JOSHI JAGUARS"},
    {"id": 27, "name": "SUJAL PARAJULI", "price": 17, "position": "DEF", "realTeam": "JOSHI JAGUARS"},
    {"id": 28, "name": "SUJAL SOTI", "price": 18, "position": "DEF", "realTeam": "SOTI SOLDIERS"},
    {"id": 29, "name": "SUJAN BHAATTA", "price": 10, "position": "DEF", "realTeam": "SOTI SOLDIERS"},
    {"id": 30, "name": "SUSHAN PANDEY", "price": 7, "position": "DEF", "realTeam": "ACHARYA ATTACKERS"},
    {"id": 31, "name": "SWORNIM TIMILSINA", "price": 13, "position": "DEF", "realTeam": "ACHARYA ATTACKERS"},
    {"id": 32, "name": "VIVEK GAUTAM", "price": 12, "position": "DEF", "realTeam": "ACHARYA ATTACKERS"},
    {"id": 33, "name": "ZENITH SARU", "price": 18, "position": "DEF", "realTeam": "ZENITH ZEBRAS"},
    {"id": 34, "name": "ANUJ THAPA", "price": 15, "position": "DEF", "realTeam": "BENZE BULLS"},
    {"id": 35, "name": "ANUPAM BISTA", "price": 7, "position": "FWD", "realTeam": "BENZE BULLS"},
    {"id": 36, "name": "TASHI SHERPA", "price": 10, "position": "FWD", "realTeam": "BENZE BULLS"},
]

# SHEET CONNECTION
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
st.markdown("**1 GK + 5 DEF/FWD**")

BUDGET = 60
team_name = st.text_input("🏷️ **Team Name**")
owner_name = st.text_input("👤 **Your Name**")

# Session state
if 'selected_gk' not in st.session_state: st.session_state.selected_gk = []
if 'selected_fwd' not in st.session_state: st.session_state.selected_fwd = []
if 'selected_def' not in st.session_state: st.session_state.selected_def = []
if 'show_captain_select' not in st.session_state: st.session_state.show_captain_select = False
if 'team_players' not in st.session_state: st.session_state.team_players = []

# Check captain status
all_selected = st.session_state.selected_gk + st.session_state.selected_fwd + st.session_state.selected_def
has_captain_selected = any(' ⭐' in player for player in all_selected)

# POSITION COLUMNS
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("### 🧤 **GK (REQUIRED)**")
    gk_options = [f"{p['name']} (₹{p['price']}{' ⭐' if p.get('iscaptain', False) else ''})" 
                  for p in PLAYERS if p['position'] == 'GK']
    new_gk = st.multiselect("GK", gk_options, default=st.session_state.selected_gk, max_selections=1)
    st.session_state.selected_gk = new_gk

with col2:
    st.markdown("### ⚽ **FWD**")
    fwd_options = []
    def_count = len(st.session_state.selected_def)
    max_fwd = min(5 - def_count, 4)
    
    for p in PLAYERS:
        if p['position'] == 'FWD' and not (p.get('iscaptain', False) and has_captain_selected):
            fwd_options.append(f"{p['name']} (₹{p['price']}{' ⭐' if p.get('iscaptain', False) else ''})")
    
    st.caption(f"Max: {max_fwd}")
    new_fwd = st.multiselect("FWD", fwd_options, default=st.session_state.selected_fwd, max_selections=max_fwd)
    st.session_state.selected_fwd = new_fwd

with col3:
    st.markdown("### 🛡️ **DEF**")
    def_options = []
    fwd_count = len(st.session_state.selected_fwd)
    max_def = min(5 - fwd_count, 3)
    
    for p in PLAYERS:
        if p['position'] == 'DEF' and not (p.get('iscaptain', False) and has_captain_selected):
            def_options.append(f"{p['name']} (₹{p['price']}{' ⭐' if p.get('iscaptain', False) else ''})")
    
    st.caption(f"Max: {max_def}")
    new_def = st.multiselect("DEF", def_options, default=st.session_state.selected_def, max_selections=max_def)
    st.session_state.selected_def = new_def

# Update calculations
all_selected = st.session_state.selected_gk + st.session_state.selected_fwd + st.session_state.selected_def
captain_count = len([p for p in all_selected if ' ⭐' in p])
def_fwd_total = len(st.session_state.selected_fwd) + len(st.session_state.selected_def)
total_price = sum(int(p.split("₹")[1].split('⭐')[0].strip(")")) for p in all_selected) if all_selected else 0

# METRICS
col1, col2, col3, col4, col5 = st.columns(5)
col1.metric("Total", len(all_selected), "6")
col2.metric("GK", len(st.session_state.selected_gk), "1")
col3.metric("DEF+FWD", def_fwd_total, "5")
col4.metric("Captain", captain_count, "0-1")
col5.metric("Budget", f"₹{total_price}", "₹60")

is_valid = (len(st.session_state.selected_gk) == 1 and def_fwd_total == 5 and len(all_selected) == 6 and total_price <= BUDGET)

if is_valid:
    st.success("✅ **READY TO SAVE!**")
else:
    st.warning("⚠️ **Fix selection**")

# TEAM LIST
if all_selected:
    st.markdown("### 📋 **Your Team:**")
    for player in all_selected:
        captain_emoji = " ⭐ **(C)**" if ' ⭐' in player else ""
        st.write(f"• {player.replace(' ⭐', '')}{captain_emoji}")

# SAVE BUTTON - Opens Captain Selection
if st.button("💾 **SAVE TEAM + SET CAPTAIN**", type="primary", use_container_width=True):
    def_fwd_total = len(st.session_state.selected_fwd) + len(st.session_state.selected_def)
    
    if not team_name.strip() or not owner_name.strip():
        st.error("❌ Team Name & Owner required!")
    elif len(st.session_state.selected_gk) != 1:
        st.error("❌ 1 GK REQUIRED!")
    elif def_fwd_total != 5:
        st.error(f"❌ Need 5 DEF+FWD! (Have {def_fwd_total})")
    elif total_price > BUDGET:
        st.error(f"❌ Over budget: ₹{total_price}")
    else:
        # Store team data for captain selection
        st.session_state.team_players = []
        for sel in all_selected:
            name = sel.split(" (")[0].replace(' ⭐', '')
            player = next(p for p in PLAYERS if p["name"] == name)
            st.session_state.team_players.append({
                'name': player['name'],
                'position': player['position'],
                'realTeam': player['realTeam']
            })
        st.session_state.team_name = team_name.strip()
        st.session_state.owner_name = owner_name.strip()
        st.session_state.total_price = total_price
        st.session_state.show_captain_select = True

# CAPTAIN SELECTION MODAL - FIXED
if st.session_state.get('show_captain_select', False):
    st.markdown("---")
    st.markdown("### 👑 **SELECT CAPTAIN**")
    
    team_players = st.session_state.team_players
    captain_options = [p['name'] for p in team_players]
    
    selected_captain = st.selectbox("**Captain** (2x points):", captain_options, key="captain_select")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("✅ **SAVE TEAM + CAPTAIN**", type="primary"):
            try:
                worksheet = get_sheet()
                
                # Prepare data with CAPTAIN NAME (not star)
                team_players_str = ", ".join([p['name'] for p in team_players])
                positions_str = ", ".join([p['position'] for p in team_players])
                real_teams_str = ", ".join([p['realTeam'] for p in team_players])
                
                # CAPTAIN NAME saved directly
                captain_name = selected_captain
                
                worksheet.append_row([
                    st.session_state.team_name,
                    st.session_state.total_price,
                    team_players_str,
                    positions_str,
                    real_teams_str,
                    captain_name,  # CAPTAIN NAME SAVED HERE
                    datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    st.session_state.owner_name
                ])
                
                st.success(f"🎉 **TEAM SAVED! Captain: {captain_name}**")
                st.balloons()
                
                # Reset everything
                for key in ['selected_gk', 'selected_fwd', 'selected_def', 'show_captain_select', 
                           'team_players', 'team_name', 'owner_name', 'total_price']:
                    if key in st.session_state:
                        del st.session_state[key]
                st.rerun()
                
            except Exception as e:
                st.error(f"❌ {str(e)}")
    
    with col2:
        if st.button("❌ **Cancel**"):
            for key in ['show_captain_select', 'team_players', 'team_name', 'owner_name', 'total_price']:
                if key in st.session_state:
                    del st.session_state[key]
            st.rerun()
