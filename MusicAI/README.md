# 🎧 Spotify Wrapped Analytics (Streamlit App)

## 📌 Overview
An **interactive Spotify analytics web app** built with **Python**, **Streamlit**, and the **Spotify Web API**.  
Compare your own playlist to **my curated 2025 playlist** and the **Spotify Global 2025 charts**, and explore **trends, popularity metrics, genre overlap, and artist similarity** in a fun and visual way.

**Try it live here:** [https://gabspotify2025.streamlit.app](https://gabspotify2025.streamlit.app)

---

<p align="center">
  <img src="https://media.giphy.com/media/3o7TKU8RvQuomFfUUU/giphy.gif" alt="Spotify Analytics" width="400">
</p>

---

## 📂 Repository Contents

- **`app.py`** – Main Streamlit application  
- **`spotify_utils.py`** – Playlist metadata extraction, genre mapping, and analysis functions  
- **`visualizations.py`** – KDE plots, genre breakdowns, and artist overlap heatmaps  
- **OAuth Integration** – Spotipy-based Spotify authentication  

---

## 🗃️ Data Sources

- **Spotify Web API** – Track metadata, artist information, popularity scores  
- **User-provided Spotify Playlists** (public only)  
- **Spotify Global 2025 Charts**  

---

## ⚙️ Setup Instructions

### 🌐 Step 0 – Create a Streamlit Account & Playground

1️⃣ Go to [Streamlit Cloud](https://streamlit.io/cloud) and **sign up** (GitHub login recommended).  
2️⃣ Click **“New App”** to create your playground. This will let you **deploy your app and set secrets** securely.  
3️⃣ Make note of your app URL; you will need it as the **Redirect URI** in Spotify Developer settings.  

---

### 🛠️ Step 1 – Test Locally on Your Computer

1️⃣ **Clone the repository**  

```bash
git clone https://github.com/your-username/spotify-wrapped-streamlit.git
cd spotify-wrapped-streamlit
````

2️⃣ **Create and activate a virtual environment**

```bash
# Mac / Linux
python -m venv venv
source venv/bin/activate

# Windows
python -m venv venv
venv\Scripts\activate
```

3️⃣ **Install dependencies**

```bash
pip install -r requirements.txt
```

---

### 🔐 Step 2 – Spotify API Configuration

1️⃣ **Create a Spotify Developer App**
[Spotify Developer Dashboard](https://developer.spotify.com/dashboard)

2️⃣ **Add Redirect URIs**

```
http://127.0.0.1:8501/callback       # For local testing
https://<your-streamlit-app>.streamlit.app/callback  # For deployment
```

3️⃣ **Set environment variables** (or create a `.env` file)

```env
SPOTIPY_CLIENT_ID=your_client_id
SPOTIPY_CLIENT_SECRET=your_client_secret
SPOTIPY_REDIRECT_URI=http://127.0.0.1:8501/callback
```

> ⚠️ Never commit API credentials to GitHub.

---

### ▶️ Step 3 – Run Locally

```bash
streamlit run app.py
```

The app will open automatically at:
[http://localhost:8501](http://localhost:8501)

---

### 🌐 Step 4 – Deploy to Streamlit Cloud

1️⃣ **Push your repo to GitHub**

```bash
git add .
git commit -m "Initial commit"
git push origin main
```

2️⃣ **Log in to Streamlit Cloud** and create a new app (playground)
3️⃣ **Connect your GitHub repository**
4️⃣ **Set your secrets** in Streamlit (client ID, secret, redirect URI)
5️⃣ **Deploy** and access your app at your Streamlit URL

> Make sure the **Redirect URI for Streamlit** matches what you set in Spotify Developer Dashboard.

---

## 🎯 How to Use the App

1️⃣ Log in with Spotify (OAuth)
2️⃣ Paste a **public Spotify playlist link or ID**
3️⃣ Click **Analyze**
4️⃣ Explore insights including:

* Playlist popularity trends
* Top genres
* Shared artists and tracks
* Popularity comparisons vs. Global 2025

> ⚠️ Only **public playlists** can be analyzed.

---

## 📊 Key Features

* 🎵 Playlist Popularity Analysis
* 🎧 Genre Distribution & Comparison
* 📈 Kernel Density Estimates (KDE) for popularity
* 🤝 Artist & Track Overlap Metrics
* 🔐 Secure OAuth Authentication
* ⚡ Cached API calls for faster performance

---

## 🚀 Skills Demonstrated

* Python (Pandas, NumPy, Matplotlib, Seaborn)
* API Integration & OAuth (Spotify Web API, Spotipy)
* Streamlit App Development
* Data Visualization & Statistical Analysis
* User-centric UX design
* Secure credential handling

---

## 🔮 Future Enhancements

* Spotify Wrapped-style yearly summaries
* Audio feature analysis (danceability, energy, valence)
* Exportable insights (CSV / PDF)
* Enhanced interactivity & playlist comparisons

---

## 📎 Notes

* Spotify playlists must be **public** to fetch data
* OAuth tokens are **cached locally** to avoid repeated logins
* Built for **interactive analytics, API mastery, and music data storytelling**
