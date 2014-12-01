import sqlite3
from selenium import webdriver
from time import sleep

"""
issues:

1. pagination > 100
2. images - not sure if real
3. address = google maps link
4. brute force - sloppy code. refactor functions.
    check for duplicates. add tests. add data to db frequenty.
"""


def get_links(link_array):
    all_links = []
    driver = webdriver.Firefox()
    counter = 1
    while True:
        driver.get(link_array[0] + str(counter))
        links = driver.find_elements_by_xpath(
            '//span[@class="HeaderControlTitle"]/a[2]')
        if len(links) > 0:
            for link in links:
                all_links.append(
                    [
                        link.get_attribute('text'),
                        link.get_attribute('href'),
                        link_array[1]
                    ]
                )
            print '{0}, page {1}...'.format(link_array[1], counter)
            counter += 1
            sleep(1)
        else:
            break
    driver.quit()
    return all_links


def add_links_to_database(all_links):
    con = sqlite3.connect('fish_links.db')
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
            pass
        for link in all_links:
            cur.execute(
                """
                INSERT INTO links(name, url, category) VALUES(?, ?, ?)
                """, (link[0], link[1], link[2]))


def grab_data():
    all_data_array = []
    driver = webdriver.Firefox()
    con = sqlite3.connect('fish_links.db')
    with con:
        cur = con.cursor()
        all_links = cur.execute('SELECT * FROM links;')
    for link in all_links:
        all_data = {}
        driver.get(str(link[2]))
        all_data["name"] = link[1]
        all_data["url"] = link[2]
        all_data["category"] = link[3]
        try:
            row_one_name = driver.find_element_by_xpath(
                '//tbody/tr[2]/td[1]').text
            row_one_value = driver.find_element_by_xpath(
                '//tbody/tr[2]/td[2]/a').get_attribute('href')
            all_data[row_one_name] = row_one_value
        except:
            pass
        try:
            row_two_name = driver.find_element_by_xpath(
                '//tbody/tr[3]/td[1]').text
            row_two_value = driver.find_element_by_xpath(
                '//tbody/tr[3]/td[2]/a').get_attribute('href')
            all_data[row_two_name] = row_two_value
        except:
            pass
        try:
            row_three_name = driver.find_element_by_xpath(
                '//tbody/tr[4]/td[1]').text
            row_three_value = driver.find_element_by_xpath(
                '//tbody/tr[4]/td[2]/a').get_attribute('text')
            all_data[row_three_name] = row_three_value
        except:
            pass
        try:
            row_four_name = driver.find_element_by_xpath(
                '//tbody/tr[5]/td[1]').text
            if row_four_name == "Social":
                try:
                    row_four_name_one = driver.find_element_by_xpath(
                        '//tbody/tr[5]/td[2]/a').get_attribute('text')
                    row_four_value_one = driver.find_element_by_xpath(
                        '//tbody/tr[5]/td[2]/a').get_attribute('href')
                    all_data[row_four_name_one] = row_four_value_one
                except:
                    pass
                try:
                    row_four_name_two = driver.find_element_by_xpath(
                        '//tbody/tr[5]/td[2]/a[2]').get_attribute('text')
                    row_four_value_two = driver.find_element_by_xpath(
                        '//tbody/tr[5]/td[2]/a[2]').get_attribute('href')
                    all_data[row_four_name_two] = row_four_value_two
                except:
                    pass
            else:
                row_four_value = driver.find_element_by_xpath(
                    '//tbody/tr[5]/td[2]/a').get_attribute('text')
                all_data[row_four_name] = row_four_value
        except:
            pass
        try:
            row_five_name = driver.find_element_by_xpath(
                '//tbody/tr[6]/td[1]').text
            if row_five_name == "Social":
                try:
                    row_five_name_one = driver.find_element_by_xpath(
                        '//tbody/tr[6]/td[2]/a').get_attribute('text')
                    row_five_value_one = driver.find_element_by_xpath(
                        '//tbody/tr[6]/td[2]/a').get_attribute('href')
                    all_data[row_five_name_one] = row_five_value_one
                except:
                    pass
                try:
                    row_five_name_two = driver.find_element_by_xpath(
                        '//tbody/tr[6]/td[2]/a[2]').get_attribute('text')
                    row_five_value_two = driver.find_element_by_xpath(
                        '//tbody/tr[6]/td[2]/a[2]').get_attribute('href')
                    all_data[row_five_name_two] = row_five_value_two
                except:
                    pass
            else:
                row_five_value = driver.find_element_by_xpath(
                    '//tbody/tr[6]/td[2]/a').get_attribute('href')
                all_data[row_five_name] = row_five_value
        except:
            pass
        img = driver.find_element_by_xpath(
            '//div[@id="dnn_ctr387_ModuleContent"]/div[2]/a[2]/img'
        ).get_attribute('src')
        all_data["image"] = img
        print 'Grabbing data - {0}, row {1}...'.format(link[3], link[0])
        all_data_array.append([all_data])
    driver.quit()
    return all_data_array


def add_data_to_database(all_data):
    con = sqlite3.connect('fish_links.db')
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
                    address TEXT,
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
                address = array[0]['Address']
            else:
                address = 'n/a'
            if 'Website' in array[0].keys():
                website = array[0]['Website']
            else:
                website = 'n/a'
            if 'Phone' in array[0].keys():
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
                    address,
                    website,
                    phone,
                    email,
                    facebook,
                    twitter,
                    image
                )
                VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    name,
                    url,
                    category,
                    address,
                    website,
                    phone,
                    email,
                    facebook,
                    twitter,
                    image
                )
            )


def main():
    # starting_links_array = [
    #     ['http://fishingstatus.com/places/directory/view/groupslist/categoryId/8/vgsPage/', 'marina'],
    #     ['http://fishingstatus.com/places/directory/view/groupslist/categoryId/72/vgsPage/', 'piers'],
    #     ['http://fishingstatus.com/places/directory/view/groupslist/categoryId/1194/vgsPage/', 'lodges & resorts'],
    #     ['http://fishingstatus.com/places/directory/view/groupslist/categoryId/1197/vgsPage/', 'clubs & groups'],
    #     ['http://fishingstatus.com/places/directory/view/groupslist/categoryId/9/vgsPage/', 'charters & guides'],
    #     ['http://fishingstatus.com/places/directory/view/groupslist/categoryId/1105/vgsPage/', 'publications'],
    #     ['http://fishingstatus.com/places/directory/view/groupslist/categoryId/1195/vgsPage/', 'campgrounds'],
    #     ['http://fishingstatus.com/places/directory/view/groupslist/categoryId/1198/vgsPage/', 'government'],
    #     ['http://fishingstatus.com/places/directory/view/groupslist/categoryId/70/vgsPage/', 'bait & tackle'],
    #     ['http://fishingstatus.com/places/directory/view/groupslist/categoryId/1172/vgsPage/', 'taxidermy'],
    #     ['http://fishingstatus.com/places/directory/view/groupslist/categoryId/1196/vgsPage/', 'marine service & supplies']
    # ]
    # for link in starting_links_array:
    #     add_links_to_database(get_links(link))
    all_data = grab_data()
    add_data_to_database(all_data)


if __name__ == '__main__':
    main()
