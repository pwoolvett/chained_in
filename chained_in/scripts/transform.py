# coding=utf-8
"""Transform already obtained html files"""
import os
import re
import json
from typing import List

import requests
from bs4 import BeautifulSoup

from chained_in.settings import LINKEDIN_PAGE, DATA, SKIP_URLS
from chained_in.scripts.extract import get_profile

REGEX_URL = re.compile(r'https?://\S+',re.IGNORECASE|re.MULTILINE)
""" See https://github.com/django/django/blob/master/django/core/validators.py#L74"""

UGLY_SPACES_RE = re.compile(r"\s+")

URLS_TO_SKIP = ','.split(SKIP_URLS)

def get_img_url(soup):
    return soup.find("img", {"class": "topcard__profile-image"}).get("data-delayed-url")


def get_summary_info(soup):
    summary_info = {}
    div = soup.find("div", {"class": "topcard__info-container"})
    summary_info["name"] = div.find("h1", {"class": "topcard__name"}).text
    summary_info["headline"] = div.find("h2", {"class": "topcard__headline"}).text
    summary_info["location"] = div.find("h3", {"class": "topcard__location"}).text
    summary_info["industry"] = div.find("h4", {"class": "topcard__industry"}).text

    return summary_info


def get_summary_descr(soup):

    section = soup.find("section", {"class": "summary pp-section"})
    descr = section.find("p", {"class": "summary__description"}).text

    return descr


def get_dates(date_range):

    dates = {}

    dates["st"] = date_range.find("time", {"class": "date-range__start-date"}).text
    dates["nd"] = date_range.find("time", {"class": "date-range__end-date"}).text

    duration = date_range.find_all("span", {"class": "date-range__duration-bullet"})
    if len(duration) != 0:
        dates["duration"] = duration[0].text

    return dates


def get_experience(li):

    experience = {}

    div = li.find("div", {"class": "position"})
    ddiv = div.find("div", {"class": "position__content"})

    experience["title"] = ddiv.find("h4", {"class": "position__title"}).text
    experience["company_name"] = ddiv.find(
        "h5", {"class": "position__company-name"}
    ).text

    date_range = ddiv.find("span", {"class": "date-range"})

    experience.update(**get_dates(date_range))

    experience["location"] = ddiv.find("p", {"class": "position-body__location"}).text
    experience["description"] = ddiv.find(
        "p", {"class": "position-body__description"}
    ).text

    return experience


def get_experiences(soup):

    section = soup.find("section", {"class": "experience pp-section"})
    ul = section.find("ul", {"class": "experience__list"})

    experiences = [
        get_experience(li)
        for li in ul.find_all("li", {"class": "experience__list-item"})
    ]

    return experiences


def get_educ_descr(dddiv):

    r = {"description": None}

    div = dddiv.find("div", {"class": "education-item__details"})
    if not div:
        return r

    descr = div.find("p", {"class": "education-item__description"}).text
    r["description"] = descr
    return r


def get_education(li):

    education = {}

    a = li.find("a", {"class": "section-item__url education-item__url"})
    ddiv = a.find("div", {"class": "section-item education-item"})
    dddiv = ddiv.find("div", {"class": "section-item__content education-item__content"})

    education["title"] = dddiv.find("h4", {"class": "education-item__title"}).text

    education["degree"] = dddiv.find("p", {"class": "education-item__degree-info"}).text

    date_range = dddiv.find("span", {"class": "date-range"})

    education.update(**get_dates(date_range))

    education.update(**get_educ_descr(dddiv))

    return education


def get_educations(soup):

    section = soup.find("section", {"class": "education pp-section"})
    ul = section.find("ul", {"class": "education__list"})

    educations = [
        get_education(li) for li in ul.find_all("li", {"class": "education__list-item"})
    ]

    return educations


def get_skills_endorsements(soup):
    pass


def get_honors_awards(soup):
    pass


def get_languages(soup):
    pass


def valid_urls(url):
    found = REGEX_URL.findall(url)
    if found:
        return [f for f in found if f not in URLS_TO_SKIP]
    else:
        return False


def download(string_with_urls: str, urls: List[str], force=False) -> str:
    """Downloads all urls and replaces them with downloaded locations in a string

    Args:
        string_with_urls (str): a Atring containing urls.
        urls (List[str]): Urls to be downloaded.
        force (bool, optional): Defaults to False. Whether to download urls regardless of file existence

    Returns:
        updated_string (str): The original string but with all urls replaced by their
        corresponding, downloaded filepaths.
    """

    updated_string = string_with_urls
    for url in urls:
        _, filename = os.path.split(url)
        if filename:
            new_loc = os.path.join(DATA, filename)

            if force or not os.path.isfile(new_loc):
                response = requests.get(url)
                with open(new_loc, "wb") as file:
                    file.write(response.content)

            updated_string = updated_string.replace(url, new_loc)

    return updated_string


def single_spaces(string: str) -> str:
    """Replaces all instances of whitespace-like chars with single spaces

    Args:
        string (str): The string to modify

    Returns:
        str: The cleaned string
    """

    return UGLY_SPACES_RE.sub(" ", string)


def clean_json(raw_dct: dict) -> dict:
    cleaned = {}
    for k, v in raw_dct.items():
        if isinstance(v, dict):
            cleaned[k] = clean_json(v)
        elif isinstance(v, str):
            vv = v.strip()
            urls = valid_urls(vv)
            if urls:
                cleaned[k] = download(vv, urls)
            else:
                cleaned[k] = single_spaces(vv)
        elif isinstance(v, list):
            cleaned[k] = [clean_json(vv) for vv in v]
        elif not v:
            pass
        else:
            raise NotImplementedError(
                f"Didn't expect object v {v}of class {v.__class__.__name__}"
            )

    return cleaned

def get_json(profile_id=LINKEDIN_PAGE):

    raw_dct = {}

    html = get_profile(profile_id)

    soup = BeautifulSoup(html, features="html.parser")

    raw_dct["image_url"] = get_img_url(soup)
    raw_dct["info"] = get_summary_info(soup)
    raw_dct["summary"] = get_summary_descr(soup)
    raw_dct["experiences"] = get_experiences(soup)
    raw_dct["educations"] = get_educations(soup)
    raw_dct["skills_endorsements"] = get_skills_endorsements(soup)
    raw_dct["honors_awards"] = get_honors_awards(soup)
    raw_dct["languages"] = get_languages(soup)

    cleaned = clean_json(raw_dct)

    with open('cv.json', 'w') as fp:
        json.dump(cleaned, fp)

    return cleaned


if __name__ == "__main__":
    get_json()
