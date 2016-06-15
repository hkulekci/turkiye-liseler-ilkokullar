import requests
from bs4 import BeautifulSoup
import re
import json
import config


def get_last_page(content_soup):
    navigation_last_a = str(content_soup.find('a', class_="last").get('href'))
    p = re.compile('SAYFANO=(\d+)')
    result = p.findall(navigation_last_a)
    if len(result) >= 1:
        return int(result[0])


def get_page_schools(content_soup):
    # type: (BeautifulSoup) -> array

    schools = []
    for table in content_soup.find_all('table', class_="table"):
        if None != table.get('class') and 'table' in table.get('class'):
            # print table.find_all('tr')
            for tr in table.find_all('tr'):
                tds = tr.find_all('td')
                if len(tds) > 2:
                    aObj = tds[0].find('a')
                    school = aObj.text.split(' - ')
                    school.append(aObj.get('href'))
                    school.append(tds[2].find('img').get('data-veri'))

                    schools.append(school)

    return schools


def get_city_with_page(city_id, page=1):
    # type: (integer, integer) -> BeautifulSoup
    url = config.url + '' + str(city_id) + '&SAYFANO=' + str(page)

    content = requests.get(url)
    content_soup = BeautifulSoup(content.content, 'html.parser')

    return content_soup


def get_city(city_id):
    # type: (integer) -> array
    content_soup = get_city_with_page(city_id, 1)
    last_page = get_last_page(content_soup)
    schools = []
    print "Last Page (City Id : " + str(city_id) + "): " + str(last_page)
    for i in range(1, last_page + 1):
        print "Page : " + str(i)
        content_soup = get_city_with_page(city_id, i)
        schools += get_page_schools(content_soup)

    return schools


def main():
    schools = []
    cities = range(1, 82)
    cities.append(999)
    cities = [999]
    for city_id in cities:
        schools += get_city(city_id)
        with open('data/schools'+str(city_id)+'.json', 'w') as outfile:
            outfile.write(json.dumps(schools).decode('unicode-escape').encode('utf8'))


if __name__ == '__main__':
    main()
