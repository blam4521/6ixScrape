"""Util functions to help run generic searches for craigslist toronto"""

from bs4 import BeautifulSoup as bs4
from cachetools import cached, TTLCache
from collections import OrderedDict
import json
import requests
import sys


URL_BASE = 'https://toronto.craigslist.org'
cache = TTLCache(maxsize=120, ttl=300)

AREAS = {'toronto': 'tor',
         'durham_region': 'drh',
         'york_region': 'yrk',
         'brampton': 'bra',
         'mississuaga': 'mss',
         'oakville': 'oak'}

CATEGORY_TOPICS = {'community': 'ccc',
                   'events': 'eee',
                   'for_sale': 'sss',
                   'gigs': 'ggg',
                   'housing': 'hhh',
                   'jobs': 'jjj',
                   'resume': 'rrr',
                   'services': 'bbb'}


@cached(cache)
def get_search_query(param, area, category):
    """Make a get request to URL_BASE, with user defined parameters.

        Args:
            param(str): user input on the type of object they are searching for.

            OPTIONAL area(str): user input on the city they are searching for.

            OPTIONAL category(str): user input on the topic they are searching for.

        Return:
            html(obj): a beautiful soup object with find methods.
    """

    search_url = URL_BASE + '/search'
    if area:
        search_url = search_url + '/%s' % area

    if category:
        search_url = search_url + '/%s' % category
    search_url = search_url + '?query=%s' % param

    try:
        response = requests.get(search_url)
        response.raise_for_status()
        html = bs4(response.text, 'html.parser')
        return html
    except requests.exceptions.HTTPError as err:
        print err
        return False


def search_results(html,  number_of_postings):
    """Parse the html object and pulls out the title text and date text.

        Args:
            html(obj): a beautiful soup object with find methods.

            number_of_postings(int): the number of postings to show user.

        Return:
            json(obj): a json output of the post title and date.
    """

    postings = html.find_all('li', attrs={'class': 'result-row'})

    json_list_of_postings = []

    for post in postings:
        title = post.find('a', attrs={'class': 'result-title hdrlnk'})
        date = post.find('time', attrs={'class': 'result-date'})

        # Python2.7 apparently orders the keys, one potential solution is to
        # use OrderedDict class to keep keys/values in the same order as
        # declared.
        data = OrderedDict()
        data['title'] = title.text
        data['date'] = date.text
        json_list_of_postings.append(data)

    # Sometimes the user might want to define the number of postings to view.
    if number_of_postings != 0:
        chunks = [json_list_of_postings[i:i + number_of_postings]
                  for i in xrange(0, len(json_list_of_postings), number_of_postings)]
        print(json.dumps(chunks[0], indent=4))
        return chunks[0]
    else:
        print(json.dumps(json_list_of_postings, indent=4))

    return json_list_of_postings


def search(param, area='', category='', number_of_postings=0):
    """Main entry point to the script.

    Args:
            param(str): user input on the type of object they are searching for.

            OPTIONAL area(str): user input on the city they are searching for.

            OPTIONAL category(str): user input on the topic they are searching for.

            OPTIONAL number_of_postings(int): the number of postings to show user.

    Return:
        search_results(obj): a list of objects.
    """

    raw_html = get_search_query(param, area, category)
    # Dont run the search results function if
    # raw_html returns a invalid URL.
    if raw_html:
        return search_results(raw_html, number_of_postings)
