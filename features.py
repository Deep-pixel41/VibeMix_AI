import sqlite3
import streamlit as st
from datetime import datetime

# ==========================================
# DATABASE LOGIC (SQLite)
# ==========================================

def init_db():
    """Creates the local database and table if it doesn't exist."""
    conn = sqlite3.connect('vibe_history.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            mood TEXT,
            timestamp TEXT,
            playlist_url TEXT
        )
    ''')
    conn.commit()
    conn.close()

def save_to_history(mood, playlist_url):
    """Inserts a new generated playlist into the database."""
    conn = sqlite3.connect('vibe_history.db')
    cursor = conn.cursor()
    timestamp = datetime.now().strftime("%Y-%m-%d %I:%M %p") # e.g., 2026-05-09 03:30 PM
    
    cursor.execute('INSERT INTO history (mood, timestamp, playlist_url) VALUES (?, ?, ?)', 
                   (mood, timestamp, playlist_url))
    conn.commit()
    conn.close()

# ==========================================
# UI COMPONENTS
# ==========================================

def display_sidebar_history():
    """Fetches the last 5 playlists from the database and puts them in the sidebar."""
    st.sidebar.title("🕰️ Vibe History")
    
    conn = sqlite3.connect('vibe_history.db')
    cursor = conn.cursor()
    # Fetch the most recent 5 entries
    cursor.execute('SELECT mood, timestamp, playlist_url FROM history ORDER BY id DESC LIMIT 5')
    rows = cursor.fetchall()
    conn.close()
    
    if not rows:
        st.sidebar.info("No history yet. Generate your first playlist!")
    else:
        for row in rows:
            mood, timestamp, url = row
            st.sidebar.caption(f"**{timestamp}**")
            st.sidebar.write(f"*{mood}*")
            st.sidebar.markdown(f"[🎧 Listen on Spotify]({url})")
            st.sidebar.divider()

def display_album_gallery(track_details):
    """Takes track data and builds a 5-column grid for album art."""
    st.write("### 🖼️ Up Next...")
    
    # Create 5 columns in Streamlit
    cols = st.columns(5)
    
    for index, track in enumerate(track_details):
        # The modulo operator (%) assigns each track to columns 0, 1, 2, 3, 4, then repeats
        col = cols[index % 5] 
        with col:
            if track['image_url']:
                st.image(track['image_url'], use_container_width=True)
            # Display title, cut off at 20 characters so it doesn't break the layout
            st.caption(f"**{track['title'][:20]}**")