@echo off
echo ==========================================================
echo           STARTING GIT AND DEPLOYMENT RESET SCRIPT
echo ==========================================================
echo.
echo This will fix your Git history and deploy to Hugging Face.
echo It will ask for your Hugging Face login at the very end.
echo.

echo --- Step 1: Deleting corrupted local Git history (.git folder)...
rmdir /s /q .git
echo --- Done.

echo.
echo --- Step 2: Initializing a new, clean Git repository...
git init
echo --- Done.

echo.
echo --- Step 3: Setting up Git LFS...
git lfs install
git lfs track "model/**"
git lfs track "tokenizer/**"
echo --- Done.

echo.
echo --- Step 4: Adding all project files to the new repository...
echo (This will take a moment, it is checking all your files)
git add .
echo --- Done.

echo.
echo --- Step 5: Creating the first clean commit...
git commit -m "Final Project Commit: All Phases Complete"
echo --- Done.

echo.
echo --- Step 6: Setting up the connection to Hugging Face...
git branch -M main
git remote add hf https://huggingface.co/spaces/Khush25/GIT-intelligent-issue-triage
echo --- Done.

echo.
echo --- Step 7: Pushing to Hugging Face...
echo --- A login window may appear. Use your HF username and Access Token.
git push -f hf main

echo.
echo ==========================================================
echo                       SCRIPT FINISHED
echo ==========================================================
echo.
echo If there were no errors above, your project is now deploying on Hugging Face.
echo You can close this window.

pause