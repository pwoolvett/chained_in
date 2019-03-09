#!/usr/bin/python3
# coding=utf-8
"""Auxiliary Utilities"""

import requests
from requests_oauthlib import OAuth1

def get_oauth(url:str, auth:OAuth1=None, **oaouth_kw) -> requests.Response:
    """GET with OAuth

    Args:
        url (str): the url to GET.
        auth (OAuth1, optional): Defaults to None. Authentication object.
        oaouth_kw (optional): Kwargs passed to initialize Oauth1.

    Returns:
        requests.Response: the result of the GET request.
    """

    url = 'https://api.twitter.com/1.1/account/verify_credentials.json'
    auth = OAuth1(
        **oaouth_kw,
        # 'YOUR_APP_KEY',
        # 'YOUR_APP_SECRET',
        # 'USER_OAUTH_TOKEN',
        # 'USER_OAUTH_TOKEN_SECRET'
    )

    return requests.get(url, auth=auth)
