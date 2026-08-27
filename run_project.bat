@echo off
title AI-Based House Price Prediction System - Launcher
echo ======================================================================
echo    AI-BASED HOUSE PRICE PREDICTION SYSTEM
echo    Integrated Machine Learning + Java Spring Boot + Web Frontend
echo ======================================================================
echo.

echo [1/3] Starting Python ML Prediction Microservice on Port 5001...
start "Python ML Service (Port 5001)" cmd /k "python ml_service\app.py"
timeout /t 3 /nobreak > nul

echo [2/3] Starting Java Spring Boot Backend on Port 8080...
start "Spring Boot Backend (Port 8080)" cmd /k "cd backend && java -jar target\house-price-prediction-backend-1.0.0.jar"
timeout /t 6 /nobreak > nul

echo [3/3] Launching Web Application in Default Browser...
start http://localhost:8080/

echo.
echo ======================================================================
echo  System is up and running!
echo  - Web Application: http://localhost:8080/
echo  - Spring Boot REST APIs: http://localhost:8080/api/predict
echo  - Python ML Service: http://localhost:5001/predict
echo  - H2 DB Console: http://localhost:8080/h2-console
echo ======================================================================
pause
