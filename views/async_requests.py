import aiohttp
import asyncio
import async_timeout
from flask import Blueprint, render_template
from utils.access import is_full_access


async_view = Blueprint("async", __name__, static_folder="static", template_folder="template")
source_urls = [
    'http://localhost:8000/source_1.json',
    'http://localhost:8000/source_2.json',
    'http://localhost:8000/source_3.json'
]
loop = asyncio.get_event_loop()


@is_full_access
@async_view.route('/')
def async_requests():
    return render_template('async_requests.html')


# create async loop & display results
@is_full_access
@async_view.route('/display_data', methods=['POST', 'GET'])
def display_data():
    responses = loop.run_until_complete(asyncio.gather(
        get_data(source_urls[0]),
        get_data(source_urls[1]),
        get_data(source_urls[2])
    ))
    # if one of responses raise exception - remove it from list
    for response in responses:
        if not isinstance(response, list):
            responses.remove(response)
    flat_list = [item for sublist in responses for item in sublist]
    sorted_data = sorted(flat_list, key=lambda d: d['id'])
    return render_template('async_requests.html', sorted_data=sorted_data)


# getting data from url
async def get_data(url):
    try:
        async with aiohttp.ClientSession() as session, async_timeout.timeout(2):
            async with session.get(url) as response:
                return await response.json()
    except Exception:
        pass
