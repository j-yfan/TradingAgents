import schedule
import time
import sys
from main import run_daily_workflow

def job():
    """Wrapper function for the daily workflow."""
    print(f"Scheduler triggered at {time.ctime()}. Running daily workflow...")
    run_daily_workflow()
    print("Daily workflow complete. Waiting for next scheduled run.")

# --- Configure the Schedule ---
# Schedule the job to run every day at a specific time.
# Adjust the time as needed, e.g., before market open.
# Example: "08:00" for 8:00 AM system time.
SCHEDULE_TIME = "08:00" 
schedule.every().day.at(SCHEDULE_TIME).do(job)

# You can also schedule for testing purposes, e.g., every 5 minutes
# schedule.every(5).minutes.do(job)

if __name__ == '__main__':
    print("Starting the LLM Trading Bot Scheduler.")
    print(f"The daily trading workflow is scheduled to run at {SCHEDULE_TIME} every day.")
    print("Press Ctrl+C to exit.")

    # Run the job once immediately on startup if desired
    # job() 
    
    try:
        while True:
            schedule.run_pending()
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nScheduler stopped by user.")
        sys.exit(0)
