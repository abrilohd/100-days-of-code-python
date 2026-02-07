# utils/scheduler.py
import os
import sys
import time
import schedule

# make sure project root is on sys.path so imports work when running scheduler directly
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from main import run_flight_check

def job():
    print("[scheduler] Running scheduled job...")
    run_flight_check()

def start_scheduler(run_time="08:00"):
    print(f"[scheduler] Scheduler started, will run daily at {run_time}")
    schedule.every().day.at(run_time).do(job)
    while True:
        schedule.run_pending()
        time.sleep(30)

if __name__ == "__main__":
    start_scheduler()
