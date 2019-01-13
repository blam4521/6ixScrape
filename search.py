from bs4 import BeautifulSoup as bs4
from collections import OrderedDict
import json
import requests
import sys


URL_BASE = 'https://toronto.craigslist.org'
AREAS = ['tor', 'drh', 'yrk', 'bra', 'mss', 'oak']
PREFIX_TOPICS = ['ccc', 'eee', 'sss', 'ggg', 'hhh', 'jjj', 'rrr', 'bbb']


def get_search_query(area='', prefix='', param=''):
    """Make a get request to URL_BASE, with user defined parameter.

        Args:

            Optional area(str): user input on the city they are searching for. 

            Optional prefix(str): user input on the topic they are searching for. 

            param(str): user input on the type of object they are searching for. 

        Return:
            html(obj): a beautiful soup object with find methods.
    """

    search_url = '/'.join([URL_BASE, 'search?query=%s' % param])
    print(search_url)
    try:
        response = requests.get(search_url)
        print(response.url)
        response.raise_for_status()
        html = bs4(response.text, 'html.parser')
        return html
    except requests.exceptions.HTTPError as err:
        print err
        return False


def search_results(html):
    """Parse the html object and pulls out the title text and date text.

        Args:
            html(obj): a beautiful soup object with find methods.

        Return:
            json(obj): a json output of the post title and date.
    """

    postings = html.find_all('li', attrs={'class': 'result-row'})

    json_list_of_postings = []

    for post in postings:
        title = post.find('a', attrs={'class': 'result-title hdrlnk'})
        date = post.find('time', attrs={'class': 'result-date'})

        # Python2.7 apparently orders the keys, one potential solution is to
        # use OrderedDict classe to keep keys/values in the same order as
        # declared.
        data = OrderedDict()
        data['title'] = title.text
        data['date'] = date.text
        json_list_of_postings.append(data)

    # print(json.dumps(json_list_of_postings, indent=4))
    return json_list_of_postings


def main():
    """Main entry point to the script."""

    raw_html = get_search_query(param='apartments')
    # Dont run the search results function if
    # raw_html returns a invalid URL.
    if raw_html:
        search_results(raw_html)


if __name__ == '__main__':
    main()
