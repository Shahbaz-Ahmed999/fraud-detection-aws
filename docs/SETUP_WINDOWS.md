# 🔧 Windows Setup Guide
## Complete Environment Configuration for Fraud Detection Project

---

## ✅ STEP-BY-STEP SETUP (Windows 11)

### ✓ Prerequisites Check

You already have:
- ✅ Python 3.13.5
- ✅ pip 25.2
- ✅ Git 2.53.0
- ✅ VS Code (installed)

**You're ready to proceed!**

---

## 📂 STEP 1: DOWNLOAD PROJECT FILES

### Option A: Using Git Clone (Recommended after GitHub upload)

```cmd
# Navigate to your projects folder
cd C:\Users\SK Traders\Documents

# Clone the repository (after you push to GitHub)
git clone https://github.com/YOUR_USERNAME/fraud-detection-aws.git

# Enter project directory
cd fraud-detection-aws
```

### Option B: Manual Setup (Use this NOW)

1. **Download all project files I've created for you**
   - Download the `.gitignore`, `README.md`, `requirements.txt`, `setup.bat`
   - Download the `docs/` folder with all 3 documents
   - Download the `src/` folder structure

2. **Create folder structure manually:**

```cmd
# Navigate to your projects folder
cd C:\Users\SK Traders\Documents

# Create main project folder
mkdir fraud-detection-aws
cd fraud-detection-aws

# Create folder structure
mkdir docs data notebooks src models deployment tests aws
mkdir data\raw data\processed data\interim
mkdir notebooks\exploratory notebooks\modeling
mkdir src\data src\models src\evaluation src\api
mkdir deployment\lambda deployment\ec2 deployment\streamlit
mkdir models\saved_models models\checkpoints
mkdir tests
mkdir aws\scripts
```

3. **Copy downloaded files into this structure**

---

## 🐍 STEP 2: SETUP PYTHON ENVIRONMENT

### 2.1 Create Virtual Environment

```cmd
# Make sure you're in the project folder
cd C:\Users\SK Traders\Documents\fraud-detection-aws

# Create virtual environment
python -m venv venv
```

**What is a virtual environment?**
- Isolated Python installation for this project
- Prevents package conflicts with other projects
- Professional best practice

### 2.2 Activate Virtual Environment

```cmd
# Activate (Windows)
venv\Scripts\activate
```

**You'll see (venv) before your command prompt:**
```
(venv) C:\Users\SK Traders\Documents\fraud-detection-aws>
```

**To deactivate later (when done):**
```cmd
deactivate
```

### 2.3 Upgrade pip

```cmd
python -m pip install --upgrade pip
```

### 2.4 Install Project Dependencies

```cmd
pip install -r requirements.txt
```

**This installs:**
- pandas, numpy (data manipulation)
- scikit-learn, xgboost, lightgbm (ML models)
- boto3 (AWS SDK)
- fastapi (API development)
- jupyter (notebooks)
- shap (explainability)
- And 30+ other packages

**Expected time:** 5-10 minutes

---

## 🎯 ALTERNATIVE: AUTOMATED SETUP (EASIER!)

Instead of manual steps, you can run the automated setup script:

```cmd
# Navigate to project folder
cd C:\Users\SK Traders\Documents\fraud-detection-aws

# Run setup script
setup.bat
```

This script:
1. ✅ Checks Python installation
2. ✅ Checks pip installation
3. ✅ Creates virtual environment
4. ✅ Activates environment
5. ✅ Upgrades pip
6. ✅ Installs all dependencies

---

## 📊 STEP 3: DOWNLOAD DATASET

### 3.1 Create Kaggle Account (Free)

1. Go to: https://www.kaggle.com/
2. Click "Register" (top right)
3. Sign up with Google/email (free)

### 3.2 Download Dataset

1. Go to: https://www.kaggle.com/mlg-ulb/creditcardfraud
2. Click "Download" button
3. Save `creditcard.csv` to Downloads folder

### 3.3 Move Dataset to Project

```cmd
# Create data/raw folder (if not exists)
mkdir data\raw

# Move file (adjust path to your Downloads folder)
move C:\Users\SK Traders\Downloads\creditcard.csv data\raw\
```

**Verify:**
```cmd
dir data\raw\
```

You should see `creditcard.csv` (~150 MB)

---

## 💻 STEP 4: VERIFY INSTALLATION

### 4.1 Check Python Packages

```cmd
# Activate environment first
venv\Scripts\activate

# Check installations
python -c "import pandas; print(f'pandas: {pandas.__version__}')"
python -c "import sklearn; print(f'scikit-learn: {sklearn.__version__}')"
python -c "import xgboost; print(f'xgboost: {xgboost.__version__}')"
python -c "import boto3; print(f'boto3: {boto3.__version__}')"
```

**Expected output (versions may vary):**
```
pandas: 2.0.0
scikit-learn: 1.3.0
xgboost: 2.0.0
boto3: 1.28.0
```

### 4.2 Launch Jupyter Notebook

```cmd
jupyter notebook
```

**This should:**
1. Start Jupyter server
2. Open browser automatically
3. Show project folder structure

**Test it:**
- Create new notebook
- Run: `import pandas as pd`
- If no error → Success! ✅

---

## 🌐 STEP 5: SETUP AWS ACCOUNT (Next)

We'll do this together in detail. For now, just be aware you'll need:

1. **AWS Account** (free, requires credit card for verification but won't be charged)
2. **AWS Access Keys** (for programmatic access)
3. **AWS CLI Configuration**

**Don't worry - I'll guide you through every step when we get there!**

---

## 🔐 STEP 6: CONFIGURE GIT

### 6.1 Set Your Identity

```cmd
# Your name (for commit messages)
git config --global user.name "Your Full Name"

# Your email (use same as GitHub)
git config --global user.email "your.email@example.com"
```

### 6.2 Initialize Repository

```cmd
# Initialize Git in project folder
git init

# Add all files
git add .

# First commit
git commit -m "Initial commit: Project structure and documentation"
```

### 6.3 Connect to GitHub (After Creating Repository)

```cmd
# Add remote (replace with your GitHub username)
git remote add origin https://github.com/YOUR_USERNAME/fraud-detection-aws.git

# Push to GitHub
git branch -M main
git push -u origin main
```

---

## 📝 STEP 7: OPEN PROJECT IN VS CODE

### 7.1 Open Folder

1. Open VS Code
2. File → Open Folder
3. Select: `C:\Users\SK Traders\Documents\fraud-detection-aws`

### 7.2 Select Python Interpreter

1. Press `Ctrl+Shift+P`
2. Type: "Python: Select Interpreter"
3. Choose: `.\venv\Scripts\python.exe`

### 7.3 Install VS Code Extensions (Recommended)

- **Python** (by Microsoft)
- **Pylance** (by Microsoft)
- **Jupyter** (by Microsoft)
- **GitLens** (by GitKraken)
- **Python Indent** (by Kevin Rose)

---

## ✅ VERIFICATION CHECKLIST

Run through this checklist:

- [ ] Project folder created: `fraud-detection-aws/`
- [ ] All folders created (docs, data, src, etc.)
- [ ] Virtual environment created: `venv/`
- [ ] Virtual environment activated (see `(venv)` in terminal)
- [ ] All packages installed from `requirements.txt`
- [ ] Dataset downloaded: `data/raw/creditcard.csv`
- [ ] Jupyter notebook launches successfully
- [ ] Git initialized and first commit made
- [ ] VS Code opened with project folder
- [ ] Python interpreter set to virtual environment

---

## 🚨 TROUBLESHOOTING

### Issue: "Python not found"
**Solution:**
```cmd
# Check PATH
where python

# If not found, add Python to PATH:
# Settings → System → Advanced → Environment Variables
# Add: C:\Users\SK Traders\AppData\Local\Programs\Python\Python313
```

### Issue: "pip install fails"
**Solution:**
```cmd
# Try with --user flag
pip install --user package_name

# Or upgrade pip first
python -m pip install --upgrade pip
```

### Issue: "Virtual environment won't activate"
**Solution:**
```cmd
# Use full path
C:\Users\SK Traders\Documents\fraud-detection-aws\venv\Scripts\activate.bat

# If still fails, recreate environment
rmdir /s venv
python -m venv venv
```

### Issue: "Jupyter won't start"
**Solution:**
```cmd
# Reinstall jupyter
pip uninstall jupyter jupyterlab
pip install jupyter jupyterlab

# Start with full path
python -m jupyter notebook
```

### Issue: "Import errors in notebooks"
**Solution:**
```cmd
# Make sure virtual environment is activated
venv\Scripts\activate

# Install ipykernel
pip install ipykernel

# Add kernel
python -m ipykernel install --user --name=fraud-detection
```

---

## 🎯 NEXT STEPS

Once setup is complete, you're ready for:

1. **AWS Account Setup** (Step-by-step guide coming)
2. **Data Exploration** (Phase 2)
3. **Model Training** (Phase 4)

---

## 📞 QUICK REFERENCE

### Essential Commands

```cmd
# Activate environment
cd C:\Users\SK Traders\Documents\fraud-detection-aws
venv\Scripts\activate

# Deactivate environment
deactivate

# Install new package
pip install package_name

# Update requirements.txt after installing new package
pip freeze > requirements.txt

# Launch Jupyter
jupyter notebook

# Run Python script
python src/models/train.py

# Git commands
git status
git add .
git commit -m "Your message"
git push
```

### Folder Quick Access

```cmd
# Data
cd data\raw

# Notebooks
cd notebooks\exploratory

# Source code
cd src\models

# Models
cd models\saved_models
```

---

## 📚 RESOURCES

### Documentation
- Python: https://docs.python.org/3/
- pandas: https://pandas.pydata.org/docs/
- scikit-learn: https://scikit-learn.org/stable/
- XGBoost: https://xgboost.readthedocs.io/
- FastAPI: https://fastapi.tiangolo.com/

### Tutorials
- Git: https://git-scm.com/book/en/v2
- VS Code: https://code.visualstudio.com/docs
- Jupyter: https://jupyter.org/documentation

---

**Setup Guide Version**: 1.0  
**Last Updated**: April 2026  
**Platform**: Windows 11  
**Python Version**: 3.13.5
