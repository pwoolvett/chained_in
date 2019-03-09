# coding=utf-8
"""download linkedin profiles"""
import os

from requests import get
from bs4 import BeautifulSoup

from chained_in.settings import LINKEDIN_PAGE, DATA


def get_profile(profile_id=LINKEDIN_PAGE, force=False):

    output = os.path.join(DATA, profile_id) + ".html"

    if force or not os.path.isfile(output):
        url = f"https://www.linkedin.com/in/{profile_id}"
        response = get(url)
        enc = response.__dict__["encoding"]
        data = response.content.decode(enc)

        with open(output, "w") as file:
            file.write(data)

    else:
        with open(output, "r") as file:
            data = file.read()

    return data


if __name__ == "__main__":
    get_profile()
