@echo off
title SDA Media Server - Media SDA Ambolokandrina
echo ============================================
echo   MEDIA SDA AMBOLOKANDRINA - Mode Etendre
echo ============================================
echo.
echo  Serveur local demarre sur http://localhost:8000
echo  Ouvrez Chrome, faites Windows+P -> Etendre
echo  Puis cliquez le bouton Projeter (bas-droite)
echo.
echo  Pour arreter : fermez cette fenetre ou Ctrl+C
echo ============================================
echo.
cd /d "%~dp0"
py -m http.server 8000 --directory "%~dp0" --bind 127.0.0.1
pause
