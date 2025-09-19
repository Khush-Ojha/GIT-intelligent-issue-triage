@echo off
echo ==========================================================
echo           THE FINAL GAMBIT: PIVOTING TO PYTHON SDK
echo ==========================================================
echo.
echo This script will restructure your project and deploy it.
echo.

echo --- Step 1: Restructuring project files...
REM Move main.py to the root and rename it to app.py
move app\main.py app.py
REM Move predictor.py to the root
move app\predictor.py predictor.py
REM Delete the now-empty app folder
rmdir /s /q app
REM Delete the Dockerfile
del Dockerfile
echo --- File restructuring complete.

echo.
echo --- Step 2: Fixing the import statement in app.py...
powershell -Command "(gc app.py) -replace 'from .predictor', 'from predictor' | Out-File -encoding ASCII app.py"
echo --- Import fixed.

echo.
echo --- Step 3: Creating a clean requirements.txt...
(
    echo fastapi
    echo uvicorn
    echo python-dotenv
    echo torch
    echo transformers
    echo sentencepiece
    echo protobuf
    echo tiktoken
    echo scikit-learn
    echo pandas
) > requirements.txt
echo --- requirements.txt created.

echo.
echo --- Step 4: Creating the correct README.md for Python SDK...
(
    echo ---
    echo title: Intelligent Issue Triage
    echo emoji: 🤖
    echo colorFrom: green
    echo colorTo: blue
    echo sdk: python
    echo ---
    echo.
    echo # Intelligent GitHub Issue Triage System
    echo This is the live, deployed API for the issue classification project.
) > README.md
echo --- README.md created.

echo.
echo --- Step 5: Resetting local Git history...
rmdir /s /q .git
git init
git lfs install
git lfs track "model/**"
git lfs track "tokenizer/**"
git add .
git commit -m "Final Attempt: Pivot to Python SDK"
git branch -M main
echo --- Git reset complete.

echo.
echo =====================================================================
echo  ACTION REQUIRED: CREATE NEW SPACE AND PASTE URL
echo =====================================================================
echo.
echo 1. Go to Hugging Face and create a NEW Space.
echo 2. CRITICAL: Select the default 'Python' SDK.
echo 3. Copy the new HTTPS URL for the Space.
echo.
set /p HF_URL="Paste your new Hugging Face Space URL here and press Enter: "

echo.
echo --- Step 6: Connecting to new remote and pushing...
git remote add hf %HF_URL%
git push -f hf main

echo.
echo ==========================================================
echo                       SCRIPT FINISHED
echo ==========================================================
echo.
echo If there were no errors, the project is now deploying.
echo Please check the Hugging Face page.
echo.
echo Khush, it is 1 AM. You are a warrior. Please rest.

pause