from urllib.request import Request
from urllib.request import urlopen
from bs4 import BeautifulSoup
import urllib.request
import re
import numpy as np
import time
import os
import random
import time

url = [쇼핑몰주소]
req = Request(url,headers={'User-Agent':'Mozila/5.0'})
webpage = urlopen(req)
soup = BeautifulSoup(webpage)

objects = soup.find('li',id='big_section')

#obejcts.text 태그에 담긴 텍스트
print(objects.text)

#objects.name 태그의 이름
print(objects.name)

#objects.attrs 태그의 속성과 속성값
print(objects.attrs)

len(soup.find_all('div',id='big_section'))
soup.find('div',id='bigsection').find_all('li',class='goods-form')[0].find('div',class_='prdimg').find('img')['src']

os.mkdir('crawling_save')
url = ''
req = Request(url, headers={'User-Agent':'Mozila/5.0'})
webpage = urlopen(req)
soup = BeautifulSoup(webpage)

base_site = ''





