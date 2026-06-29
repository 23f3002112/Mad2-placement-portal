from celery import Celery
from celery.schedules import crontab

celery = Celery(
    'ppa', 
    broker='redis://localhost:6379/0', 
    backend='redis://localhost:6379/0',
    include=['tasks']
)

celery.conf.enable_utc = True

# Celery Beat schedule
celery.conf.beat_schedule = {
    'daily-interview-reminders': {
        'task': 'tasks.send_interview_reminders',
        'schedule': crontab(hour=8, minute=0), # Every day at 8:00 AM
    },
    'monthly-placement-reports': {
        'task': 'tasks.generate_monthly_reports',
        'schedule': crontab(0, 0, day_of_month='1'), # 1st day of every month at midnight
    }
}
