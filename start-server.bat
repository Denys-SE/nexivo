@echo off
cd /d "%~dp0"
echo Starting Nexivo Sourcing local website...
echo.
echo Open this URL in your browser:
echo http://127.0.0.1:4173
echo.
echo Keep this window open while viewing the website.
echo Press Ctrl+C to stop the server.
echo.
node dev-server.js
pause
