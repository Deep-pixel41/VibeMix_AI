# 🎧 VibeMix AI: Emotion-Driven Spotify Curator

**VibeMix AI** is an intelligent music discovery web application that translates complex human emotions into curated Spotify playlists. By bridging Natural Language Processing (NLP) with the Spotify ecosystem, VibeMix AI moves beyond standard keyword searches, using a Large Language Model to interpret your exact "vibe" and generate a synchronized playlist in real-time.

---

## 🚀 Key Features

*   **Emotion-to-Music NLP:** Uses Groq (Llama-3.1) to analyze descriptive text (e.g., *"Coding at 2 AM in a rainy cyberpunk city"*) and generate highly contextual song recommendations.
*   **Spotify Integration:** Secure OAuth 2.0 authentication for direct-to-account playlist creation.
*   **Dynamic UI Gallery:** A custom-built Streamlit grid that fetches and displays high-resolution album covers before finalizing the playlist.
*   **Session Memory:** A local SQLite database backend that tracks your generated playlists and "Vibe History" for future listening.
*   **Modular Architecture:** Built using "Separation of Concerns," cleanly isolating database and UI logic from the main application controller.

---

## 🛠️ Tech Stack

*   **Frontend:** [Streamlit](https://streamlit.io/) (Data-driven Web Interface)
*   **Intelligence:** [Groq Cloud API](https://groq.com/) (Llama-3.1-8b-instant)
*   **Backend API:** [Spotipy](https://spotipy.readthedocs.io/) (Spotify Web API Wrapper)
*   **Database:** [SQLite3](https://www.sqlite.org/index.html) (Local Relational Storage)
*   **Environment:** Python 3.x with `python-dotenv` for secret management

---

## 🏗️ Project Structure

```text
vibemix-ai/
├── app.py               # Main controller, API synchronization, and business logic
├── features.py          # Utility layer (SQLite database ops & UI rendering)
├── requirements.txt     # Project dependencies
├── .env                 # Environment variables (Ignored by Git)
└── .gitignore           # Git ignore file