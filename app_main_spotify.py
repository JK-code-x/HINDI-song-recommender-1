"""
Hindi Song Recommender System - Spotify-Style UI (Pro Edition)
Artificial Intelligence Laboratory | Chandigarh University
CSE Core 1st Semester

Features:
- Spotify-inspired modern dark theme
- Interactive music player interface
- Advanced song recommendations
- Better visual hierarchy
- Smooth animations
"""

import streamlit as st
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import json
import os
from datetime import datetime

# ==================== PAGE CONFIGURATION ====================
st.set_page_config(
    page_title="Hindi Music Recommender",
    page_icon="🎵",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ==================== CUSTOM CSS - SPOTIFY STYLE ====================
st.markdown("""
<style>
    * {
        margin: 0;
        padding: 0;
        box-sizing: border-box;
    }
    
    html, body, [data-testid="stAppViewContainer"] {
        background: linear-gradient(135deg, #0f0c29, #302b63, #24243e);
        color: #fff;
    }
    
    [data-testid="stSidebar"] {
        background: rgba(20, 20, 30, 0.95);
        border-right: 1px solid #1DB954;
    }
    
    .main {
        background: transparent;
        padding: 2rem;
    }
    
    /* Spotify Green Accent */
    .spotify-green {
        color: #1DB954;
    }
    
    /* Song Cards */
    .song-card {
        background: linear-gradient(135deg, rgba(29, 185, 84, 0.1), rgba(45, 160, 110, 0.1));
        border: 1px solid rgba(29, 185, 84, 0.3);
        border-radius: 12px;
        padding: 1.5rem;
        margin: 0.75rem 0;
        transition: all 0.3s ease;
        cursor: pointer;
        backdrop-filter: blur(10px);
    }
    
    .song-card:hover {
        background: linear-gradient(135deg, rgba(29, 185, 84, 0.2), rgba(45, 160, 110, 0.2));
        border-color: #1DB954;
        transform: translateX(5px);
        box-shadow: 0 0 20px rgba(29, 185, 84, 0.3);
    }
    
    .song-title {
        font-size: 1.3rem;
        font-weight: 700;
        color: #fff;
        margin-bottom: 0.5rem;
        text-shadow: 0 2px 4px rgba(0,0,0,0.3);
    }
    
    .song-artist {
        font-size: 0.95rem;
        color: #b3b3b3;
        margin-bottom: 0.3rem;
    }
    
    .song-meta {
        display: flex;
        gap: 1rem;
        font-size: 0.85rem;
        color: #a0a0a0;
        margin-top: 0.5rem;
    }
    
    .similarity-badge {
        background: linear-gradient(135deg, #1DB954, #1ed760);
        padding: 0.3rem 0.8rem;
        border-radius: 20px;
        font-weight: 600;
        color: #000;
        display: inline-block;
        font-size: 0.85rem;
    }
    
    /* Header */
    .header-main {
        background: linear-gradient(135deg, #1DB954, #1ed760);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        font-size: 2.5rem;
        font-weight: 800;
        margin-bottom: 1rem;
        text-align: center;
    }
    
    /* Stats Cards */
    .stat-card {
        background: linear-gradient(135deg, rgba(29, 185, 84, 0.15), rgba(30, 215, 96, 0.15));
        border: 1px solid rgba(29, 185, 84, 0.4);
        border-radius: 12px;
        padding: 1.5rem;
        text-align: center;
        backdrop-filter: blur(10px);
    }
    
    .stat-number {
        font-size: 2.5rem;
        font-weight: 800;
        color: #1DB954;
        margin: 0.5rem 0;
    }
    
    .stat-label {
        font-size: 0.9rem;
        color: #b3b3b3;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    /* Buttons */
    .stButton > button {
        background: linear-gradient(135deg, #1DB954, #1ed760) !important;
        color: #000 !important;
        font-weight: 700 !important;
        border: none !important;
        border-radius: 24px !important;
        padding: 0.75rem 2rem !important;
        transition: all 0.3s ease !important;
        font-size: 1rem !important;
    }
    
    .stButton > button:hover {
        background: linear-gradient(135deg, #1ed760, #1DB954) !important;
        transform: scale(1.05) !important;
        box-shadow: 0 0 30px rgba(29, 185, 84, 0.4) !important;
    }
    
    /* Input fields */
    .stSelectbox, .stMultiSelect {
        background: rgba(30, 30, 50, 0.8) !important;
    }
    
    .stSelectbox > div > div, .stMultiSelect > div > div {
        background: rgba(30, 30, 50, 0.9) !important;
        border: 1px solid rgba(29, 185, 84, 0.3) !important;
        border-radius: 8px !important;
        color: #fff !important;
    }
    
    /* Tabs */
    .stTabs [data-baseweb="tab-list"] button {
        border-bottom: 2px solid transparent;
        color: #b3b3b3;
        transition: all 0.3s ease;
    }
    
    .stTabs [data-baseweb="tab-list"] button[aria-selected="true"] {
        border-bottom-color: #1DB954;
        color: #1DB954;
        font-weight: 700;
    }
    
    /* Sidebar */
    .sidebar-item {
        padding: 1rem;
        margin: 0.5rem 0;
        background: rgba(29, 185, 84, 0.1);
        border-left: 3px solid #1DB954;
        border-radius: 4px;
        cursor: pointer;
        transition: all 0.3s ease;
    }
    
    .sidebar-item:hover {
        background: rgba(29, 185, 84, 0.2);
        padding-left: 1.5rem;
    }
    
    /* Expander */
    .streamlit-expanderHeader {
        background: rgba(29, 185, 84, 0.1) !important;
        border: 1px solid rgba(29, 185, 84, 0.3) !important;
        border-radius: 8px !important;
    }
    
    .streamlit-expanderHeader:hover {
        background: rgba(29, 185, 84, 0.15) !important;
    }
    
    /* Metrics */
    [data-testid="metric-container"] {
        background: linear-gradient(135deg, rgba(29, 185, 84, 0.1), rgba(45, 160, 110, 0.1));
        padding: 1rem;
        border-radius: 12px;
        border: 1px solid rgba(29, 185, 84, 0.2);
    }
    
    .recommendation-reason {
        background: rgba(29, 185, 84, 0.05);
        border-left: 3px solid #1DB954;
        padding: 0.5rem 0.75rem;
        border-radius: 4px;
        font-size: 0.85rem;
        color: #1ed760;
        margin-top: 0.5rem;
    }
    
</style>
""", unsafe_allow_html=True)

# ==================== DATA LOADING & CACHING ====================
@st.cache_resource
def load_data():
    """Load and preprocess song dataset"""
    try:
        songs_df = pd.read_csv('data/hindi_songs.csv')
        return songs_df
    except FileNotFoundError:
        st.error("❌ Dataset not found. Please upload hindi_songs.csv to data/ folder")
        return None

@st.cache_resource
def get_vectorizer_and_matrix(songs_df):
    """Create TF-IDF vectorizer and similarity matrix"""
    songs_df['combined_features'] = (
        songs_df['artist'].fillna('') + ' ' +
        songs_df['genre'].fillna('') + ' ' +
        songs_df['mood'].fillna('') + ' ' +
        songs_df['language'].fillna('')
    )
    
    tfidf = TfidfVectorizer(
        max_features=500,
        stop_words='english',
        ngram_range=(1, 2)
    )
    tfidf_matrix = tfidf.fit_transform(songs_df['combined_features'])
    similarity_matrix = cosine_similarity(tfidf_matrix)
    
    return tfidf, tfidf_matrix, similarity_matrix, songs_df

# ==================== RECOMMENDATION ENGINE ====================
def get_recommendations(song_title, songs_df, similarity_matrix, 
                       n_recommendations=7, genre_filter=None, 
                       mood_filter=None, explain=True):
    """Get recommendations with filters and explanations"""
    try:
        idx = songs_df[songs_df['title'].str.lower() == song_title.lower()].index
        if len(idx) == 0:
            return None, "Song not found"
        
        idx = idx[0]
        sim_scores = list(enumerate(similarity_matrix[idx]))
        sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
        
        recommendations = []
        for i, (song_idx, score) in enumerate(sim_scores[1:]):
            if len(recommendations) >= n_recommendations:
                break
            
            song_data = songs_df.iloc[song_idx]
            
            if genre_filter and genre_filter != "All":
                if song_data['genre'].lower() != genre_filter.lower():
                    continue
            
            if mood_filter and mood_filter != "All":
                if song_data['mood'].lower() != mood_filter.lower():
                    continue
            
            reason = get_reason(songs_df.iloc[idx], song_data)
            
            recommendations.append({
                'title': song_data['title'],
                'artist': song_data['artist'],
                'genre': song_data['genre'],
                'mood': song_data['mood'],
                'language': song_data['language'],
                'similarity': score,
                'reason': reason if explain else None
            })
        
        return recommendations, "Success"
    except Exception as e:
        return None, str(e)

def get_reason(original, recommended):
    """Get recommendation reason"""
    reasons = []
    
    if original['artist'].lower() == recommended['artist'].lower():
        reasons.append("🎤 Same Artist")
    if original['genre'].lower() == recommended['genre'].lower():
        reasons.append("🎭 Similar Genre")
    if original['mood'].lower() == recommended['mood'].lower():
        reasons.append("😊 Same Mood")
    
    return " • ".join(reasons) if reasons else "✨ Similar Features"

# ==================== MAIN APP ====================
def main():
    songs_df = load_data()
    if songs_df is None:
        return
    
    tfidf, tfidf_matrix, similarity_matrix, songs_df = get_vectorizer_and_matrix(songs_df)
    
    # ==================== HEADER ====================
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown('<div class="header-main">🎵 Hindi Music Recommender</div>', unsafe_allow_html=True)
        st.markdown("<p style='text-align:center; color:#b3b3b3; font-size:0.95rem;'>Discover Your Next Favorite Song</p>", unsafe_allow_html=True)
    
    st.markdown("<hr style='border: 1px solid rgba(29, 185, 84, 0.2);'>", unsafe_allow_html=True)
    
    # ==================== STATS ====================
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
        <div class="stat-card">
            <div style="font-size: 1.5rem;">🎵</div>
            <div class="stat-number">{len(songs_df)}</div>
            <div class="stat-label">Total Songs</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="stat-card">
            <div style="font-size: 1.5rem;">🎤</div>
            <div class="stat-number">{songs_df['artist'].nunique()}</div>
            <div class="stat-label">Artists</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="stat-card">
            <div style="font-size: 1.5rem;">🎭</div>
            <div class="stat-number">{songs_df['genre'].nunique()}</div>
            <div class="stat-label">Genres</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown(f"""
        <div class="stat-card">
            <div style="font-size: 1.5rem;">😊</div>
            <div class="stat-number">{songs_df['mood'].nunique()}</div>
            <div class="stat-label">Moods</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # ==================== TABS ====================
    tab1, tab2, tab3, tab4 = st.tabs(["🎧 Discover", "🎼 Playlists", "📊 Analytics", "ℹ️ About"])
    
    # ==================== TAB 1: DISCOVER ====================
    with tab1:
        st.subheader("🔍 Find Your Next Song")
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            selected_song = st.selectbox(
                "Select a song you like:",
                sorted(songs_df['title'].unique()),
                help="Choose a song to get personalized recommendations"
            )
        
        with col2:
            n_recs = st.slider("Recommendations:", 1, 15, 7)
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            genre_filter = st.selectbox(
                "Genre:",
                ["All"] + sorted(songs_df['genre'].unique()),
                key="genre_filter"
            )
        
        with col2:
            mood_filter = st.selectbox(
                "Mood:",
                ["All"] + sorted(songs_df['mood'].unique()),
                key="mood_filter"
            )
        
        with col3:
            show_reasons = st.checkbox("Show reasons", value=True)
        
        if st.button("🎵 Get Recommendations", use_container_width=True):
            with st.spinner("Finding similar songs..."):
                recs, status = get_recommendations(
                    selected_song, songs_df, similarity_matrix,
                    n_recs,
                    genre_filter if genre_filter != "All" else None,
                    mood_filter if mood_filter != "All" else None,
                    show_reasons
                )
                
                if recs:
                    seed = songs_df[songs_df['title'].str.lower() == selected_song.lower()].iloc[0]
                    
                    st.markdown(f"""
                    <div style='text-align:center; margin: 1.5rem 0;'>
                        <p style='color:#b3b3b3; font-size:0.9rem;'>Based on your selection:</p>
                        <p style='font-size:1.3rem; font-weight:700; color:#1DB954;'>{seed['title']}</p>
                        <p style='color:#a0a0a0; font-size:0.85rem;'>by {seed['artist']}</p>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    st.markdown("<hr style='border: 1px solid rgba(29, 185, 84, 0.2);'>", unsafe_allow_html=True)
                    
                    for idx, rec in enumerate(recs, 1):
                        st.markdown(f"""
                        <div class="song-card">
                            <div style="display: flex; justify-content: space-between; align-items: start;">
                                <div>
                                    <div class="song-title">#{idx} {rec['title']}</div>
                                    <div class="song-artist">🎤 {rec['artist']}</div>
                                    <div class="song-meta">
                                        <span>🎭 {rec['genre']}</span>
                                        <span>😊 {rec['mood']}</span>
                                    </div>
                                    {f'<div class="recommendation-reason">💡 {rec["reason"]}</div>' if show_reasons else ''}
                                </div>
                                <div class="similarity-badge">{rec['similarity']:.0%}</div>
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
                else:
                    st.error(f"❌ {status}")
    
    # ==================== TAB 2: PLAYLISTS ====================
    with tab2:
        st.subheader("🎼 Create a Playlist")
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            playlist_name = st.text_input(
                "Playlist name:",
                value="My Awesome Playlist",
                help="Give your playlist a name"
            )
        
        with col2:
            playlist_size = st.slider("Size:", 5, 50, 15, 5)
        
        seed_songs = st.multiselect(
            "Select 2-5 songs to base playlist on:",
            sorted(songs_df['title'].unique()),
            max_selections=5,
            help="Choose songs you like"
        )
        
        if st.button("🎼 Generate Playlist", use_container_width=True):
            if len(seed_songs) < 2:
                st.warning("⚠️ Please select at least 2 songs")
            else:
                with st.spinner("Creating your playlist..."):
                    playlist = []
                    used_indices = set()
                    
                    for seed in seed_songs:
                        recs, _ = get_recommendations(
                            seed, songs_df, similarity_matrix,
                            10, explain=False
                        )
                        
                        if recs:
                            for rec in recs:
                                if rec not in [p for p in playlist]:
                                    playlist.append(rec)
                                    if len(playlist) >= playlist_size:
                                        break
                        if len(playlist) >= playlist_size:
                            break
                    
                    st.markdown(f"<p style='font-size:1.3rem; font-weight:700; color:#1DB954; text-align:center;'>🎼 {playlist_name}</p>", unsafe_allow_html=True)
                    st.markdown(f"<p style='text-align:center; color:#b3b3b3;'>{len(playlist)} songs • Created just now</p>", unsafe_allow_html=True)
                    st.markdown("<hr style='border: 1px solid rgba(29, 185, 84, 0.2);'>", unsafe_allow_html=True)
                    
                    for idx, song in enumerate(playlist[:playlist_size], 1):
                        st.markdown(f"""
                        <div class="song-card">
                            <div class="song-title">#{idx} {song['title']}</div>
                            <div class="song-artist">🎤 {song['artist']}</div>
                            <div class="song-meta">
                                <span>🎭 {song['genre']}</span>
                                <span>😊 {song['mood']}</span>
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
    
    # ==================== TAB 3: ANALYTICS ====================
    with tab3:
        st.subheader("📊 Music Insights")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**🎭 Top Genres**")
            genre_counts = songs_df['genre'].value_counts().head(5)
            st.bar_chart(genre_counts)
        
        with col2:
            st.markdown("**😊 Top Moods**")
            mood_counts = songs_df['mood'].value_counts().head(5)
            st.bar_chart(mood_counts)
        
        st.markdown("<hr style='border: 1px solid rgba(29, 185, 84, 0.2);'>", unsafe_allow_html=True)
        
        st.markdown("**🎤 Top 10 Artists**")
        artist_counts = songs_df['artist'].value_counts().head(10)
        st.bar_chart(artist_counts)
    
    # ==================== TAB 4: ABOUT ====================
    with tab4:
        st.markdown("""
        ## 🎵 About This Project
        
        **Hindi Song Recommender System** is an AI-powered music discovery platform built for 
        Chandigarh University's AI Laboratory course.
        
        ### 📚 Technology
        - **Algorithm**: Content-Based Filtering with TF-IDF
        - **Similarity**: Cosine Similarity Metric
        - **Framework**: Streamlit
        - **Libraries**: Scikit-learn, Pandas, NumPy
        
        ### 🎓 Course Information
        - **Institution**: Chandigarh University
        - **Department**: Computer Science & Engineering
        - **Course**: Artificial Intelligence Laboratory
        - **Semester**: 1st Semester (CSE Core)
        - **Session**: 2025-2026
        
        ### 👥 Team
        - Jaskeerat Singh (25BCS12208)
        - Aman Kumar (25BCS12035)
        - Adhiraj Pandey (25BCS12700)
        - Priyanka Thakur (25BCS10921)
        - Jaskiran Kaur (25BCS12387)
        
        **Supervisor**: Mr. Sachin Thakur
        
        ---
        
        **Built with ❤️ for AI Learning**
        """)

if __name__ == "__main__":
    main()
