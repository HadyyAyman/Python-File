import requests
from bs4 import BeautifulSoup
from urllib.request import urlopen
import csv

url = 'https://www.instagram.com/'

# profile_url = 'bassantt91'


def get_post_count(profile_url: str):
    page = urlopen(url+profile_url).read()
    soup = BeautifulSoup(page, 'html.parser')
    # print(soup.prettify())
    string = soup.find('meta', {'property': 'og:description'})['content']
    # print(string)
    return string


profiles = ['bassantt91', 'hadyyayman']

for profile in profiles:
    count = get_post_count(profile)

    user_details = []
    user_details.append({'Profile Name': profile, 'User Status': count})
    keys = user_details[0].keys()
    print(f"{profile} has {count}")


