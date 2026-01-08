# -------------  imports  -------------
import base64, requests, streamlit as st, spotipy, pandas as pd, seaborn as sns, matplotlib.pyplot as plt, numpy as np, re, os
from spotipy.oauth2 import SpotifyOAuth
from collections import Counter
from matplotlib.ticker import MaxNLocator
# -------------------------------------


CLIENT_ID     = os.getenv("SPOTIPY_CLIENT_ID")
CLIENT_SECRET = os.getenv("SPOTIPY_CLIENT_SECRET")
REDIRECT_URI  = os.getenv("SPOTIPY_REDIRECT_URI")
SCOPE         = "user-library-read playlist-modify-private playlist-modify-public"

if "SPOTIPY_CLIENT_ID" in st.secrets:
    os.environ["SPOTIPY_CLIENT_ID"] = st.secrets["SPOTIPY_CLIENT_ID"]
    os.environ["SPOTIPY_CLIENT_SECRET"] = st.secrets["SPOTIPY_CLIENT_SECRET"]
    os.environ["SPOTIPY_REDIRECT_URI"] = st.secrets["SPOTIPY_REDIRECT_URI"]


@st.cache_resource(show_spinner=False)
def get_spotify_client():
    auth = SpotifyOAuth(client_id=CLIENT_ID, client_secret=CLIENT_SECRET,
                        redirect_uri=REDIRECT_URI, scope=SCOPE, cache_path=".cache-streamlit",
                        open_browser=False)
    if (code := st.query_params.get("code")):
        auth.get_access_token(code)
        st.query_params.clear(); st.rerun()
    if not (token := auth.get_cached_token()):
        st.link_button("🔐  Login with Spotify", auth.get_authorize_url())
        st.stop()
    return spotipy.Spotify(auth=token["access_token"])

sp = get_spotify_client()


@st.cache_data
def get_playlist_metadata_with_ids(playlist_id, name_suffix):
    st.info(f"--- Starting data pull for {name_suffix} ---")
    all_track_items, results = [], sp.playlist_tracks(
        playlist_id, fields='items.track.id,items.track.name,items.track.artists,items.track.popularity,next')
    while results:
        all_track_items.extend(results['items'])
        results = sp.next(results) if results.get('next') else None
    data = []
    for item in all_track_items:
        track = item.get('track')
        if track and track.get('id'):
            art = track['artists'][0] if track.get('artists') else {'name': 'Unknown', 'id': 'Unknown'}
            data.append({
                'track_name': track['name'],
                'artist': art['name'],
                'artist_id': art['id'],
                'popularity': track['popularity'],
                'Source': name_suffix,
                'track_id': track['id']
            })
    df = pd.DataFrame(data)
    st.success(f"✅ Retrieved {len(df)} tracks for {name_suffix}.")
    return df


@st.cache_data
def get_genres_for_artists(artist_ids):
    genres_map = {}
    for i in range(0, len(artist_ids), 50):
        batch = artist_ids[i:i + 50]
        try:
            for art in sp.artists(batch)['artists']:
                if art:
                    genres_map[art['id']] = art['genres'] if art['genres'] else ['Unknown Genre']
        except Exception:
            continue
    return genres_map


# -------------  PRETTY + USER-FIRST SUMMARY  -------------
LOGO_URL = "https://storage.googleapis.com/pr-newsroom-wp/1/2018/11/Spotify_Logo_CMYK_Green.png"
spoti_logo = base64.b64encode(requests.get(LOGO_URL).content).decode()

st.markdown(f"""
<style>
.logo{{width:130px;margin:-25px 0 -35px -8px;}}
.title{{font-size:2.6rem;color:#1DB954;font-weight:700;}}
.sub{{font-size:1.15rem;color:#191414;}}
.metric{{text-align:center;font-size:1.7rem;color:#1DB954;}}
</style>
<img class="logo" src="data:image/png;base64,{spoti_logo}">
""", unsafe_allow_html=True)

st.markdown('<div class="title">Gabs Spotify Wrapped 🎧</div>', unsafe_allow_html=True)
st.markdown('<div class="sub">Your personal playlist insights → vs. my playlist → vs. the world</div>', unsafe_allow_html=True)
st.write("")


def extract_playlist_id(inp):
    m = re.search(r'playlist/([a-zA-Z0-9]+)', inp)
    return m.group(1) if m else (inp if re.match(r'^[a-zA-Z0-9]{22}$', inp) else None)


USER_ID   = None
GLOBAL_ID = '4bW0GSFWFWqOjWmkHII7aw'
MY_ID     = '6i0LNQ0QCzlFGx2lZXxSdj'

with st.form("playlist_form"):
    c1, c2, c3 = st.columns([1, 3, 1])
    with c2:
        user_playlist_input = st.text_input("🔗  Paste your Spotify Playlist Link or ID:", value="")
        submitted = st.form_submit_button("▶️  Analyze", use_container_width=True)

if submitted and (USER_ID := extract_playlist_id(user_playlist_input)):
    with st.spinner("Fetching data from Spotify…"):
        df_user = get_playlist_metadata_with_ids(USER_ID,    'Your Playlist')
        df_glob = get_playlist_metadata_with_ids(GLOBAL_ID,  'Global 2025')
        df_my   = get_playlist_metadata_with_ids(MY_ID,      'My 2025 PL')

    # 1.  YOUR PERSONAL SUMMARY
    st.write(""); st.markdown("---")
    st.header("🪞  Your Playlist Snapshot")
    c1, c2, c3 = st.columns(3)
    c1.metric("Total tracks", len(df_user))
    c2.metric("Average popularity", f"{df_user['popularity'].mean():.1f}")
    c3.metric("Top popularity", f"{df_user['popularity'].max()}")

    st.subheader("🔥  Your Top 5 Most Popular Songs")
    for i, row in df_user.nlargest(5, 'popularity')[['track_name', 'artist', 'popularity']].iterrows():
        st.write(f"{i+1}. **{row['track_name']}** – {row['artist']}  (popularity {row['popularity']})")

    st.subheader("🎧  Your Top Genres")
    df_user['genres'] = df_user['artist_id'].map(get_genres_for_artists(df_user['artist_id'].unique()))
    user_genres = [g for sub in df_user['genres'].dropna() for g in sub]
    top_genres = dict(Counter(user_genres).most_common(5))
    cols = st.columns(5)
    for col, (genre, count) in zip(cols, top_genres.items()):
        col.metric(genre, count)

    # 2.  YOU vs. MY PLAYLIST
    st.markdown("---")
    st.header("⚖️  You vs. My Playlist")
    common_m = pd.merge(df_user, df_my, on='track_id', suffixes=('', '_my'))
    st.metric("Shared songs", len(common_m))
    if not common_m.empty:
        st.subheader("Songs we both have")
        for _, row in common_m.nlargest(5, 'popularity_my')[['track_name', 'artist', 'popularity_my']].iterrows():
            st.write(f"• **{row['track_name']}** – {row['artist']}  (pop {row['popularity_my']})")
    else:
        st.info("No overlap with my playlist – you’re unique!")

    df_my['genres'] = df_my['artist_id'].map(get_genres_for_artists(df_my['artist_id'].unique()))
    my_genres = [g for sub in df_my['genres'].dropna() for g in sub]
    shared_genre_cnt = len(set(user_genres) & set(my_genres))
    st.metric("Shared genres", shared_genre_cnt)

    # 3.  YOU vs. GLOBAL 2025
    st.markdown("---")
    st.header("🌍  You vs. Global 2025")
    common_g = pd.merge(df_user, df_glob, on='track_id', suffixes=('', '_glob'))
    st.metric("Shared with Global", len(common_g))
    if not common_g.empty:
        st.subheader("Your songs that are world hits")
        for _, row in common_g.nlargest(5, 'popularity_glob')[['track_name', 'artist', 'popularity_glob']].iterrows():
            st.write(f"• **{row['track_name']}** – {row['artist']}  (global pop {row['popularity_glob']})")
    else:
        st.info("You’re discovering outside the mainstream – nice!")

    pop_diff = df_user['popularity'].mean() - df_glob['popularity'].mean()
    st.metric("Average popularity vs. Global", f"{pop_diff:+.1f}  points")

    # 4.  BIG-PICTURE KDE CHARTS
    st.markdown("---")
    st.header("📊  Big Picture Charts")

    # smooth KDE popularity curves
    st.subheader("Popularity Distribution (smooth KDE)")
    df_comp = pd.concat([df_user, df_glob, df_my], ignore_index=True)
    plt.figure(figsize=(11, 4))
    for source, colour in zip(['Your Playlist', 'Global 2025', 'My 2025 PL'], ['#1DB954', '#FF6060', '#4B8BF5']):
        subset = df_comp[df_comp['Source'] == source]['popularity']
        sns.kdeplot(subset, fill=True, alpha=0.4, linewidth=1.8, label=source, color=colour)
    plt.xlabel("Popularity Score"); plt.ylabel("Density"); plt.title("Kernel Density Estimate (KDE)")
    plt.legend(); plt.tight_layout()
    st.pyplot(plt)

    # jaccard heat-map
    st.subheader("Artist Similarity Heat-map")
    labels = ['Your Playlist', 'Global 2025', 'My 2025 PL']
    sets   = [set(df_user['artist']), set(df_glob['artist']), set(df_my['artist'])]
    jac = pd.DataFrame(index=labels, columns=labels, dtype=float)
    for i, s1 in enumerate(sets):
        for j, s2 in enumerate(sets):
            jac.iloc[i, j] = len(s1 & s2) / len(s1 | s2) if len(s1 | s2) else 0.0
    mask = np.zeros_like(jac, dtype=bool); mask[np.diag_indices_from(mask)] = True
    plt.figure(figsize=(4, 3))
    sns.heatmap(jac, mask=mask, annot=True, fmt=".2f", cmap='Greens', square=True, linewidths=1, cbar_kws={"shrink": .6})
    plt.title("Similarity (artists)")
    st.pyplot(plt)

st.sidebar.subheader("How to use this app")
st.sidebar.markdown("1. Open the playlist on Spotify.")
st.sidebar.markdown("2. Click **Share → Copy link**.")
st.sidebar.markdown("3. Paste above and click **Analyze Playlists**.")
st.sidebar.warning("Playlist must be public.")
