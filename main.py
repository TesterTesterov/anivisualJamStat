import requests
from bs4 import BeautifulSoup
#Install lxml!
#import matplotlib.pyplot as plt
from datetime import date, datetime
from fake_useragent import UserAgent
import time

base_link = 'https://anivisual.net'

def _get_num_of_pages(url):
    count = 0
    bad = True
    response = None
    while (bad):
        try:
            response = requests.get(url, headers={'User-Agent': UserAgent().chrome})
            bad = False
        except:
            time.sleep(5)
    bf = BeautifulSoup(response.text, "lxml", multi_valued_attributes = None)
    good_tag = bf.find('ul', class_='switches switchesTbl forum-pages')
    very_good_tags = good_tag.contents

    for i in very_good_tags:
        try:
            if ((i['class'] == 'switchActive') or (i['class'] == 'switch')):
                count += 1
        except:
            pass
    return count

def _find_all_thread_links(url):
    links = []

    bad = True
    response = None
    while (bad):
        try:
            response = requests.get(url, headers={'User-Agent': UserAgent().chrome})
            bad = False
        except:
            time.sleep(5)
    bf = BeautifulSoup(response.text, "lxml", multi_valued_attributes=None)

    good_tags = bf.find_all('a', class_='threadLink')
    for i in good_tags:
        try:
            links.append(base_link+i['href'])
        except:
            pass
    return links

def _find_first_post_date(url):
    dater = ''
    bad = True
    response = None
    while (bad):
        try:
            response = requests.get(url, headers={'User-Agent': UserAgent().chrome})
            bad = False
        except:
            time.sleep(5)
    bf = BeautifulSoup(response.text, 'lxml', multi_valued_attributes=None)

    normal_tags = bf.find_all('td', class_='postTdTop', limit=2)
    good_tag = normal_tags.pop()
    date_string = good_tag.contents[0].split(' ')[2][:-1]
    dater = datetime.strptime(date_string, '%d.%m.20%y')
    return dater.date()

jam1_start = date(2020, 7, 7)
jam1_dur = 7
jam1_url = 'https://anivisual.net/forum/43' #-0-1 #5
jam1_str = '=== ANIVISUAL JAM #1 (ХОРРОР):'
jam2_start = date(2021, 1, 11)
jam2_dur = 7
jam2_url = 'https://anivisual.net/forum/49' #-0-1 #3
jam2_str = '=== ANIVISUAL JAM #2 (ХОЛОД):'
jam3_start = date(2021, 7, 16)
jam3_dur = 10
jam3_url = 'https://anivisual.net/forum/53' #-0-1 #4
jam3_str = '=== ANIVISUAL JAM #3 (СВИДАНИЕ):'

jam = {
    'start': (jam1_start, jam2_start, jam3_start),
    'url': (jam1_url, jam2_url, jam3_url),
    'dur': (jam1_dur, jam2_dur, jam3_dur),
    'str': (jam1_str, jam2_str, jam3_str)
}

def main():
    jam_num = 0
    #for i in range(3):
    #    print(_get_num_of_pages(jam["url"][i]))
    #for i in _find_all_thread_links(jam["url"][jam_num]):
    #    first_date = _find_first_post_date(i)
    #    second_date = jam["start"][jam_num]
    #    print(i, first_date, second_date, first_date <= second_date)

    for jam_num in range(3):
        first_day_count = 0
        str_number = _get_num_of_pages(jam['url'][jam_num])
        for str_num in range(str_number):
            str_url = jam['url'][jam_num]
            str_url += "-0-" + str(str_num)
            thread_links = _find_all_thread_links(str_url)
            for thread_link in thread_links:
                new_date = _find_first_post_date(thread_link)
                if (new_date <= jam['start'][jam_num]):
                    first_day_count += 1
        print(jam['str'][jam_num])
        print(first_day_count, 'за первый день и ранее (до 2-го дня).')
    input()

if __name__ == '__main__':
    main()