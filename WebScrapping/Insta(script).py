import requests
from bs4 import BeautifulSoup
import json
from concurrent.futures import ThreadPoolExecutor
import asyncio
import time
instagram_url = 'https://www.instagram.com'
# profile_url = 'hadyyayman'


def get_followers_count(profile_url: str, session):

    response = session.get(f'{instagram_url}/{profile_url}')
    # print(response.status_code)
    if response.ok:
        soup = BeautifulSoup(response.text, 'lxml')
        # print(response.text)
        scripts = soup.select('script[type="application/ld+json"]')
        scripts_content = json.loads(scripts[0].text.strip())
        # print(json.dumps(scripts_content, indent=4, sort_keys=True))
        main_Entity_Of_Page = scripts_content['mainEntityOfPage']
        interaction_Statistic = scripts_content['interactionStatistic']
        followers_count = interaction_Statistic[0]['userInteractionCount']
        # print(followers_count)
        # print(len(scripts))
        # print(soup.prettify())
        return float(followers_count)

# Function for a faster output


async def get_followers_async(profile: list) -> list:
    res = []
    with ThreadPoolExecutor(max_workers=10) as executor:
        with requests.session() as session:
            loop = asyncio.get_event_loop()
            task = [
                loop.run_in_executor(executor, get_followers_count, *(profile, session)) for profile in profiles
            ]
            for response in await asyncio.gather(*task):
                res.append(response)
    return res

profiles = ['bassantt91', 'hadyyayman',
            '_emanhazem', 'minamagdy3', 'aserelkikii']
start = time.time()
for profile in profiles:
    count = get_followers_count(profile, requests)
    print(f'{profile} has {count} Posts')
end = time.time()
elapsed = end - start
print(f"Synchronously took {elapsed} seconds")
print("-------------------------------------------")
# much faster way
start = time.time()
loop = asyncio.get_event_loop()
future = asyncio.ensure_future(get_followers_async(profiles))
res = loop.run_until_complete(future)
end = time.time()
elapsed = end - start
print(res)
print(f"ASync Multi-Threading took {elapsed} seconds")
