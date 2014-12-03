import sqlite3
from selenium import webdriver
from time import sleep

# from category_links import starting_links_array_by_category
from state_links import create_list


###############
### Globals ###
###############

DATABASE_NAME = 'test.db'
ALL_DATA_ARRAY = []


############
### Code ###
############


def get_links_by_category(link_array):
    """
    Given a list with a link and category, this function returns
    a list of lists, each containing the name, URL, and category.
    """
    DRIVER = webdriver.Firefox()
    # DRIVER = webdriver.PhantomJS()
    category_list = []
    counter = 1
    while True:
        DRIVER.get(link_array[0] + str(counter))
        links = DRIVER.find_elements_by_xpath(
            '//span[@class="HeaderControlTitle"]/a[2]')
        # If there are relevant links on the page, grab them
        if len(links) > 0:
            for link in links:
                category_list.append(
                    [
                        link.get_attribute('text'),
                        link.get_attribute('href'),
                        link_array[1]
                    ]
                )
            print '{0}, page {1}...'.format(link_array[1], counter)
            # print category_list  # sanity check
            counter += 1
            sleep(1)  # to reduce load
        else:
            break
    DRIVER.quit()
    return category_list


def add_links_to_database(all_links):
    """
    Given a list of lists, each containing the name, URL, and category,
    update the database.
    """
    con = sqlite3.connect(DATABASE_NAME)
    with con:
        cur = con.cursor()
        try:
            cur.execute(
                """
                CREATE TABLE links(
                    id INTEGER PRIMARY KEY, name TEXT, url TEXT, category TEXT)
                """
            )
        except sqlite3.OperationalError:
            pass  # silenced

        # loop through scrapped emails
        for link in all_links:
            cur.execute("SELECT url FROM links where url = ?", (link[1],))
            check = cur.fetchone()
            # if link is not in db, add it
            if check is None:
                cur.execute(
                    """
                    INSERT INTO links(name, url, category) VALUES(?, ?, ?)
                    """, (link[0], link[1], link[2]))


def grab_data():
    """
    Grab all scrapped links from the links table in the database.
    Iterating through the links, scrap relevant data from each -

        name
        url
        category
        street address
        city
        state
        address (google maps url)
        website
        phone
        email
        facebook
        twitter
        image (url)

    - returning a list of dicts
    Note: In *most* cases facebook and twitter profiles are not listed. Also,
    the image is usually a placeholder image.
    """
    DRIVER = webdriver.Firefox()
    # DRIVER = webdriver.PhantomJS()
    con = sqlite3.connect(DATABASE_NAME)
    with con:
        cur = con.cursor()
        # all_links = cur.execute('SELECT * FROM links;')
        all_links = cur.execute('SELECT * FROM links LIMIT 10;')  # for testing
    for link in all_links:
        all_data = {}
        DRIVER.get(str(link[2]))
        all_data["name"] = link[1]
        all_data["url"] = link[2]
        all_data["category"] = link[3]
        # Grab data from the table (if exists)
        try:
            row_one_name = DRIVER.find_element_by_xpath(
                '//tbody/tr[2]/td[1]').text  # street address
            row_one_value = DRIVER.find_element_by_xpath(
                '//tbody/tr[2]/td[2]/a').get_attribute('text')
            all_data[row_one_name] = row_one_value
        except:
            pass  # silenced
        try:
            row_two_name = "city"
            row_two_value = DRIVER.find_element_by_xpath(
                '//tbody/tr[2]/td[2]/a[2]').get_attribute('text')
            all_data[row_two_name] = row_two_value
        except:
            pass  # silenced
        try:
            row_three_name = "state"
            row_three_value = DRIVER.find_element_by_xpath(
                '//tbody/tr[2]/td[2]/a[3]').get_attribute('text')
            all_data[row_three_name] = row_three_value
        except:
            pass  # silenced
        try:
            row_four_name = DRIVER.find_element_by_xpath(
                '//tbody/tr[2]/td[1]').text  # address url
            row_four_name = row_one_name + " url"
            row_four_value = DRIVER.find_element_by_xpath(
                '//tbody/tr[2]/td[2]/a').get_attribute('href')
            all_data[row_four_name] = row_four_value
        except:
            pass  # silenced
        try:
            row_five_name = DRIVER.find_element_by_xpath(
                '//tbody/tr[3]/td[1]').text  # website
            row_five_value = DRIVER.find_element_by_xpath(
                '//tbody/tr[3]/td[2]/a').get_attribute('href')
            all_data[row_five_name] = row_five_value
        except:
            pass  # silenced
        try:
            row_six_name = DRIVER.find_element_by_xpath(
                '//tbody/tr[4]/td[1]').text  # phone
            row_six_value = DRIVER.find_element_by_xpath(
                '//tbody/tr[4]/td[2]/a').get_attribute('text')
            all_data[row_six_name] = row_six_value
        except:
            pass  # silenced
        try:
            row_seven_name = DRIVER.find_element_by_xpath(
                '//tbody/tr[5]/td[1]').text  # social links and/or email
            if row_seven_name == "Social":
                try:
                    row_seven_name_one = DRIVER.find_element_by_xpath(
                        '//tbody/tr[5]/td[2]/a').get_attribute('text')
                    row_seven_value_one = DRIVER.find_element_by_xpath(
                        '//tbody/tr[5]/td[2]/a').get_attribute('href')
                    all_data[row_seven_name_one] = row_seven_value_one
                except:
                    pass  # silenced
                try:
                    row_seven_name_two = DRIVER.find_element_by_xpath(
                        '//tbody/tr[5]/td[2]/a[2]').get_attribute('text')
                    row_seven_value_two = DRIVER.find_element_by_xpath(
                        '//tbody/tr[5]/td[2]/a[2]').get_attribute('href')
                    all_data[row_seven_name_two] = row_seven_value_two
                except:
                    pass  # silenced
            else:
                row_seven_value = DRIVER.find_element_by_xpath(
                    '//tbody/tr[5]/td[2]/a').get_attribute('text')
                all_data[row_seven_name] = row_seven_value
        except:
            pass  # silenced
        try:
            row_eight_name = DRIVER.find_element_by_xpath(
                '//tbody/tr[6]/td[1]').text  # social links and/or email
            if row_eight_name == "Social":
                try:
                    row_eight_name_one = DRIVER.find_element_by_xpath(
                        '//tbody/tr[6]/td[2]/a').get_attribute('text')
                    row_eight_value_one = DRIVER.find_element_by_xpath(
                        '//tbody/tr[6]/td[2]/a').get_attribute('href')
                    all_data[row_eight_name_one] = row_eight_value_one
                except:
                    pass  # silenced
                try:
                    row_eight_name_two = DRIVER.find_element_by_xpath(
                        '//tbody/tr[6]/td[2]/a[2]').get_attribute('text')
                    row_eight_value_two = DRIVER.find_element_by_xpath(
                        '//tbody/tr[6]/td[2]/a[2]').get_attribute('href')
                    all_data[row_eight_name_two] = row_eight_value_two
                except:
                    pass  # silenced
            else:
                row_eight_value = DRIVER.find_element_by_xpath(
                    '//tbody/tr[6]/td[2]/a').get_attribute('href')
                all_data[row_eight_name] = row_eight_value
        except:
            pass  # silenced
        img = DRIVER.find_element_by_xpath(
            '//div[@id="dnn_ctr387_ModuleContent"]/div[2]/a[2]/img'
        ).get_attribute('src')
        all_data["image"] = img
        print 'Grabbing data - {0}, row {1}...'.format(link[3], link[0])
        ALL_DATA_ARRAY.append([all_data])
    DRIVER.quit()
    # print ALL_DATA_ARRAY  # sanity check
    return ALL_DATA_ARRAY  # all data!!


def add_data_to_database(all_data):
    """
    Given the ALL_DATA_ARRAY, this function adds the data to the database.
    """
    con = sqlite3.connect(DATABASE_NAME)
    with con:
        cur = con.cursor()
        try:
            cur.execute(
                """
                CREATE TABLE data(
                    id INTEGER PRIMARY KEY,
                    name TEXT,
                    url TEXT,
                    category TEXT,
                    street_address TEXT,
                    city TEXT,
                    state TEXT,
                    address_url TEXT,
                    website TEXT,
                    phone TEXT,
                    email TEXT,
                    facebook TEXT,
                    twitter TEXT,
                    image TEXT
                )
                """
            )
        except sqlite3.OperationalError:
            pass
        counter = 1
        for array in all_data:
            name = array[0]['name']
            url = array[0]['url']
            category = array[0]['category']
            if 'Address' in array[0].keys():
                street_address = array[0]['Address']
            else:
                street_address = 'n/a'
            if 'city' in array[0].keys():
                city = array[0]['city']
            else:
                city = 'n/a'
            if 'state' in array[0].keys():
                state = array[0]['state']
            else:
                state = 'n/a'
            if 'Address url' in array[0].keys():
                address_url = array[0]['Address url']
            else:
                address_url = 'n/a'
                state = 'n/a'
            if 'Website' in array[0].keys():
                website = array[0]['Website']
            else:
                website = 'n/a'
            if 'phone' in array[0].keys():
                phone = array[0]['Phone']
            else:
                phone = 'n/a'
            if 'Email' in array[0].keys():
                email = array[0]['Email']
            else:
                email = 'n/a'
            if 'Facebook' in array[0].keys():
                facebook = array[0]['Facebook']
            else:
                facebook = 'n/a'
            if 'Twitter' in array[0].keys():
                twitter = array[0]['Twitter']
            else:
                twitter = 'n/a'
            if 'image' in array[0].keys():
                image = array[0]['image']
            else:
                image = 'n/a'
            print 'Adding data - {0}, row {1}...'.format(category, counter)
            counter += 1
            cur.execute(
                """
                INSERT INTO data(
                    name,
                    url,
                    category,
                    street_address,
                    city,
                    state,
                    address_url,
                    website,
                    phone,
                    email,
                    facebook,
                    twitter,
                    image
                )
                VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    name,
                    url,
                    category,
                    street_address,
                    city,
                    state,
                    address_url,
                    website,
                    phone,
                    email,
                    facebook,
                    twitter,
                    image
                )
            )


def main():

    # for link in starting_links_array_by_category:
    #     category_list = get_links_by_category(link)
    #     add_links_to_database(category_list)

    # grab links, add to database
    starting_links_array_by_state = create_list()
    for link in starting_links_array_by_state:
        category_list = get_links_by_category(link)
        add_links_to_database(category_list)

    # scrape data from links
    all_data = grab_data()

    # add scraped data to the database
    add_data_to_database(all_data)


if __name__ == '__main__':
    main()
