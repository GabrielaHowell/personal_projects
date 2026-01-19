# ===================== IMPORTS =====================
import os
import re
import base64
import requests
import streamlit as st
import spotipy
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

from spotipy.oauth2 import SpotifyOAuth
from collections import Counter
# ==================================================
st.cache_data.clear()
st.cache_resource.clear()


# ===================== SECRETS → ENV =====================
# MUST COME BEFORE ANY getenv()
if "SPOTIPY_CLIENT_ID" in st.secrets:
    os.environ["SPOTIPY_CLIENT_ID"] = st.secrets["SPOTIPY_CLIENT_ID"]
    os.environ["SPOTIPY_CLIENT_SECRET"] = st.secrets["SPOTIPY_CLIENT_SECRET"]
    os.environ["SPOTIPY_REDIRECT_URI"] = st.secrets["SPOTIPY_REDIRECT_URI"]

CLIENT_ID = os.getenv("SPOTIPY_CLIENT_ID")
CLIENT_SECRET = os.getenv("SPOTIPY_CLIENT_SECRET")
REDIRECT_URI = os.getenv("SPOTIPY_REDIRECT_URI")

SCOPE = "playlist-read-private playlist-read-collaborative"

if not all([CLIENT_ID, CLIENT_SECRET, REDIRECT_URI]):
    st.error("🚨 Spotify API credentials not loaded. Check Streamlit secrets.")
    st.stop()
# =========================================================


# ===================== SPOTIFY AUTH =====================
def get_spotify_client():
    auth = SpotifyOAuth(
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        redirect_uri=REDIRECT_URI,
        scope=SCOPE,
        cache_path=".spotifycache",
        open_browser=False
    )

    # OAuth callback
    if "code" in st.query_params:
        auth.get_access_token(st.query_params["code"])
        st.query_params.clear()
        st.rerun()

    token = auth.get_cached_token()
    if not token:
        st.link_button("🔐 Login with Spotify", auth.get_authorize_url())
        st.stop()

    return spotipy.Spotify(auth=token["access_token"])


sp = get_spotify_client()
# =========================================================


# ===================== DATA FUNCTIONS =====================
@st.cache_data(show_spinner=False)
def get_playlist_metadata_with_ids(playlist_id, source):
    tracks, results = [], sp.playlist_tracks(
        playlist_id,
        fields="items.track.id,items.track.name,items.track.artists,items.track.popularity,next",
        market="US" #added recently because streamlit was missing this parameter
    )

    while results:
        tracks.extend(results["items"])
        results = sp.next(results) if results.get("next") else None

    data = []
    for item in tracks:
        track = item.get("track")
        if track and track.get("id"):
            artist = track["artists"][0]
            data.append({
                "track_name": track["name"],
                "artist": artist["name"],
                "artist_id": artist["id"],
                "popularity": track["popularity"],
                "track_id": track["id"],
                "Source": source
            })

    return pd.DataFrame(data)


@st.cache_data(show_spinner=False)
def get_genres_for_artists(artist_ids):
    genre_map = {}
    for i in range(0, len(artist_ids), 50):
        batch = artist_ids[i:i + 50]
        for a in sp.artists(batch)["artists"]:
            genre_map[a["id"]] = a["genres"] if a["genres"] else ["Unknown"]
    return genre_map
# =========================================================


# ===================== UI HEADER =====================
LOGO_URL = "https://storage.googleapis.com/pr-newsroom-wp/1/2018/11/Spotify_Logo_CMYK_Green.png"
logo = base64.b64encode(requests.get(LOGO_URL).content).decode()

st.markdown(f"""
<style>
.logo {{ width:120px; margin-bottom:-20px; }}
.title {{ font-size:2.4rem; font-weight:700; color:#1DB954; }}
.sub {{ font-size:1.1rem; }}
</style>
<img class="logo" src="data:image/png;base64,{logo}">
<div class="title">Gabs Spotify Wrapped 🎧</div>
<div class="sub">Compare your playlist vs mine vs global hits</div>
""", unsafe_allow_html=True)

st.divider()
# =========================================================


# ===================== INPUT =====================
def extract_playlist_id(text):
    match = re.search(r"playlist/([a-zA-Z0-9]+)", text)
    return match.group(1) if match else text.strip()


GLOBAL_ID = "4bW0GSFWFWqOjWmkHII7aw"
MY_ID = "6i0LNQ0QCzlFGx2lZXxSdj"

playlist_input = st.text_input("🔗 Paste a Spotify playlist link or ID")

if st.button("▶ Analyze"):
    playlist_id = extract_playlist_id(playlist_input)

    with st.spinner("Fetching Spotify data…"):
        df_user = get_playlist_metadata_with_ids(playlist_id, "Your Playlist")
        df_global = get_playlist_metadata_with_ids(GLOBAL_ID, "Global 2025")
        df_my = get_playlist_metadata_with_ids(MY_ID, "My Playlist")
# =========================================================


# ===================== ANALYSIS =====================
    st.header("🪞 Your Playlist Snapshot")
    c1, c2, c3 = st.columns(3)
    c1.metric("Tracks", len(df_user))
    c2.metric("Avg Popularity", f"{df_user.popularity.mean():.1f}")
    c3.metric("Max Popularity", df_user.popularity.max())

    st.subheader("🔥 Top Songs")
    st.dataframe(df_user.nlargest(5, "popularity")[["track_name", "artist", "popularity"]])

    # Genres
    genre_map = get_genres_for_artists(df_user.artist_id.unique())
    df_user["genres"] = df_user.artist_id.map(genre_map)
    flat_genres = [g for lst in df_user.genres for g in lst]
    top_genres = Counter(flat_genres).most_common(5)

    st.subheader("🎧 Top Genres")
    st.write(dict(top_genres))

    # KDE
    st.subheader("📊 Popularity Distribution")
    combined = pd.concat([df_user, df_global, df_my])
    plt.figure(figsize=(10,4))
    sns.kdeplot(data=combined, x="popularity", hue="Source", fill=True)
    st.pyplot(plt)
# =========================================================


# ===================== SIDEBAR =====================
st.sidebar.info(
    "1. Open a Spotify playlist\n"
    "2. Copy the link\n"
    "3. Paste it above\n\n"
    "Playlist must be public."
)
# =========================================================
