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
from modules.libraries import client
from modules import resolvers


class source:
    def __init__(self):
        self.base_link = 'http://moviestorm.eu'
        self.search_link = '/search'
        self.episode_link = '%s?season=%01d&episode=%01d'


    def get_movie(self, imdb, title, year):
        try:
            query = urlparse.urljoin(self.base_link, self.search_link)
            post = urllib.urlencode({'go': 'Search', 'q': title})

            result = client.source(query, post=post)
            result = client.parseDOM(result, "div", attrs = { "class": "movie_box" })

            imdb = 'tt' + imdb
            result = [i for i in result if imdb in i][0]
            result = client.parseDOM(result, "a", ret="href")[0]

            try: url = re.compile('//.+?(/.+)').findall(result)[0]
            except: url = result
            url = client.replaceHTMLCodes(url)
            url = url.encode('utf-8')
            return url
        except:
            return


    def get_show(self, imdb, tvdb, show, show_alt, year):
        try:
            query = urlparse.urljoin(self.base_link, self.search_link)
            post = urllib.urlencode({'go': 'Search', 'q': show})

            result = client.source(query, post=post)
            result = client.parseDOM(result, "div", attrs = { "class": "movie_box" })

            imdb = 'tt' + imdb
            result = [i for i in result if imdb in i][0]
            result = client.parseDOM(result, "a", ret="href")[0]

            try: url = re.compile('//.+?(/.+)').findall(result)[0]
            except: url = result
            url = client.replaceHTMLCodes(url)
            url = url.encode('utf-8')
            return url
        except:
            return


    def get_episode(self, url, imdb, tvdb, title, date, season, episode):
        if url == None: return

        url = self.episode_link % (url, int(season), int(episode))
        url = client.replaceHTMLCodes(url)
        url = url.encode('utf-8')
        return url


    def get_sources(self, url, hosthdDict, hostDict, locDict):
        try:
            sources = []

            if url == None: return sources

            url = urlparse.urljoin(self.base_link, url)

            result = client.source(url)
            result = client.parseDOM(result, "div", attrs = { "class": "links" })[0]
            result = client.parseDOM(result, "tr")
            result = [(client.parseDOM(i, "td", attrs = { "class": "quality_td" })[0], client.parseDOM(i, "a", ret="href")[-1]) for i in result]

            ts_quality = ['CAM', 'TS']
            links = [i for i in result if not any(x in i[0] for x in ts_quality)]
            if len(links) == 0: links = result

            for i in links:
                try:
                    url = i[1]
                    url = client.replaceHTMLCodes(url)
                    url = url.encode('utf-8')

                    host = re.sub('.+?/exit/\d*-|[.].+?[.]html|http://(|www[.])|/.+|[.].+$','', i[1])
                    host = host.strip().lower()
                    if not host in hostDict: raise Exception()
                    host = client.replaceHTMLCodes(host)
                    host = host.encode('utf-8')

                    if any(x in i[0] for x in ts_quality): quality = 'CAM'
                    else: quality = 'SD'

                    sources.append({'source': host, 'quality': quality, 'provider': 'Moviestorm', 'url': url})
                except:
                    pass

            return sources
        except:
            return sources


    def resolve(self, url):
        try:
            if url.startswith(self.base_link):
                result = client.request(url)
                url = client.parseDOM(result, "a", ret="href", attrs = { "class": "real_link" })[0]

            url = resolvers.request(url)
            return url
        except:
            return

