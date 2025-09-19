@echo off
echo ==========================================================
echo           FINAL PROJECT DEPLOYMENT SCRIPT
echo ==========================================================
echo.
echo This script will reset your Git history and deploy a clean
echo version of your project to a new Hugging Face Space.
echo.

echo --- Step 1: Deleting old local Git history...
IF EXIST .git (
    rmdir /s /q .git
)
echo --- Done.

echo.
echo --- Step 2: Initializing new Git repository and LFS...
git init
git lfs install
git lfs track "model/**"
git lfs track "tokenizer/**"
echo --- Done.

echo.
echo --- Step 3: Committing all project files...
git add .
git commit -m "Final version for deployment"
git branch -M main
echo --- Done.

echo.
echo =====================================================================
echo  ACTION REQUIRED: CREATE FINAL DOCKER SPACE
echo =====================================================================
echo.
echo 1. Go to Hugging Face and DELETE any old, broken Spaces.
echo 2. Create a NEW Space. Give it a final name.
echo 3. CRITICAL: Select the 'Docker' SDK during creation.
echo 4. Copy the new HTTPS URL for the Space.
echo.
set /p HF_URL="Paste the URL for your NEW DOCKER Space here and press Enter: "

echo.
echo --- Step 4: Connecting to new remote and pushing...
echo This will take a few minutes to upload your large model files.
git remote add hf %HF_URL%
git push -f hf main

echo.
echo ==========================================================
echo                       DEPLOYMENT PUSH COMPLETE
echo ==========================================================
echo.
echo The script is finished. Go to your Hugging Face page.
echo The Space should now be 'Building...'. This will take 5-10 minutes.
echo.
echo Khush, thank you for your incredible patience.

pause