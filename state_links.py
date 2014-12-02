STATE_BASE = 'http://fishingstatus.com/places/directory/categoryId/'

states = ["AL", "AK", "AZ", "AR", "CA", "CO", "CT", "DC", "DE", "FL", "GA",
          "HI", "ID", "IL", "IN", "IA", "KS", "KY", "LA", "ME", "MD",
          "MA", "MI", "MN", "MS", "MO", "MT", "NE", "NV", "NH", "NJ",
          "NM", "NY", "NC", "ND", "OH", "OK", "OR", "PA", "RI", "SC",
          "SD", "TN", "TX", "UT", "VT", "VA", "WA", "WV", "WI", "WY"]

starting_links_array_by_state = [
    ['9/State/', 'charters & guides'],
    ['70/State/', 'bait & tackle'],
]


def create_list():
    new_list = []
    for state in states:
        for url in starting_links_array_by_state:
            new_list.append([STATE_BASE + url[0] + state + '/vgsPage/', url[1]])
    return new_list
