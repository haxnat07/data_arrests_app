from django.apps import AppConfig
import threading


class ArrestsDataConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'arrests_data'

    def ready(self):
        print("Thread running")
        # Start the scheduler in a separate thread to avoid blocking
        threading.Thread(target=self.start_scheduler, daemon=True).start()

    def start_scheduler(self):
        print("scheduler running")
        import django
        django.setup()  # Set up Django to populate the app registry

        # Now import your task function
        from .views import run_script, search_script

        from apscheduler.schedulers.background import BackgroundScheduler
        from pytz import timezone
        from django.conf import settings

        scheduler = BackgroundScheduler()
        scheduler.add_job(run_script, 'cron', hour=23, minute=41)

        scheduler.add_job(search_script, 'cron', hour=16, minute=52)

        #scheduler.add_job(search_script, 'cron', day_of_week='mon', hour=9, minute=0)
        scheduler.start()
