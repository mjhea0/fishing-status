STATE_BASE = 'http://fishingstatus.com/places/directory/categoryId/'

states = ["RI", "SC",
          "SD", "TN", "TX", "UT", "VT", "VA", "WA", "WV", "WI", "WY"]

starting_links_array_by_state = [
    ['8/State/', 'marina'],
    ['72/State/', 'piers'],
    ['1194/State/', 'lodges & resorts'],
    ['1197/State/', 'clubs & groups'],
    ['9/State/', 'charters & guides'],
    ['1105/State/', 'publications'],
    ['1195/State/', 'campgrounds'],
    ['1198/State/', 'government'],
    ['70/State/', 'bait & tackle'],
    ['1172/State/', 'taxidermy'],
    ['1196/State/', 'marine service & supplies']
]


def create_list():
    new_list = []
    for state in states:
        for url in starting_links_array_by_state:
            new_list.append([STATE_BASE + url[0] + state + '/vgsPage/', url[1]])
    return new_list
