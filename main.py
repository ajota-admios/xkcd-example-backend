import requests
from bs4 import BeautifulSoup

import random
import json
import os
import sys

xkcd_base_url = "https://xkcd.com"

def make_xkcd_home_url():
    return xkcd_base_url

def make_xkcd_entry_url(entry_id):
    return xkcd_base_url + "/{0}".format(entry_id)

def request_with_url(url):
    result = requests.get(url)

    status_code = result.status_code
    if status_code != 200:
        raise Exception("Request failed to get contents from: {0} with HTTP status code: {1}".format(url, status_code))

    content_type = result.headers["content-type"]
    if content_type != "text/html":
        raise Exception("Request returned contents from: {0} with Content-Type: {1}".format(url, content_type))

    return result.content

def make_soup_from_url_request_content(content):
    return BeautifulSoup(content, "lxml")

def get_latest_xkcd_entry_id():
    soup = make_soup_from_url_request_content(request_with_url(make_xkcd_home_url()))

    previous_xkcd_entry_tag = soup.find(attrs={"rel": "prev"})
    previous_xkcd_entry_id = int(previous_xkcd_entry_tag["href"][1:-1])

    latest_xkcd_entry_id = previous_xkcd_entry_id + 1

    return latest_xkcd_entry_id

def get_xkcd_entry_with_id(entry_id):
    soup = make_soup_from_url_request_content(request_with_url(make_xkcd_entry_url(entry_id)))

    title = soup.find(id="ctitle").string
    image_url = "https:" + soup.find(id="comic").img["src"]

    xkcd_entry = {
        "title": title,
        "image_url": image_url
    }

    return xkcd_entry

def save_json_file(path, payload):
    with open(path, "w") as json_file:
        json.dump(payload, json_file, indent=2)

def make_random_xkcd_entries_file(number_of_random_entries=10):
    latest_xkcd_entry_id = get_latest_xkcd_entry_id()

    random_xkcd_entry_ids_set = set()
    random_xkcd_entries = []

    while len(random_xkcd_entries) < number_of_random_entries:

        random_xkcd_entry_id = random.randrange(1, latest_xkcd_entry_id + 1)

        if random_xkcd_entry_id in random_xkcd_entry_ids_set:
            continue

        xkcd_entry = get_xkcd_entry_with_id(random_xkcd_entry_id)

        random_xkcd_entry_ids_set.add(random_xkcd_entry_id)
        random_xkcd_entries.append(xkcd_entry)

    return random_xkcd_entries

if __name__ == "__main__":
    filename = "/var/app/build/xkcd-entries.json"

    os.makedirs(os.path.dirname(filename), exist_ok=True)
    save_json_file(filename, make_random_xkcd_entries_file())

    sys.exit()
