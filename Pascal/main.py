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

import os
import requests
import urllib.request as urlrequest
from bs4 import BeautifulSoup as bsoup
from tqdm import tqdm


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
    os_path = os.path.abspath(os.getcwd())
    data_path = os_path+'/Pascal/data/'

    page = request_pascal(url)
    
    data_class, img_name, txt_table = parser_page(page)
    # img_url = [url+'/'+data_class[index]+'/'+img_name[index] for index in range(len(img_name))]
    if len(img_name)!=len(txt_table):
        print("Data Error, over!")
        exit

    label_text = data_path+"label.txt"
    lab_f = open(label_text, 'w')
    tqdm_range = tqdm(range(len(img_name)), ncols=80)
    for index in tqdm_range:
        tqdm_range.set_description(img_name[index])
        text_name = data_path+'text/'+img_name[index][:-4]+'.txt'
        local_img = data_path+'images/'+img_name[index]
        img_url = url+data_class[index]+'/'+img_name[index]
        urlrequest.urlretrieve(img_url,filename=local_img)
        text_str = ""
        for txt in txt_table[index].find_all('td'):
            tstr = txt.get_text()
            text_str = text_str+"\t"+tstr
        with open(text_name,'w') as fp:
            fp.write(text_str)
        
        lab_f.write(data_class[index])
        lab_f.write('\n')

    lab_f.close()