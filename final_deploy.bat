@echo off
echo.
echo ### FINAL DEPLOYMENT SCRIPT ###
echo This will reset your Git history and deploy a clean version.
echo.

echo --- Deleting old local Git history...
IF EXIST .git (rmdir /s /q .git)

echo --- Initializing new repository and LFS...
git init
git lfs install
git lfs track "model/**"
git lfs track "tokenizer/**"

echo --- Committing all project files...
git add .
git commit -m "Final version for deployment"
git branch -M main

echo.
echo ### ACTION REQUIRED ###
echo 1. Go to Hugging Face and DELETE your old Space.
echo 2. Create a NEW Space. CRITICAL: Select the 'Docker' SDK.
echo 3. Copy the new HTTPS URL for the Space.
echo.
set /p HF_URL="Paste the URL for your NEW DOCKER Space and press Enter: "

echo.
echo --- Connecting to new remote and pushing...
git remote add hf %HF_URL%
git push -f hf main

echo.
echo ### DEPLOYMENT PUSH COMPLETE ###
echo Go to your Hugging Face page. It should now be 'Building...'.
pause