# -*- encoding: utf-8 -*-
'''
@File    :   main.py
@Time    :   2020/12/14 22:21:33
@Author  :   Liou Siaocing 
@Version :   1.0
@Contact :   itliuxiaoqing@163.com
@License :   (C)Copyright 2020-, Liugroup-NLPR-CASIA
@Desc    :   None
'''

import requests
import lxml
import re
from bs4 import BeautifulSoup as bsoup


def request_pascal(url):

    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.text
    except requests.RequestException:
        return None

def parser_page(page):
    imgurl_list = []
    soup = bsoup(page, features='lxml')
    img_list = soup.find_all('img')
    for img in img_list:
        imgurl_list.append(img.get('src'))
    
    return imgurl_list

if __name__=='__main__':

    url = 'https://vision.cs.uiuc.edu/pascal-sentences/'
    page = request_pascal(url)
    if page is None:
        exit
    add_prestr = lambda b:url+b
    soup = parser_page(page)
    soup = map(add_prestr,soup)
    print(soup[0])