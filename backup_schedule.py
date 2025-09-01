import schedule
import time

def daily_backup():
    upload_db_to_drive('attendance_system.db', f'backup_{time.strftime("%Y%m%d")}.db')

schedule.every().day.at("02:00").do(daily_backup)  # Runs at 2 AM daily

while True:
    schedule.run_pending()
    time.sleep(60)