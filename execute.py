import os
import time
import schedule


def exec_hcheck():
    os.system('python h_batch.py')


# GMT +9 05:00
# server time is GMT 0
schedule.every().day.at("20:00").do(exec_hcheck)

while True:
    schedule.run_pending()
    # interval: 1 min
    time.sleep(60)
# use kill -term PID
