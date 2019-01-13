import craigslist_util as cgu
reload(cgu)


AREAS = {'toronto': 'tor',
         'durham_region': 'drh',
         'york_region': 'yrk',
         'brampton': 'bra',
         'mississuaga': 'mss',
         'oakville': 'oak'}

PREFIX_TOPICS = {'community': 'ccc',
                 'events': 'eee',
                 'for_sale': 'sss',
                 'gigs': 'ggg',
                 'housing': 'hhh',
                 'jobs': 'jjj',
                 'resume': 'rrr',
                 'services': 'bbb'}

# cgu.search(param='apartments', number_of_postings=1)

# OPTIONAL: If you want to add region and topics like housing, community, etc.
cgu.search(param='apartments',
           area=AREAS['brampton'], prefix=PREFIX_TOPICS['housing'], number_of_postings=2)
