# 🎧 Spotify Wrapped Analytics (Streamlit App)

## 📌 Overview
An interactive **Spotify analytics web app** built with **Python**, **Streamlit**, and the **Spotify Web API**.  
Users can analyze a personal playlist and compare it against:

- My curated playlist  
- Spotify Global 2025 charts  

The app highlights **listening trends, popularity metrics, genre overlap, and artist similarity**.

---

# <p align="center"> <img src="https://media.giphy.com/media/3o7TKU8RvQuomFfUUU/giphy.gif" alt="Spotify Analytics"> </p>

# 📂 Contents


 📄 Streamlit App (app.py) – Main application file
 
 📊 Data Analysis Functions – Playlist metadata, genre extraction, popularity metrics
 
 📈 Visualizations – KDE plots, genre breakdowns, artist overlap heatmaps
 
 🗂️ Spotify OAuth Integration – Secure authentication using Spotipy
 

 
---
# 🗃️ Data Sources

 📌 Spotify Web API – Track metadata, artist information, popularity scores
 
 📌 User-provided Spotify Playlists (public playlists only)
 
 📌 Spotify Global 2025 Charts
 


⚙️ Setup Instructions

🛠️ Local Environment Setup

---
# 1️⃣ Clone the repository:

 git clone https://github.com/your-username/spotify-wrapped-streamlit.git
 
 cd spotify-wrapped-streamlit
 
#
# 2️⃣ Create and activate a virtual environment (recommended):
 python -m venv venv
 
 source venv/bin/activate  # Mac/Linux
 
 venv\\Scripts\\activate     # Windows
 
#
#  3️⃣ Install dependencies:

 pip install -r requirements.txt
 
---
#  🔐 Spotify API Configuration


 1️⃣ Create a Spotify Developer App
 
 🔗 https://developer.spotify.com/dashboard
 
#

 2️⃣ Add the following Redirect URI:
 
 http://127.0.0.1:8501/callback
 
#

 3️⃣ Create a .env file (or set environment variables):
 
 SPOTIPY\_CLIENT\_ID=your\_client\_id
 SPOTIPY\_CLIENT\_SECRET=your\_client\_secret
 SPOTIPY\_REDIRECT\_URI=http://127.0.0.1:8501/callback
 
 ⚠️ Never commit API keys to GitHub


 ▶️ Run the App
 streamlit run app.py
 The app will open automatically at:
 http://localhost:8501
 
---
# 🎯 How to Use the App

 1️⃣ Log in with Spotify (OAuth)
 
 2️⃣ Paste a public Spotify playlist link or ID
 
 3️⃣ Click Analyze
 
 4️⃣ Explore insights including:
 
  Playlist popularity trends
 
  Top genres
 
  Shared artists and tracks
 
  Popularity comparisons vs. Global 2025
  
---
# 📊 Key Features

 🎵 Playlist Popularity Analysis
 
 🎧 Genre Distribution \& Comparison
 
 📈 Kernel Density Estimates (KDE)
 
 🤝 Artist \& Track Overlap Metrics
 
 🔐 Secure OAuth Authentication
 
 ⚡ Cached API calls for performance
 
---
# 🚀 Skills Demonstrated

 Python (Pandas, NumPy, Matplotlib, Seaborn)
 
 API Integration \& OAuth (Spotify Web API, Spotipy)
 
 Streamlit App Development
 
 Data Visualization \& Statistical Analysis
 
 User-centric UX design
 
 Secure credential handling
 
---
# 🔮 Future Enhancements

Spotify Wrapped-style yearly summaries

Audio feature analysis (danceability, energy, valence)

Deployment via Streamlit Cloud

User exportable insights (CSV / PDF)

---
# 📎 Notes
 ⚠️ Spotify playlists must be public for analysis
 
 🔒 Authentication tokens are cached locally to avoid repeated logins
 
 🚀 Built for data storytelling, API mastery, and interactive analytics
