from apscheduler.schedulers.background import BackgroundScheduler
from notifier import run_check

scheduler = BackgroundScheduler()

scheduler.add_job(run_check, 'cron', hour=0)

if __name__ == '__main__':
    scheduler.start()
    try:
        while True:
            pass
    except (KeyboardInterrupt, SystemExit):
        scheduler.shutdown()
