"""
Configuration settings for Hindi Song Recommender System
"""

import os

# App Configuration
APP_NAME = "Hindi Song Recommender Pro"
APP_VERSION = "2.0.0"
APP_DESCRIPTION = "AI-powered music recommendation system for Chandigarh University"

# Paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, 'data')
CONFIG_DIR = os.path.join(BASE_DIR, 'config')

# Data Configuration
DATASET_PATH = os.path.join(DATA_DIR, 'hindi_songs.csv')
USER_PROFILES_PATH = os.path.join(DATA_DIR, 'user_profiles.json')

# ML Configuration
TFIDF_MAX_FEATURES = 500
TFIDF_NGRAM_RANGE = (1, 2)
TFIDF_STOP_WORDS = 'english'

# Recommendation Configuration
DEFAULT_N_RECOMMENDATIONS = 5
MAX_N_RECOMMENDATIONS = 15
MIN_SEED_SONGS = 2
MAX_SEED_SONGS = 5
MIN_PLAYLIST_SIZE = 5
MAX_PLAYLIST_SIZE = 50

# UI Configuration
PAGE_ICON = "🎵"
LAYOUT = "wide"
INITIAL_SIDEBAR_STATE = "expanded"

# Feature Columns
REQUIRED_COLUMNS = ['title', 'artist', 'genre', 'mood', 'language']
FEATURE_COLUMNS = ['artist', 'genre', 'mood', 'language']

# Similarity Threshold
MIN_SIMILARITY_THRESHOLD = 0.0  # 0% - no minimum threshold
MAX_SIMILARITY_THRESHOLD = 1.0  # 100% - maximum similarity

# Cache Configuration
CACHE_DURATION = 3600  # 1 hour in seconds
USE_CACHE = True

# Logging Configuration
LOG_LEVEL = "INFO"
LOG_FILE = os.path.join(BASE_DIR, 'logs', 'app.log')

# Project Information
PROJECT_INSTITUTION = "Chandigarh University"
PROJECT_DEPARTMENT = "Computer Science & Engineering"
PROJECT_COURSE = "Artificial Intelligence Laboratory"
PROJECT_SEMESTER = "1st Semester (CSE Core)"
PROJECT_SESSION = "2025-2026"

TEAM_MEMBERS = [
    "Jaskeerat Singh (25BCS12208)",
    "Aman Kumar (25BCS12035)",
    "Adhiraj Pandey (25BCS12700)",
    "Priyanka Thakur (25BCS10921)",
    "Jaskiran Kaur (25BCS12387)"
]

SUPERVISOR = "Mr. Sachin Thakur"

# Create necessary directories
os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(CONFIG_DIR, exist_ok=True)
os.makedirs(os.path.join(BASE_DIR, 'logs'), exist_ok=True)
