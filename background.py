import time, threading
from config import CHECK_INTERVAL
from email_handler import check_inbox

def start_mail_listener():
    while True:
        try:
            check_inbox()
        except Exception as e:
            print("Error checking inbox:", e)
        time.sleep(CHECK_INTERVAL)

def run_in_background():
    threading.Thread(target=start_mail_listener, daemon=True).start()
