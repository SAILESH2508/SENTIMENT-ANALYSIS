# 🚀 Streamlit Cloud Deployment - Step by Step

## 📋 Pre-Deployment Checklist ✅
- [x] Model file ready (`sentiment_pipeline.pkl`)
- [x] Streamlit app ready (`streamlit_app.py`)
- [x] Requirements file ready (`requirements_streamlit.txt`)
- [x] All files checked and working

## 🔧 Step 1: Create GitHub Repository

### Option A: Using GitHub Website (Easiest)
1. Go to https://github.com/new
2. Repository name: `sentiment-analyzer` (or your preferred name)
3. Description: `Universal Sentiment Analyzer - AI-powered text sentiment analysis`
4. Set to **Public** (required for free Streamlit Cloud)
5. ✅ Add README file
6. Click "Create repository"

### Option B: Using Git Commands
```bash
# Initialize git (if not done)
git init

# Add all files
git add .

# Commit
git commit -m "Universal Sentiment Analyzer v2.0 - Ready for deployment"

# Add remote (replace YOUR_USERNAME)
git remote add origin https://github.com/YOUR_USERNAME/sentiment-analyzer.git

# Push to GitHub
git branch -M main
git push -u origin main
```

## 🌐 Step 2: Deploy on Streamlit Cloud

1. **Go to Streamlit Cloud:**
   - Visit: https://share.streamlit.io/
   - Click "Sign in with GitHub"
   - Authorize Streamlit to access your repositories

2. **Create New App:**
   - Click "New app" button
   - Select "From existing repo"

3. **Configure Deployment:**
   - **Repository:** Select your `sentiment-analyzer` repo
   - **Branch:** `main`
   - **Main file path:** `streamlit_app.py`
   - **App URL:** Choose your custom URL (optional)

4. **Advanced Settings (Optional):**
   - **Python version:** 3.11 (recommended)
   - **Requirements file:** Will auto-detect `requirements_streamlit.txt`

5. **Deploy:**
   - Click "Deploy!" button
   - Wait 2-5 minutes for deployment

## 🎉 Step 3: Your App is Live!

Your app will be available at:
`https://YOUR_USERNAME-sentiment-analyzer-streamlit-app-RANDOM.streamlit.app/`

## 🔧 Troubleshooting

### If deployment fails:
1. **Check logs** in Streamlit Cloud dashboard
2. **Common issues:**
   - Model file too large (>100MB) - Use Git LFS
   - Missing dependencies - Check requirements file
   - Import errors - Verify all files uploaded

### Model file too large?
```bash
# Use Git LFS for large files
git lfs track "*.pkl"
git add .gitattributes
git add sentiment_pipeline.pkl
git commit -m "Add model with LFS"
git push
```

## 🎯 Success Indicators:
- ✅ App loads without errors
- ✅ Model loads successfully
- ✅ Predictions work correctly
- ✅ All tabs functional

## 🔄 Updates:
To update your app:
1. Make changes locally
2. `git add .` and `git commit -m "Update"`
3. `git push`
4. Streamlit Cloud auto-deploys changes!

## 📊 Features Available:
- 🔍 Single text analysis
- 📊 Batch CSV file analysis
- ℹ️ Model information
- 📈 Sentiment distribution charts
- 📥 Download results

Your sentiment analyzer is now live and accessible worldwide! 🌍