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
    img_name = []
    txt_table = []
    data_class = []
    soup = bsoup(page, features='lxml')
    img_list = soup.find_all('img')
    for img in img_list:
        url_str = img.get('src').split('/')
        data_class.append(url_str[0])
        img_name.append(url_str[1])

    for txt in soup.find_all('table'):
        txt_table.append(txt)
    return data_class, img_name, txt_table[1:]

if __name__=='__main__':

    url = 'https://vision.cs.uiuc.edu/pascal-sentences/'
    data_path = './data/'

    page = request_pascal(url)
    
    data_class, img_name, txt_table = parser_page(page)
    print(data_class[1])
    img_url = [url+'/'+data_class[index]+'/'+img_name[index] for index in range(len(img_name))]
    if len(img_url)!=len(txt_table):
        print("Data Error, over!")
        exit

    print(len(txt_table))
    a = txt_table[2].find_all('td')
    print(a)