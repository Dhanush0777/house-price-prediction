@echo off
setlocal enabledelayedexpansion

echo =======================================================
echo     AI-Based House Price Prediction - GitHub Deploy
echo =======================================================
echo.

:: Add Git to PATH if freshly installed
if exist "C:\Program Files\Git\cmd\git.exe" (
    set "PATH=C:\Program Files\Git\cmd;%PATH%"
)

where git >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo [!] Git is not found in PATH. Please install Git or restart VS Code.
    pause
    exit /b 1
)

echo [*] Initializing Git repository...
git init

echo [*] Adding files to staging...
git add .

echo [*] Creating initial commit...
git commit -m "Initial commit: AI-Based House Price Prediction & Real Estate Valuation System"

echo.
echo =======================================================
echo   Next: Link to your GitHub repository
echo =======================================================
echo 1. Go to: https://github.com/new
echo 2. Name your repository (e.g. house-price-prediction)
echo 3. Do NOT check 'Initialize with README'
echo 4. Copy your repository URL (e.g. https://github.com/YOUR_USERNAME/house-price-prediction.git)
echo.
set /p REPO_URL="Enter your GitHub Repository URL: "

if "%REPO_URL%"=="" (
    echo [!] No URL provided. You can push manually later with:
    echo     git remote add origin YOUR_URL
    echo     git branch -M main
    echo     git push -u origin main
    pause
    exit /b 0
)

echo [*] Setting remote origin to %REPO_URL% ...
git remote remove origin >nul 2>&1
git remote add origin %REPO_URL%
git branch -M main

echo [*] Pushing code to GitHub main branch...
git push -u origin main

echo.
echo =======================================================
echo [+] Successfully pushed project to GitHub!
echo =======================================================
echo.
echo To enable GitHub Pages (Live Demo Link):
echo 1. In your GitHub repo, go to: Settings -^> Pages
echo 2. Under 'Branch', select 'main' and '/ (root)' or '/frontend'
echo 3. Click 'Save'
echo 4. Your live link will be: https://YOUR_USERNAME.github.io/REPO_NAME/
echo.
pause
