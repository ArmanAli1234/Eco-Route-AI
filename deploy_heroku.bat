@echo off
REM EcoRoute AI - Heroku deploy script
REM Run this AFTER: heroku login (once)

echo.
echo ========================================
echo   EcoRoute AI - Deploying to Heroku
echo ========================================
echo.

cd /d "%~dp0"

REM App name (change if taken): https://ecoroute-ai-msme.herokuapp.com
set APPNAME=ecoroute-ai-msme

REM Check Heroku CLI
where heroku >nul 2>&1
if errorlevel 1 (
    echo ERROR: Heroku CLI not found.
    echo Install it from: https://devcenter.heroku.com/articles/heroku-cli
    echo Then run: heroku login
    pause
    exit /b 1
)

REM Git init and commit if needed
if not exist .git (
    echo Initializing git...
    git init
)

git add -A
git status
git commit -m "Deploy EcoRoute AI to Heroku" 2>nul || git commit --allow-empty -m "Deploy EcoRoute AI to Heroku"

REM Create Heroku app (skip if already linked)
heroku apps:info -a %APPNAME% >nul 2>&1
if errorlevel 1 (
    echo Creating Heroku app: %APPNAME%
    heroku create %APPNAME%
) else (
    echo Using existing app: %APPNAME%
)

REM Set remote and push
git remote add heroku https://git.heroku.com/%APPNAME%.git 2>nul
heroku git:remote -a %APPNAME% 2>nul

echo.
echo Pushing to Heroku (this may take 2-3 minutes)...
echo

git push heroku main 2>nul || git push heroku master 2>nul || (
    echo If push failed, try: git push heroku HEAD:main
    git push heroku HEAD:main
)

if errorlevel 1 (
    echo.
    echo Push failed. Make sure you ran: heroku login
    pause
    exit /b 1
)

echo.
echo ========================================
echo   DEPLOY DONE
echo ========================================
echo.
echo   Your app link:
echo   https://%APPNAME%.herokuapp.com
echo.
echo   Opening in browser...
echo.
start https://%APPNAME%.herokuapp.com

heroku open
pause
