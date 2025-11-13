# GitHub Upload Instructions for Hindi Song Recommender Upgraded Version

## Complete Guide to Set Up Your GitHub Repository

### Step 1: Create a New GitHub Repository

1. Go to https://github.com/new
2. **Repository name**: `hindi-song-recommender-upgraded`
3. **Description**: "AI-powered music recommendation system for Chandigarh University - Upgraded Version with user profiles, playlists, and analytics"
4. **Visibility**: Choose **Public** (for university submission) or **Private** (if you prefer)
5. **Initialize with**: Select **Add .gitignore** (choose Python)
6. Click **Create repository**

### Step 2: Clone and Set Up Locally

```bash
# Clone the repository
git clone https://github.com/YOUR-USERNAME/hindi-song-recommender-upgraded.git
cd hindi-song-recommender-upgraded

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

### Step 3: Add All Required Files

Your repository should have this structure:

```
hindi-song-recommender-upgraded/
│
├── app_main.py                    # Main application
├── requirements.txt               # Python dependencies
├── README.md                      # Project documentation
├── LICENSE                        # MIT License
├── .gitignore                     # Git ignore rules
├── streamlit_config.toml          # Streamlit configuration
│
├── config/
│   └── settings.py               # Configuration settings
│
├── data/
│   ├── hindi_songs.csv           # Song dataset (CREATE THIS)
│   └── .gitkeep                  # Placeholder for user_profiles.json
│
├── docs/
│   ├── INSTALLATION.md           # Installation guide
│   ├── USAGE.md                  # Usage guide
│   └── DEPLOYMENT.md             # Deployment guide
│
├── .streamlit/
│   └── config.toml               # Streamlit theme config
│
└── logs/
    └── .gitkeep                  # Placeholder for logs
```

### Step 4: Copy All Files to Your Local Repository

1. **Main Application File** (`app_main.py`)
   - Copy the Python code provided
   - Place in project root

2. **Requirements File** (`requirements.txt`)
   ```
   streamlit==1.28.1
   pandas==2.0.3
   numpy==1.24.3
   scikit-learn==1.3.1
   python-dateutil==2.8.2
   pytz==2023.3
   ```

3. **README.md** - Complete documentation

4. **Configuration** (`config/settings.py`)
   - Copy the settings file
   - Contains all project configuration

5. **Create Directory Structure**:
   ```bash
   mkdir -p data config docs .streamlit logs
   touch data/.gitkeep logs/.gitkeep
   ```

### Step 5: Prepare Your Dataset

1. **Create `data/hindi_songs.csv`** with columns:
   ```
   title,artist,genre,mood,language
   Tum Hi Ho,Arijit Singh,Romantic,Sad,Hindi
   Ae Dil Hai Mushkil,Arijit Singh,Romantic,Emotional,Hindi
   ...
   ```

2. **Options**:
   - Use your existing dataset
   - Create a sample dataset
   - You can add the file locally but exclude from Git using .gitignore

### Step 6: Create Additional Documentation Files

**docs/INSTALLATION.md**
```markdown
# Installation Guide

## Local Setup
1. Clone repository
2. Create virtual environment: `python -m venv venv`
3. Activate venv: `source venv/bin/activate` (macOS/Linux)
4. Install dependencies: `pip install -r requirements.txt`
5. Add hindi_songs.csv to data folder
6. Run: `streamlit run app_main.py`

## Cloud Deployment (Streamlit Cloud)
1. Push code to GitHub
2. Go to https://share.streamlit.io
3. Click "New app"
4. Select your repo
5. Choose app_main.py as main file
```

**docs/USAGE.md**
```markdown
# Usage Guide

## Features
- **Recommendations**: Get personalized song suggestions
- **Playlists**: Create playlists from multiple songs
- **Profile**: Manage favorites and preferences
- **Analytics**: Explore music statistics

## How to Use
1. Select "Recommendations" from navigation
2. Choose a song you like
3. Apply filters (optional)
4. View recommendations with explanations
5. Add to favorites or create playlist
```

**docs/DEPLOYMENT.md**
```markdown
# Deployment Guide

## Streamlit Cloud
1. Create account at share.streamlit.io
2. Deploy directly from GitHub
3. Add secrets if needed

## Docker Deployment
```dockerfile
FROM python:3.9
WORKDIR /app
COPY . .
RUN pip install -r requirements.txt
CMD ["streamlit", "run", "app_main.py"]
```

## Heroku Deployment
Create Procfile:
```
web: sh -c 'pip install -r requirements.txt && streamlit run app_main.py --server.port=$PORT --server.address=0.0.0.0'
```
```

### Step 7: Add Files to Git and Push

```bash
# Add all files
git add .

# Create initial commit
git commit -m "Initial commit: Hindi Song Recommender - Upgraded Version

- Added main Streamlit application with multiple features
- Implemented content-based filtering algorithm
- Added user profiles and playlist generation
- Created analytics dashboard
- Added comprehensive documentation"

# Push to GitHub
git push origin main
```

### Step 8: Push Update with Commit Messages

For future updates, use clear commit messages:

```bash
# Example commit messages:
git commit -m "feature: Add genre and mood filtering"
git commit -m "docs: Update README with installation instructions"
git commit -m "fix: Optimize recommendation algorithm performance"
git commit -m "refactor: Reorganize code structure and configuration"
git commit -m "test: Add sample dataset and test cases"
```

### Step 9: Create GitHub Pages (Optional)

1. Go to repository Settings
2. Under "Pages", select "main" branch and "/root" folder
3. GitHub will generate documentation site

### Step 10: Add Topics and Description

1. Go to repository main page
2. Click "About" (gear icon on right)
3. Add topics:
   - `machine-learning`
   - `recommendation-system`
   - `streamlit`
   - `python`
   - `artificial-intelligence`
   - `chandigarh-university`

### Step 11: Update README with Your GitHub Link

In your README.md, update:
```markdown
1. **Clone the repository**:
   ```bash
   git clone https://github.com/YOUR-USERNAME/hindi-song-recommender-upgraded.git
   ```
```

## Files to Upload Summary

| File | Purpose | Required |
|------|---------|----------|
| app_main.py | Main application | ✅ Yes |
| requirements.txt | Dependencies | ✅ Yes |
| README.md | Documentation | ✅ Yes |
| config/settings.py | Configuration | ✅ Yes |
| .gitignore | Git ignore rules | ✅ Yes |
| LICENSE | MIT License | ✅ Yes |
| streamlit_config.toml | Streamlit config | ⭕ Optional |
| docs/*.md | Additional docs | ⭕ Optional |
| data/hindi_songs.csv | Dataset | ⭕ Add locally |

## Deployment Commands Quick Reference

```bash
# Local development
streamlit run app_main.py

# Deploy to Streamlit Cloud
git push origin main  # Auto-deploys if connected

# Create local backup
git clone https://github.com/YOUR-USERNAME/hindi-song-recommender-upgraded.git backup

# Check git status
git status

# View commit history
git log --oneline

# Undo last commit (before push)
git reset --soft HEAD~1
```

## Troubleshooting

**Issue**: Files not showing up after push
**Solution**: 
```bash
git add -A
git commit -m "Update files"
git push origin main
```

**Issue**: Want to update a file
**Solution**:
```bash
# Edit file
nano app_main.py

# Commit and push
git add app_main.py
git commit -m "Update: Fix in app_main.py"
git push origin main
```

**Issue**: Forgot to add a file
**Solution**:
```bash
# Add file and amend previous commit
git add forgotten_file.py
git commit --amend --no-edit
git push origin main -f  # Force push (use carefully)
```

## Deployment to Streamlit Cloud

1. After pushing to GitHub, go to https://share.streamlit.io
2. Click "New app"
3. Enter: `YOUR-USERNAME/hindi-song-recommender-upgraded`
4. Select `app_main.py` as main file
5. Wait for deployment
6. Share the public URL

Your app will be available at:
`https://hindi-song-recommender-upgraded-USERNAME.streamlit.app`

---

**Ready to Deploy!** 🚀

Once all files are uploaded and pushed, your upgraded Hindi Song Recommender System will be live on GitHub!
