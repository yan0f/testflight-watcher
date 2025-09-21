#!/usr/bin/env python3

import re
from collections.abc import Callable

import requests
from lxml import html

XPATH_STATUS = '//*[@class="beta-status"]/span/text()'
XPATH_TITLE = "/html/head/title/text()"
TITLE_REGEX = r"Join the (.+) beta - TestFlight - Apple"
TESTFLIGHT_URL = "https://testflight.apple.com/join/{}"
FULL_TEXTS = [
    "This beta is full.",
    "This beta isn't accepting any new testers right now.",
]


def watch(
    watch_ids: list[str],
    callback: Callable,
    notify_full: bool = True,
    sleep_time: int = 900,
) -> None:
    data = {}
    for tf_id in watch_ids:
        req = requests.get(
            TESTFLIGHT_URL.format(tf_id),
            headers={"Accept-Language": "en-us"},
        )
        page = html.fromstring(req.text)
        free_slots = page.xpath(XPATH_STATUS)[0] not in FULL_TEXTS
        if tf_id not in data or data[tf_id] != free_slots:
            if free_slots or notify_full:
                title = re.findall(TITLE_REGEX, page.xpath(XPATH_TITLE)[0])[0]
                callback(tf_id, free_slots, title)
            data[tf_id] = free_slots
