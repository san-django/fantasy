import streamlit as st
import pandas as pd
from datetime import datetime
from google.oauth2 import service_account
import gspread

# COMPLETE 36 PLAYERS LIST
PLAYERS = [
    {"id": 1, "name": "ROJIT SHRESTHA", "price": 8, "position": "GK", "realTeam": "JOSHI JAGUARS",},
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

# TABS
tab1, tab2 = st.tabs(["📝 Build Team", "👑 Set Captain"])

# TAB 1: BUILD TEAM
with tab1:
    st.markdown("**1 GK + 5 DEF/FWD + Max 1 Captain**")
    
    BUDGET = 100
    team_name = st.text_input("🏷️ **Team Name**")
    owner_name = st.text_input("👤 **Your Name**")

    # Initialize session state
    if 'selected_gk' not in st.session_state: st.session_state.selected_gk = []
    if 'selected_fwd' not in st.session_state: st.session_state.selected_fwd = []
    if 'selected_def' not in st.session_state: st.session_state.selected_def = []

    # Check if captain already selected
    all_selected = st.session_state.selected_gk + st.session_state.selected_fwd + st.session_state.selected_def
    has_captain_selected = any(' ⭐' in player for player in all_selected)

    # POSITION COLUMNS
    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("### 🧤 **GK (1 REQUIRED)**")
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
            if p['position'] == 'FWD':
                if p.get('iscaptain', False) and has_captain_selected: continue
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
            if p['position'] == 'DEF':
                if p.get('iscaptain', False) and has_captain_selected: continue
                def_options.append(f"{p['name']} (₹{p['price']}{' ⭐' if p.get('iscaptain', False) else ''})")
        
        st.caption(f"Max: {max_def}")
        new_def = st.multiselect("DEF", def_options, default=st.session_state.selected_def, max_selections=max_def)
        st.session_state.selected_def = new_def

    # Update selections
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
    col5.metric("Budget", f"₹{total_price}", "₹100")

    st.info(f"FWD max={min(5-len(st.session_state.selected_def),4)} | DEF max={min(5-len(st.session_state.selected_fwd),3)} | Captains: {captain_count}/1")

    is_valid = (len(st.session_state.selected_gk) == 1 and def_fwd_total == 5 and len(all_selected) == 6 and total_price <= BUDGET)

    if is_valid:
        st.success("✅ **READY TO SAVE!**")
    else:
        st.warning("⚠️ **Fix selection**")

    # YOUR TEAM
    if all_selected:
        st.markdown("### 📋 **Your Team:**")
        for player in all_selected:
            captain_emoji = " ⭐ **(C)**" if ' ⭐' in player else ""
            st.write(f"• {player.replace(' ⭐', '')}{captain_emoji}")

    # SAVE
    if st.button("💾 **SAVE TEAM**", type="primary", use_container_width=True):
        def_fwd_total = len(st.session_state.selected_fwd) + len(st.session_state.selected_def)
        if not team_name.strip() or not owner_name.strip():
            st.error("❌ Team Name & Owner required!")
        elif len(st.session_state.selected_gk) != 1:
            st.error("❌ 1 GK REQUIRED!")
        elif def_fwd_total != 5:
            st.error(f"❌ Need 5 DEF+FWD! (Have {def_fwd_total})")
        elif captain_count > 1:
            st.error("❌ Only 1 Captain allowed!")
        elif total_price > BUDGET:
            st.error(f"❌ Over budget: ₹{total_price}")
        else:
            try:
                worksheet = get_sheet()
                team_players = []
                positions = []
                real_teams = []
                captains = []
                for sel in all_selected:
                    name = sel.split(" (")[0].replace(' ⭐', '')
                    player = next(p for p in PLAYERS if p["name"] == name)
                    team_players.append(player['name'])
                    positions.append(player['position'])
                    real_teams.append(player['realTeam'])
                    captains.append("⭐" if player.get('iscaptain', False) else "")
                
                worksheet.append_row([
                    team_name.strip(),
                    total_price,
                    ", ".join(team_players),
                    ", ".join(positions),
                    ", ".join(real_teams),
                    "",  # Captain column - set later
                    datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    owner_name.strip()
                ])
                
                st.success(f"🎉 **SAVED!** 1-{len(st.session_state.selected_fwd)}-{len(st.session_state.selected_def)} | {captain_count}⭐")
                st.balloons()
                st.rerun()
            except Exception as e:
                st.error(f"❌ {str(e)}")

# TAB 2: SET CAPTAIN FOR SAVED TEAMS (FPL STYLE)
with tab2:
    st.markdown("### 👑 **SET CAPTAIN FOR SAVED TEAM**")
    
    try:
        worksheet = get_sheet()
        records = worksheet.get_all_records()
        
        if not records:
            st.info("👆 **Save teams first in Build Team tab!**")
        else:
            # Team selector
            team_options = [f"{row['Team']} - {row['Owner']}" for row in records]
            selected_team_idx = st.selectbox("Select saved team:", range(len(team_options)), 
                                           format_func=lambda i: team_options[i])
            
            selected_team = records[selected_team_idx]
            team_players = selected_team['Players'].split(', ')
            
            st.markdown(f"### 📋 **{selected_team['Team']}**")
            st.caption(f"Owner: {selected_team['Owner']} | Budget: ₹{selected_team['Price']}")
            
            # Show team in columns
            cols = st.columns(3)
            for i, player in enumerate(team_players):
                with cols[i % 3]:
                    st.write(f"• {player}")
            
            # CAPTAIN SELECTION
            st.markdown("---")
            st.markdown("### 👑 **CHOOSE CAPTAIN**")
            
            captain_options = team_players
            selected_captain = st.selectbox("**Captain** (2x points):", captain_options, index=0)
            
            vice_options = ["None"] + [p for p in team_players if p != selected_captain]
            selected_vice = st.selectbox("**Vice-Captain** (backup):", vice_options, index=0)
            
            if st.button("✅ **SET CAPTAIN**", type="primary"):
                try:
                    row_num = selected_team_idx + 2  # +2 for header
                    
                    # Update Captain column (column F = index 6)
                    worksheet.update(f'F{row_num}', f"{selected_captain}|{selected_vice if selected_vice != 'None' else ''}")
                    
                    st.success("🎉 **Captain Updated!**")
                    st.balloons()
                    st.rerun()
                except Exception as e:
                    st.error(f"❌ {str(e)}")
            
            # Show recent captain changes
            st.markdown("---")
            st.markdown("### 📊 **RECENT CAPTAINS**")
            df = pd.DataFrame(records.tail(10))
            if 'Captains' in df.columns:
                st.dataframe(df[['Team', 'Owner', 'Captains']], use_container_width=True)
            else:
                st.info("Captain column will appear after first captain set!")
                
    except Exception as e:
        st.error(f"❌ {str(e)}")
