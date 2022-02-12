# -*- coding: utf8 -*-

from qwer import accords_
from bs4 import BeautifulSoup
import requests


def get_singer(singer):
    singer = singer.replace(' ', '+')
    print(singer)

    url = 'https://amdm.ru/search/?q=' + singer
    page = requests.get(url)
    soup = BeautifulSoup(page.text, 'lxml')
    a = str(soup.select(".items")[0].text)
    a = a.split('.')
    songs = []
    for i in range(1, len(a)):
        if i <= 8:
            songs.append(a[i].split('—')[::-2][0][1:-1])
        if i == len(a) - 1:
            songs.append(a[i].split('—')[::-2][0][1:])
        else:
            songs.append(a[i].split('—')[::-2][0][1:-2])
    return (songs)





def get_song(song=''):
    song = song.replace(' ','+')
    url = 'https://amdm.ru/search/?q='+song
    page = requests.get(url)
    soup = BeautifulSoup(page.text, 'lxml')
    print(soup.select(".items")[0])
    teg = str(soup.select(".items")[0])
    i = 0
    links = []
    for i in range(len(teg) - 4):
        if teg[i] + teg[i + 1] + teg[i + 2] + teg[i + 3] == 'href':
            q = i + 6
            link = ''
            while teg[q] != '"':
                link += teg[q]
                q += 1
            if link != '':
                links.append(link)
    print(links[2])
    page = requests.get('https:' + links[2])
    soup = BeautifulSoup(page.text, 'lxml')
    accords = soup.select(".b-podbor__text > pre:nth-child(1)")[0].text
    return accords, get_accords(accords)



def get_accords(a):
    b = a.split()
    acr = []
    accords = []
    for i in range(len(accords_)):
        q = accords_[i].split()[0]
        acr.append(q)
    for i in range(len(b)):
        b[i] = b[i].replace('B', 'H')
        b[i] = b[i].split('/')[0]
        if b[i] in acr:
            accords.append(b[i])
    return set(accords) 

