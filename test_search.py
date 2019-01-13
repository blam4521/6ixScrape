import craigslist_util as cgu
reload(cgu)

# Default search.
cgu.search(param='apartments')

# OPTIONAL: If you want to add region and category like housing, community, etc.

# Search with area filter and number of postings.
# cgu.search(param='apartments',
#            area=cgu.AREAS['brampton'], number_of_postings=3)

# Search with category filter and number of postings.
# cgu.search(param='apartments',
#            category=cgu.CATEGORY_TOPICS['housing'], number_of_postings=1)

# Search with category and area filter and number of postings.
# cgu.search(param='apartments',
#            area=cgu.AREAS['brampton'], category=cgu.CATEGORY_TOPICS['housing'], number_of_postings=2)
