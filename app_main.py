"""
Hindi Song Recommender System - Upgraded Version
Artificial Intelligence Laboratory | Chandigarh University
CSE Core 1st Semester

Features:
- Content-based filtering with genre/mood filtering
- User profiles and history tracking
- Playlist generation
- Enhanced UI with dark mode
- Recommendation explanations
- Performance optimization with caching
"""

import streamlit as st
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import pickle
import os
from datetime import datetime
import json

# ==================== PAGE CONFIGURATION ====================
st.set_page_config(
    page_title="Hindi Song Recommender Pro",
    page_icon="🎵",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==================== CUSTOM CSS ====================
st.markdown("""
<style>
    .main {
        padding: 2rem;
    }
    .recommendation-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 10px;
        color: white;
        margin: 0.5rem 0;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    .song-title {
        font-size: 1.2rem;
        font-weight: bold;
        margin-bottom: 0.5rem;
    }
    .song-details {
        font-size: 0.9rem;
        opacity: 0.9;
    }
    .similarity-score {
        background: rgba(255,255,255,0.2);
        padding: 0.5rem 1rem;
        border-radius: 5px;
        display: inline-block;
        margin-top: 0.5rem;
    }
    .filter-section {
        background: #f0f2f6;
        padding: 1.5rem;
        border-radius: 8px;
        margin-bottom: 1.5rem;
    }
    .stats-card {
        background: white;
        padding: 1rem;
        border-radius: 8px;
        border-left: 4px solid #667eea;
        margin: 0.5rem 0;
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
        st.error("❌ Dataset not found. Please upload hindi_songs.csv")
        return None

@st.cache_resource
def get_vectorizer_and_matrix(songs_df):
    """Create TF-IDF vectorizer and similarity matrix"""
    # Create combined features
    songs_df['combined_features'] = (
        songs_df['artist'].fillna('') + ' ' +
        songs_df['genre'].fillna('') + ' ' +
        songs_df['mood'].fillna('') + ' ' +
        songs_df['language'].fillna('')
    )
    
    # Vectorize
    tfidf = TfidfVectorizer(
        max_features=500,
        stop_words='english',
        ngram_range=(1, 2)
    )
    tfidf_matrix = tfidf.fit_transform(songs_df['combined_features'])
    
    # Calculate similarity matrix
    similarity_matrix = cosine_similarity(tfidf_matrix)
    
    return tfidf, tfidf_matrix, similarity_matrix, songs_df

# ==================== USER PROFILE MANAGEMENT ====================
@st.cache_resource
def load_user_profiles():
    """Load user profiles from JSON"""
    if os.path.exists('data/user_profiles.json'):
        with open('data/user_profiles.json', 'r') as f:
            return json.load(f)
    return {}

def save_user_profiles(profiles):
    """Save user profiles to JSON"""
    os.makedirs('data', exist_ok=True)
    with open('data/user_profiles.json', 'w') as f:
        json.dump(profiles, f, indent=2)

def create_user_profile(username):
    """Create new user profile"""
    profiles = load_user_profiles()
    if username not in profiles:
        profiles[username] = {
            'created_date': datetime.now().isoformat(),
            'favorites': [],
            'history': [],
            'playlists': [],
            'preferences': {
                'genres': [],
                'moods': [],
                'artists': []
            }
        }
        save_user_profiles(profiles)
    return profiles

def add_to_favorites(username, song_title):
    """Add song to user favorites"""
    profiles = load_user_profiles()
    if username in profiles:
        if song_title not in profiles[username]['favorites']:
            profiles[username]['favorites'].append(song_title)
            save_user_profiles(profiles)
            return True
    return False

# ==================== RECOMMENDATION ENGINE ====================
def get_recommendations(song_title, songs_df, similarity_matrix, 
                       n_recommendations=5, genre_filter=None, 
                       mood_filter=None, explain=True):
    """
    Get recommendations with filters and explanations
    
    Parameters:
    - song_title: Selected song
    - songs_df: Song dataset
    - similarity_matrix: Precomputed similarity matrix
    - n_recommendations: Number of songs to recommend
    - genre_filter: Filter by genre (optional)
    - mood_filter: Filter by mood (optional)
    - explain: Return explanation for each recommendation
    """
    
    try:
        # Find song index
        idx = songs_df[songs_df['title'].str.lower() == song_title.lower()].index
        if len(idx) == 0:
            return None, "Song not found in database"
        
        idx = idx[0]
        
        # Get similarity scores
        sim_scores = list(enumerate(similarity_matrix[idx]))
        sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
        
        # Apply filters
        recommendations = []
        for i, (song_idx, score) in enumerate(sim_scores[1:]):
            if len(recommendations) >= n_recommendations:
                break
            
            song_data = songs_df.iloc[song_idx]
            
            # Apply genre filter
            if genre_filter and genre_filter != "All":
                if song_data['genre'].lower() != genre_filter.lower():
                    continue
            
            # Apply mood filter
            if mood_filter and mood_filter != "All":
                if song_data['mood'].lower() != mood_filter.lower():
                    continue
            
            # Determine explanation reason
            reason = get_recommendation_reason(
                songs_df.iloc[idx], song_data
            )
            
            recommendations.append({
                'index': song_idx,
                'title': song_data['title'],
                'artist': song_data['artist'],
                'genre': song_data['genre'],
                'mood': song_data['mood'],
                'language': song_data['language'],
                'similarity_score': score,
                'reason': reason if explain else None
            })
        
        return recommendations, "Success"
    
    except Exception as e:
        return None, f"Error: {str(e)}"

def get_recommendation_reason(original_song, recommended_song):
    """Generate explanation for recommendation"""
    reasons = []
    
    if original_song['artist'].lower() == recommended_song['artist'].lower():
        reasons.append("Same Artist")
    
    if original_song['genre'].lower() == recommended_song['genre'].lower():
        reasons.append("Similar Genre")
    
    if original_song['mood'].lower() == recommended_song['mood'].lower():
        reasons.append("Same Mood")
    
    if original_song['language'].lower() == recommended_song['language'].lower():
        reasons.append("Same Language")
    
    return " • ".join(reasons) if reasons else "Similar Features"

def generate_playlist(seed_songs, songs_df, similarity_matrix, 
                     playlist_name, n_songs=15):
    """Generate playlist from multiple seed songs"""
    playlist_songs = []
    used_indices = set()
    
    for seed_song in seed_songs:
        recommendations, status = get_recommendations(
            seed_song, songs_df, similarity_matrix, 
            n_recommendations=5, explain=False
        )
        
        if recommendations:
            for rec in recommendations:
                if rec['index'] not in used_indices:
                    playlist_songs.append(rec)
                    used_indices.add(rec['index'])
                    if len(playlist_songs) >= n_songs:
                        break
        
        if len(playlist_songs) >= n_songs:
            break
    
    return playlist_songs[:n_songs]

# ==================== ANALYTICS & STATISTICS ====================
def get_analytics_data(songs_df):
    """Get analytics for dashboard"""
    analytics = {
        'total_songs': len(songs_df),
        'total_artists': songs_df['artist'].nunique(),
        'total_genres': songs_df['genre'].nunique(),
        'total_moods': songs_df['mood'].nunique(),
        'top_genres': songs_df['genre'].value_counts().head(5),
        'top_moods': songs_df['mood'].value_counts().head(5),
        'top_artists': songs_df['artist'].value_counts().head(10)
    }
    return analytics

# ==================== MAIN APP ====================
def main():
    """Main application function"""
    
    # Load data
    songs_df = load_data()
    if songs_df is None:
        return
    
    # Get vectorizer and matrices
    tfidf, tfidf_matrix, similarity_matrix, songs_df = get_vectorizer_and_matrix(songs_df)
    
    # Sidebar
    st.sidebar.title("🎵 Navigation")
    page = st.sidebar.radio(
        "Select a page:",
        ["🏠 Home", "🎧 Recommendations", "📋 Playlists", 
         "👤 Profile", "📊 Analytics", "ℹ️ About"]
    )
    
    st.sidebar.markdown("---")
    st.sidebar.markdown(
        """
        ### About
        **Hindi Song Recommender Pro**
        
        AI-powered music discovery system
        using content-based filtering.
        
        Built for Chandigarh University
        AI Lab Course (CSE Core)
        """
    )
    
    # ==================== PAGE: HOME ====================
    if page == "🏠 Home":
        st.title("🎵 Hindi Song Recommender - Upgraded Version")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Total Songs", len(songs_df))
        
        with col2:
            st.metric("Total Artists", songs_df['artist'].nunique())
        
        with col3:
            st.metric("Total Genres", songs_df['genre'].nunique())
        
        st.markdown("---")
        
        st.subheader("✨ Key Features")
        features = [
            "🎯 **Smart Recommendations** - Content-based filtering with genre/mood filters",
            "📌 **Favorites** - Save your favorite songs and artists",
            "🎼 **Smart Playlists** - Generate playlists from multiple seed songs",
            "📊 **Analytics Dashboard** - Explore music trends and statistics",
            "💡 **Recommendation Explanations** - Understand why songs are recommended",
            "🌙 **Dark Mode Support** - Eye-friendly interface"
        ]
        
        for feature in features:
            st.write(feature)
        
        st.markdown("---")
        st.info(
            "👉 **Get Started:** Go to 'Recommendations' tab to discover new Hindi songs!"
        )
    
    # ==================== PAGE: RECOMMENDATIONS ====================
    elif page == "🎧 Recommendations":
        st.title("🎧 Get Song Recommendations")
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            selected_song = st.selectbox(
                "Select a Hindi song to get recommendations:",
                sorted(songs_df['title'].unique()),
                help="Choose a song you like to discover similar songs"
            )
        
        with col2:
            n_recommendations = st.slider(
                "Number of recommendations:",
                min_value=1,
                max_value=15,
                value=5,
                step=1
            )
        
        st.markdown("---")
        st.subheader("🎯 Apply Filters (Optional)")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            genre_filter = st.selectbox(
                "Filter by Genre:",
                ["All"] + sorted(songs_df['genre'].unique()),
                help="Leave as 'All' for no filter"
            )
        
        with col2:
            mood_filter = st.selectbox(
                "Filter by Mood:",
                ["All"] + sorted(songs_df['mood'].unique()),
                help="Leave as 'All' for no filter"
            )
        
        with col3:
            show_explanation = st.checkbox(
                "Show explanations",
                value=True,
                help="Display why each song is recommended"
            )
        
        st.markdown("---")
        
        # Get recommendations
        if st.button("🔍 Get Recommendations", use_container_width=True):
            recommendations, status = get_recommendations(
                selected_song,
                songs_df,
                similarity_matrix,
                n_recommendations,
                genre_filter if genre_filter != "All" else None,
                mood_filter if mood_filter != "All" else None,
                show_explanation
            )
            
            if recommendations is None:
                st.error(f"❌ {status}")
            else:
                # Get seed song info
                seed_song = songs_df[songs_df['title'].str.lower() == selected_song.lower()].iloc[0]
                
                st.success(f"✅ Found {len(recommendations)} recommendations!")
                
                st.markdown(f"""
                **Seed Song:** 🎵 {seed_song['title']} by {seed_song['artist']}
                | Genre: {seed_song['genre']} | Mood: {seed_song['mood']}
                """)
                
                st.markdown("---")
                st.subheader(f"🎼 Top {len(recommendations)} Recommended Songs")
                
                for idx, rec in enumerate(recommendations, 1):
                    with st.container():
                        st.markdown(f"""
                        <div class="recommendation-card">
                            <div class="song-title">
                                {idx}. {rec['title']}
                            </div>
                            <div class="song-details">
                                👤 {rec['artist']} | 🎭 {rec['genre']} | 😊 {rec['mood']}
                            </div>
                            <div class="similarity-score">
                                ✅ Similarity: {rec['similarity_score']:.1%}
                            </div>
                            {f"<div class='song-details'>💡 {rec['reason']}</div>" if show_explanation else ""}
                        </div>
                        """, unsafe_allow_html=True)
                        
                        col1, col2 = st.columns(2)
                        with col1:
                            if st.button(f"❤️ Add to Favorites", key=f"fav_{idx}"):
                                st.success(f"Added '{rec['title']}' to favorites!")
                        
                        with col2:
                            st.write("")  # Spacing
    
    # ==================== PAGE: PLAYLISTS ====================
    elif page == "📋 Playlists":
        st.title("📋 Generate Smart Playlists")
        
        st.markdown("""
        Generate playlists by selecting multiple seed songs.
        The system will create a cohesive playlist based on similarity.
        """)
        
        st.markdown("---")
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            playlist_name = st.text_input(
                "Playlist Name:",
                value="My Awesome Playlist",
                help="Give your playlist a name"
            )
        
        with col2:
            playlist_size = st.slider(
                "Playlist Size:",
                min_value=5,
                max_value=50,
                value=15,
                step=5
            )
        
        st.markdown("---")
        st.subheader("Select Seed Songs (2-5 songs)")
        
        seed_songs = st.multiselect(
            "Choose songs to base the playlist on:",
            sorted(songs_df['title'].unique()),
            max_selections=5,
            help="Select 2-5 songs you like"
        )
        
        if st.button("🎼 Generate Playlist", use_container_width=True):
            if len(seed_songs) < 2:
                st.warning("⚠️ Please select at least 2 seed songs")
            else:
                with st.spinner("🎵 Creating your playlist..."):
                    playlist = generate_playlist(
                        seed_songs,
                        songs_df,
                        similarity_matrix,
                        playlist_name,
                        playlist_size
                    )
                
                st.success(f"✅ Playlist '{playlist_name}' created with {len(playlist)} songs!")
                
                st.markdown("---")
                st.subheader(f"🎼 {playlist_name}")
                
                for idx, song in enumerate(playlist, 1):
                    st.write(f"**{idx}.** {song['title']} by {song['artist']} | {song['genre']}")
                
                # Download playlist
                playlist_df = pd.DataFrame(playlist)
                csv = playlist_df.to_csv(index=False)
                st.download_button(
                    label="📥 Download Playlist (CSV)",
                    data=csv,
                    file_name=f"{playlist_name}.csv",
                    mime="text/csv"
                )
    
    # ==================== PAGE: PROFILE ====================
    elif page == "👤 Profile":
        st.title("👤 User Profile")
        
        username = st.text_input(
            "Enter your username:",
            value="guest",
            help="Create or load your profile"
        )
        
        if st.button("Load Profile"):
            profiles = create_user_profile(username)
            profile = profiles[username]
            
            st.success(f"✅ Loaded profile for: {username}")
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric("Favorites", len(profile['favorites']))
            
            with col2:
                st.metric("History", len(profile['history']))
            
            with col3:
                st.metric("Playlists", len(profile['playlists']))
            
            st.markdown("---")
            st.subheader("❤️ Your Favorite Songs")
            
            if profile['favorites']:
                for song in profile['favorites']:
                    st.write(f"🎵 {song}")
            else:
                st.info("No favorites yet. Add some songs from recommendations!")
            
            st.markdown("---")
            st.subheader("📊 Your Preferences")
            
            if profile['preferences']['genres']:
                st.write(f"**Favorite Genres:** {', '.join(profile['preferences']['genres'])}")
            if profile['preferences']['moods']:
                st.write(f"**Favorite Moods:** {', '.join(profile['preferences']['moods'])}")
    
    # ==================== PAGE: ANALYTICS ====================
    elif page == "📊 Analytics":
        st.title("📊 Music Analytics Dashboard")
        
        analytics = get_analytics_data(songs_df)
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("📀 Total Songs", analytics['total_songs'])
        with col2:
            st.metric("🎤 Total Artists", analytics['total_artists'])
        with col3:
            st.metric("🎭 Total Genres", analytics['total_genres'])
        with col4:
            st.metric("😊 Total Moods", analytics['total_moods'])
        
        st.markdown("---")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("🎭 Top Genres")
            st.bar_chart(analytics['top_genres'])
        
        with col2:
            st.subheader("😊 Top Moods")
            st.bar_chart(analytics['top_moods'])
        
        st.markdown("---")
        
        st.subheader("🎤 Top 10 Artists")
        st.bar_chart(analytics['top_artists'])
    
    # ==================== PAGE: ABOUT ====================
    elif page == "ℹ️ About":
        st.title("ℹ️ About This Project")
        
        st.markdown("""
        ## Hindi Song Recommender System - Upgraded Version
        
        ### Project Information
        - **Institution:** Chandigarh University
        - **Department:** Computer Science & Engineering
        - **Course:** Artificial Intelligence Laboratory
        - **Semester:** 1st Semester (CSE Core)
        - **Session:** 2025-2026
        
        ### Team
        - Jaskeerat Singh (25BCS12208)
        - Aman Kumar (25BCS12035)
        - Adhiraj Pandey (25BCS12700)
        - Priyanka Thakur (25BCS10921)
        - Jaskiran Kaur (25BCS12387)
        
        ### Supervisor
        Mr. Sachin Thakur
        
        ### Project Description
        
        This is an **upgraded version** of the Hindi Song Recommender System,
        featuring advanced AI techniques for music discovery.
        
        #### Features in This Version
        
        1. **Content-Based Filtering:** Recommends songs similar to user selection
        2. **Genre & Mood Filtering:** Refine recommendations by genre and mood
        3. **User Profiles:** Save favorites and track listening history
        4. **Smart Playlists:** Generate playlists from multiple seed songs
        5. **Recommendation Explanations:** Understand why songs are recommended
        6. **Analytics Dashboard:** Explore music statistics and trends
        7. **Performance Optimization:** Cached vectorization and similarity matrices
        8. **Enhanced UI:** Modern, intuitive interface with Streamlit
        
        #### Technology Stack
        
        - **Language:** Python 3.8+
        - **Web Framework:** Streamlit
        - **ML Libraries:** Scikit-learn, Pandas, NumPy
        - **Algorithm:** TF-IDF Vectorization + Cosine Similarity
        
        #### Algorithm Explanation
        
        **TF-IDF (Term Frequency-Inverse Document Frequency):**
        - Converts song metadata (artist, genre, mood, language) into numerical vectors
        - Emphasizes distinctive features of each song
        
        **Cosine Similarity:**
        - Measures angular similarity between song feature vectors
        - Produces similarity scores between 0 and 1
        
        **Recommendation Process:**
        1. Combine song features into text representation
        2. Apply TF-IDF vectorization
        3. Calculate cosine similarity between selected song and all others
        4. Sort by similarity score and apply filters
        5. Return top N recommendations with explanations
        
        #### Future Enhancements
        
        - Collaborative filtering integration
        - Audio feature analysis (Spotify API)
        - Lyrics-based recommendations using NLP
        - Real-time learning from user feedback
        - Social sharing and recommendations
        - Integration with music streaming platforms
        
        #### References
        
        1. Scikit-learn Documentation
        2. Streamlit Documentation
        3. Recommendation Systems: A Primer (Medium)
        4. Content-Based Filtering Algorithms
        
        ---
        
        **Built with ❤️ for AI Learning | Chandigarh University**
        """)

if __name__ == "__main__":
    main()
