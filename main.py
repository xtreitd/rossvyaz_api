import json
import re
import requests
from bs4 import BeautifulSoup


def refined(ref):
    return re.sub("^\s+|\t|\n|\r|\s+$", '', ref)


def get_html(urls):
    r = requests.get(urls, verify=False)
    return r.text


def write_json(data):
    with open('name.json', 'a') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)


def get_data(html):
    soup = BeautifulSoup(html, 'lxml')
    content = soup.find_all(class_='accordion-item__content')

    for data in content:
        dt = refined(data.find('div', class_='doc__date').text)
        title = refined(data.find('div', class_='doc__title').text)
        try:
            link = data.find_all('a', class_='doc__download')[1].get('href')
        except IndexError:
            continue

        dict_data = {'title': title, 'link': link, 'date': dt}
        write_json(dict_data)


if __name__ == '__main__':
    url = 'https://rossvyaz.gov.ru/deyatelnost/resurs-numeracii/vypiska-iz-reestra-sistemy-i-plana-numeracii'
    get_data(get_html(url))
