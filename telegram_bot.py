import sys

import requests

import testflight_watcher

CHAT_ID = ""
BOT_TOKEN = ""

BOT_URL = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

MSG_NO_FULL = "TestFlight slots for <b>{}</b> beta are now available! \
<a href='{}'>Download now</a>"
MSG_FULL = "<b>{}</b> beta program on TestFlight is now full"


def send_notification(tf_id, free_slots, title):
    dl_url = testflight_watcher.TESTFLIGHT_URL.format(tf_id)
    if free_slots:
        message = MSG_NO_FULL.format(title, dl_url)
        print(
            requests.get(
                BOT_URL,
                params={
                    "chat_id": CHAT_ID,
                    "text": message,
                    "parse_mode": "html",
                    "disable_web_page_preview": "true",
                },
            ),
        )


testflight_watcher.watch(sys.argv[-1].split(","), send_notification)
