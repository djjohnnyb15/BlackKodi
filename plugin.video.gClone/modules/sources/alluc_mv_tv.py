# -*- coding: utf-8 -*-

'''
    gClone Add-on
    Copyright (C) 2015 NVTTeam

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
'''


import re
import urllib
import urlparse
import json
import base64
from modules.libraries import cleantitle
from modules.libraries import client
from modules import resolvers


class source:
    def __init__(self):
        self.base_link = 'https://www.alluc.com'
        #self.download_link = '/api/search/download/?apikey=%s&count=20&from=0&getmeta=0&query=%s+lang%%3Aen+host%%3A%s'
        #self.stream_link = '/api/search/stream/?apikey=%s&count=20&from=0&getmeta=0&query=%s+lang%%3Aen+host%%3A%s'
        self.download_link = '/api/search/download/?apikey=%s&count=100&from=0&getmeta=0&query=%s+lang%%3Aen'
        self.stream_link = '/api/search/stream/?apikey=%s&count=100&from=0&getmeta=0&query=%s+lang%%3Aen'
        self.key_link = 'OGRmNzlkYTkyMDc4MDhkNmMyOTA5Njg5MTJlMjc4Nzc='


    def get_movie(self, imdb, title, year):
        try:
            url = '%s %s' % (title, year)
            url = client.replaceHTMLCodes(url)
            url = url.encode('utf-8')
            return url
        except:
            return


    def get_show(self, imdb, tvdb, show, show_alt, year):
        try:
            url = show
            url = client.replaceHTMLCodes(url)
            url = url.encode('utf-8')
            return url
        except:
            return


    def get_episode(self, url, imdb, tvdb, title, date, season, episode):
        try:
            if url == None: return

            url = '%s S%02dE%02d' % (url, int(season), int(episode))
            url = client.replaceHTMLCodes(url)
            url = url.encode('utf-8')
            return url
        except:
            return


    def get_sources(self, url, hosthdDict, hostDict, locDict):
        try:
            sources = []

            if url == None: return sources

            headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; rv:34.0) Gecko/20110101 Firefox/34.0'}
            #params = (base64.urlsafe_b64decode(self.key_link), urllib.quote_plus(url), urllib.quote_plus(','.join(locDict)))
            params = (base64.urlsafe_b64decode(self.key_link), urllib.quote_plus(url))

            links = []

            q = urlparse.urljoin(self.base_link, self.download_link % params)
            try: links += json.loads(client.source(q, headers=headers))['result']
            except: pass

            q = urlparse.urljoin(self.base_link, self.stream_link % params)
            try: links += json.loads(client.source(q, headers=headers))['result']
            except: pass

            title, hdlr = re.compile('(.+?) (\d{4}|S\d*E\d*)$').findall(url)[0]

            if hdlr.isdigit():
                type = 'movie'
                title = cleantitle.movie(title)
                hdlr = [str(hdlr), str(int(hdlr)+1), str(int(hdlr)-1)]
            else:
                type = 'episode'
                title = cleantitle.tv(title)
                hdlr = [hdlr]

            for i in links:
                try:
                    if len(i['hosterurls']) > 1: raise Exception()
                    if not i['extension'] in ['mkv', 'mp4']: raise Exception()

                    host = i['hostername']
                    host = host.rsplit('.', 1)[0]
                    host = host.strip().lower()
                    if not (host in hosthdDict or host in hostDict): raise Exception()
                    host = client.replaceHTMLCodes(host)
                    host = host.encode('utf-8')

                    T = client.replaceHTMLCodes(i['title'])
                    N = client.replaceHTMLCodes(i['sourcetitle'])

                    t = re.sub('(\.|\_|\(|\[|\s)(\d{4}|S\d*E\d*|3D)(\.|\_|\)|\]|\s)(.+)', '', T)
                    if type == 'movie': t = cleantitle.movie(t)
                    else: t = cleantitle.tv(t)
                    n = re.sub('(\.|\_|\(|\[|\s)(\d{4}|S\d*E\d*|3D)(\.|\_|\)|\]|\s)(.+)', '', N)
                    if type == 'movie': n = cleantitle.movie(n)
                    else: n = cleantitle.tv(n)
                    if not (t == title or n == title): raise Exception()

                    y = re.compile('[\.|\_|\(|\[|\s](\d{4}|S\d*E\d*)[\.|\_|\)|\]|\s]').findall(T)
                    y += re.compile('[\.|\_|\(|\[|\s](\d{4}|S\d*E\d*)[\.|\_|\)|\]|\s]').findall(N)
                    y = y[0]
                    if not any(x == y for x in hdlr): raise Exception()

                    fmt = re.sub('(.+)(\.|\_|\(|\[|\s)(\d{4}|S\d*E\d*)(\.|\_|\)|\]|\s)', '', T)
                    fmt += ' ' + re.sub('(.+)(\.|\_|\(|\[|\s)(\d{4}|S\d*E\d*)(\.|\_|\)|\]|\s)', '', N)
                    fmt = re.split('\.|\_|\(|\)|\[|\]|\s|\-', fmt)
                    fmt = [x.lower() for x in fmt]

                    if '1080p' in fmt: quality = '1080p'
                    elif '720p' in fmt: quality = 'HD'
                    else: quality = 'SD'

                    if any(x in ['dvdscr', 'r5', 'r6', 'camrip', 'tsrip', 'hdcam', 'hdts', 'dvdcam', 'dvdts', 'cam', 'ts'] for x in fmt): raise Exception()

                    if quality in ['1080p', 'HD']  and not host in hosthdDict: raise Exception()
                    if quality == 'SD' and not host in hostDict: raise Exception()

                    url = i['hosterurls'][0]['url']
                    url = client.replaceHTMLCodes(url)
                    url = url.encode('utf-8')

                    info = []
                    size = i['sizeinternal']
                    if type == 'movie' and 1 < size < 100000000: raise Exception()
                    size = float(size)/1073741824
                    if not size == 0: info.append('%.2f GB' % size)
                    if '3d' in fmt: info.append('3D')
                    info = ' | '.join(info)

                    sources.append({'source': host, 'quality': quality, 'provider': 'Alluc', 'url': url, 'info': info})
                except:
                    pass

            return sources
        except:
            return sources


    def resolve(self, url):
        try:
            url = resolvers.request(url)
            return url
        except:
            return

