@echo off
REM Host has no PHP; skip wayfinder generate (types already on disk).
if /I "%~1"=="artisan" if /I "%~2"=="wayfinder:generate" exit /b 0
docker exec -w /var/www/html hiraya-review-app php %*
