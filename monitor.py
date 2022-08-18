#!/usr/bin/env python3

import http.client
import logging
import random
import urllib
import urllib.request
from time import sleep

import config


def pushover(message):
    conn = http.client.HTTPSConnection("api.pushover.net:443")
    conn.request(
        "POST",
        "/1/messages.json",
        urllib.parse.urlencode(
            {
                "token": config.pushovertoken,
                "user": config.pushoveruser,
                "html": 1,
                "message": message,
            }
        ),
        {"Content-type": "application/x-www-form-urlencoded"},
    )
    conn.getresponse()


def checkstatus(notifiedfunc,producturl):
    logging.info("Checking URL.")
    try:
        request_url = urllib.request.urlopen(producturl).read()
    except "FailedConnect":
        logging.error("Failed to connect to URL.")

    request_url = request_url.decode("utf-8")
    if (
        '<span class="comProductTile__soldOut add8top">Sold Out</span>'
        not in request_url
    ):
        if notifiedfunc is False:
            logging.info(
                config.item_description
                + " is in stock. Notified is false. Sending notification."
            )
            pushover(
                config.item_description
                + " is in stock: <a href = '"
                + config.producturl
                + "'>Click Here!</a>"
            )
            return True
        else:
            logging.info(
                config.item_description
                + " still in stock. Notified is true. Skipping notification."
            )
    else:
        logging.info(config.item_description + " is out of stock.")
        return False


def main():
    producturl = config.producturl

    # Logging setup. Use loging.info('text') to log something
    # with a timestamp at info level

    logging.basicConfig(
        format="%(asctime)s %(levelname)-3s: %(message)s",
        filename="./monitor.log",
        level=logging.INFO,
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    notified = False

    logging.info("monitor.py has started.")
    logging.info("Monitoring for \"" + config.item_description + "\" at URL " + config.producturl)
    while True:
        seconds = random.randint(config.mintime, config.maxtime)
        logging.info("Sleeping " + str(seconds) + " seconds.")
        sleep(seconds)
        notified = checkstatus(notified, producturl)
        continue


if __name__ == "__main__":
    main()
