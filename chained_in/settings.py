"""Settings

Set any and all project variables here.

If you have two version of the project running, they should differ only in
variables set in this file.

Optionally, secret stuff is located in the a .env file, to be loaded here.
"""
import os

DATA = os.path.join(
    os.path.dirname(os.path.dirname(os.path.realpath(__file__))),
    'data'
)
