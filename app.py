import streamlit as st
import os
import json
from groq import Groq
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv

# Import our custom module!
import features

load_dotenv()

# Initialize DB
features.init_db()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id=os.getenv("SPOTIPY_CLIENT_ID"),
    client_secret=os.getenv("SPOTIPY_CLIENT_SECRET"),
    redirect_uri=os.getenv("SPOTIPY_REDIRECT_URI"),
    scope="playlist-modify-public playlist-modify-private user-read-email",
))

def get_recommendations_from_groq(mood):
    prompt = f"The user is feeling: '{mood}'. Suggest 10 songs that match this vibe. Return ONLY a JSON object with a key 'songs' containing a list of objects with 'title' and 'artist'."
    try:
        completion = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[{"role": "user", "content": prompt}],
            response_format={"type": "json_object"}
        )
        return json.loads(completion.choices[0].message.content).get("songs", [])
    except Exception as e:
        st.error(f"Error calling Groq: {e}")
        return []

def search_tracks(songs):
    """Searches Spotify and extracts the URI, Name, and Album Art URL."""
    track_details = []
    
    for song in songs:
        try:
            query = f"{song.get('title', '')} {song.get('artist', '')}"
            results = sp.search(q=query, type="track", limit=1)
            items = results['tracks']['items']
            
            if items:
                track = items[0]
                # Spotify returns images in an array [Large, Medium, Small]
                # We grab the first one (Large) safely
                images = track['album']['images']
                img_url = images[0]['url'] if images else None
                
                track_details.append({
                    'uri': track['uri'],
                    'title': track['name'],
                    'artist': track['artists'][0]['name'],
                    'image_url': img_url
                })
        except Exception as e:
            pass # Skip if not found
            
    return track_details

def create_playlist(mood, track_uris):
    """Takes pre-searched URIs and builds the playlist."""
    try:
        playlist = sp.current_user_playlist_create(
            name=f"Mood: {mood[:20]}...",
            public=False,
            collaborative=False,
            description=f"AI-generated playlist for: {mood}"
        )
        sp.playlist_add_items(playlist_id=playlist['id'], items=track_uris)
        return playlist['external_urls']['spotify']
    except Exception as e:
        st.error(f"Error building playlist: {e}")
        return None

# ==========================================
# STREAMLIT UI
# ==========================================
st.set_page_config(page_title="VibeMix AI", page_icon="🎧", layout="wide")

# Call the sidebar from our features module
features.display_sidebar_history()

st.title("🎧 VibeMix AI")
st.subheader("Turn your feelings into a Spotify Playlist")

user_input = st.text_area("How are you feeling?")

if st.button("Generate My Playlist"):
    if not user_input:
        st.warning("Please describe your mood first!")
    else:
        # 1. Get Songs from Groq
        with st.spinner("🤖 Groq is analyzing your vibe..."):
            song_list = get_recommendations_from_groq(user_input)

        if song_list:
            # 2. Find tracks and images on Spotify
            with st.spinner("🔍 Fetching Album Art..."):
                track_details = search_tracks(song_list)
                track_uris = [track['uri'] for track in track_details]
            
            if track_uris:
                # 3. Show the cool UI Grid
                features.display_album_gallery(track_details)
                
                # 4. Create Playlist
                with st.spinner("🎵 Building Playlist..."):
                    playlist_url = create_playlist(user_input, track_uris)
                
                if playlist_url:
                    # 5. Save to our SQLite Database
                    features.save_to_history(user_input, playlist_url)
                    
                    st.success("Playlist created successfully!")
                    st.balloons()
                    st.markdown(f"### [👉 Open Your Playlist on Spotify]({playlist_url})")
                    st.info("Check your sidebar to see this saved in your history!")
            else:
                st.error("No tracks found on Spotify.")