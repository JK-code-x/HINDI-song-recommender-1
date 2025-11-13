# Hindi Song Recommender System - Upgraded Version

An AI-powered music recommendation system built for Chandigarh University's AI Laboratory course. This upgraded version includes advanced features like user profiles, smart playlists, genre/mood filtering, and analytics.

## 🎯 Features

### Core Features
- **Content-Based Filtering**: Recommends songs similar to user selection using TF-IDF and cosine similarity
- **Genre & Mood Filtering**: Refine recommendations by specific genres or moods
- **Recommendation Explanations**: Understand why each song is recommended (same artist, genre, mood, language)
- **User Profiles**: Create profiles, save favorites, and track listening history

### Advanced Features
- **Smart Playlist Generation**: Create playlists from multiple seed songs
- **Analytics Dashboard**: Explore music statistics, top genres, artists, and moods
- **Performance Optimization**: Cached vectorization and similarity matrices for fast recommendations
- **Enhanced UI**: Modern, intuitive interface built with Streamlit
- **CSV Export**: Download playlists and recommendations

## 🛠️ Technology Stack

- **Language**: Python 3.8+
- **Web Framework**: Streamlit
- **ML Libraries**:
  - scikit-learn (TF-IDF, Cosine Similarity)
  - Pandas (Data manipulation)
  - NumPy (Numerical operations)

## 📋 Project Information

- **Institution**: Chandigarh University
- **Department**: Computer Science & Engineering
- **Course**: Artificial Intelligence Laboratory
- **Semester**: 1st Semester (CSE Core)
- **Session**: 2025-2026

### Team Members
- Jaskeerat Singh (25BCS12208)
- Aman Kumar (25BCS12035)
- Adhiraj Pandey (25BCS12700)
- Priyanka Thakur (25BCS10921)
- Jaskiran Kaur (25BCS12387)

### Supervisor
Mr. Sachin Thakur

## 📦 Installation

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)

### Setup Instructions

1. **Clone the repository**:
   ```bash
   git clone https://github.com/yourusername/hindi-song-recommender-upgraded.git
   cd hindi-song-recommender-upgraded
   ```

2. **Create a virtual environment** (recommended):
   ```bash
   python -m venv venv
   
   # On Windows:
   venv\Scripts\activate
   
   # On macOS/Linux:
   source venv/bin/activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Prepare your dataset**:
   - Create a `data` folder in the project root
   - Place your `hindi_songs.csv` file in the `data` folder
   - Required columns: `title`, `artist`, `genre`, `mood`, `language`

5. **Run the application**:
   ```bash
   streamlit run app_main.py
   ```

6. **Access the app**:
   - Open your browser and go to `http://localhost:8501`

## 📊 Dataset Format

The `hindi_songs.csv` file should have the following structure:

```csv
title,artist,genre,mood,language
Tum Hi Ho,Arijit Singh,Romantic,Sad,Hindi
Ae Dil Hai Mushkil,Arijit Singh,Romantic,Emotional,Hindi
Deewani Mastani,Hrithik Roshan,Bollywood,Happy,Hindi
Raabta,Arijit Singh,Romantic,Romantic,Hindi
```

**Required Columns**:
- `title`: Song title (string)
- `artist`: Artist name (string)
- `genre`: Music genre (string, e.g., Romantic, Bollywood, Pop)
- `mood`: Song mood (string, e.g., Happy, Sad, Romantic)
- `language`: Song language (string, usually "Hindi")

## 🚀 How to Use

### 1. Home Page
- View overall statistics (total songs, artists, genres)
- Learn about key features

### 2. Recommendations
- Select a song from dropdown
- Adjust number of recommendations (1-15)
- Apply filters by genre and mood
- Click "Get Recommendations" to receive personalized suggestions
- View similarity scores and explanation reasons
- Add songs to favorites

### 3. Playlists
- Enter a playlist name
- Select 2-5 seed songs
- Specify desired playlist size (5-50 songs)
- Generate a cohesive playlist
- Download as CSV

### 4. Profile
- Enter your username
- View favorite songs and listening history
- Track your preferences
- Manage multiple user profiles

### 5. Analytics
- View comprehensive music statistics
- Explore top genres and moods
- Analyze top artists
- Interactive charts and visualizations

### 6. About
- Project information and team details
- Algorithm explanation
- Future enhancement ideas

## 🔧 Algorithm Details

### TF-IDF Vectorization
Converts song metadata into weighted numerical vectors:
```
TF(t,d) = count of term t in document d / total terms in d
IDF(t) = log(total documents / documents containing t)
TF-IDF(t,d) = TF(t,d) × IDF(t)
```

### Cosine Similarity
Measures angular similarity between song vectors:
```
similarity(A, B) = (A · B) / (||A|| × ||B||)
```

Where values range from 0 (no similarity) to 1 (identical).

## 📂 Project Structure

```
hindi-song-recommender-upgraded/
│
├── app_main.py                 # Main application file
├── requirements.txt            # Python dependencies
├── README.md                   # Project documentation
├── .gitignore                  # Git ignore rules
├── LICENSE                     # MIT License
│
├── data/
│   ├── hindi_songs.csv         # Song dataset (add this file)
│   └── user_profiles.json      # User profiles (auto-generated)
│
├── config/
│   └── settings.py             # Configuration settings
│
└── docs/
    ├── INSTALLATION.md         # Detailed installation guide
    ├── USAGE.md               # Usage guide
    └── API.md                 # API documentation
```

## 🚀 Deployment

### Deploy on Streamlit Cloud

1. **Push to GitHub**:
   ```bash
   git add .
   git commit -m "Initial commit"
   git push origin main
   ```

2. **Go to Streamlit Cloud**:
   - Visit https://share.streamlit.io
   - Click "New app"
   - Select your GitHub repo
   - Choose the branch and main file (`app_main.py`)

3. **Configure secrets** (if needed):
   - Add `data/hindi_songs.csv` to your repo or upload to Streamlit Cloud

## 🔐 Security Considerations

- User profiles stored locally in JSON (production should use database)
- No authentication implemented (add for production)
- Data is not sent to external servers (runs locally)

## 🐛 Troubleshooting

### Issue: "Dataset not found"
**Solution**: Ensure `data/hindi_songs.csv` exists in the project directory with correct columns.

### Issue: App runs slowly
**Solution**: The caching (@st.cache_resource) should speed it up. Clear cache if issues persist:
```bash
streamlit cache clear
```

### Issue: Import errors
**Solution**: Reinstall requirements:
```bash
pip install --upgrade -r requirements.txt
```

## 📈 Future Enhancements

- [ ] Collaborative filtering integration
- [ ] Audio feature analysis using Spotify API
- [ ] Lyrics-based recommendations with NLP
- [ ] Real-time learning from user feedback
- [ ] Social sharing capabilities
- [ ] Music streaming platform integration
- [ ] Database backend for scalability
- [ ] User authentication system
- [ ] Advanced visualization dashboard
- [ ] Deep learning models for embeddings

## 📚 References

1. Scikit-learn Documentation: https://scikit-learn.org/
2. Streamlit Documentation: https://docs.streamlit.io/
3. TF-IDF Vectorization: https://en.wikipedia.org/wiki/Tf%E2%80%93idf
4. Cosine Similarity: https://en.wikipedia.org/wiki/Cosine_similarity
5. Recommendation Systems Primer: https://medium.com/

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👥 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📞 Support

For issues, questions, or suggestions, please open an issue on GitHub.

---

**Built with ❤️ for AI Learning | Chandigarh University**

*Last Updated: November 2025*
