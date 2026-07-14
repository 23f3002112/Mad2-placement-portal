@echo off
echo ==============================================
echo [NOTE] Remember to run MailHog in a separate terminal!
echo [NOTE] View emails at http://localhost:8025
echo ==============================================

echo Starting Redis...
REM Assuming Redis is installed or via WSL. If using Windows Redis, start it here.
REM For example: start redis-server

echo Starting Celery Worker...
start "Celery Worker" cmd /c "celery -A celery_app.celery worker --loglevel=info --pool=solo"

echo Starting Celery Beat...
start "Celery Beat" cmd /c "celery -A celery_app.celery beat --loglevel=info"

echo Workers started in separate windows!
pause
