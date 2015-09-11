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
from modules.libraries import cleantitle
from modules.libraries import client
from modules.resolvers import videomega


class source:
    def __init__(self):
        self.base_link = 'http://movieshd.co'
        self.search_link = '/?s=%s'
        self.videomega_link = 'http://videomega.tv/cdn.php?ref=%s'


    def get_movie(self, imdb, title, year):
        try:
            query = self.search_link % (urllib.quote_plus(title))
            query = urlparse.urljoin(self.base_link, query)

            result = client.source(query)
            result = client.parseDOM(result, "ul", attrs = { "class": "listing-videos.+?" })[0]
            result = client.parseDOM(result, "li", attrs = { "class": ".+?" })

            title = cleantitle.movie(title)
            years = ['(%s)' % str(year), '(%s)' % str(int(year)+1), '(%s)' % str(int(year)-1)]
            result = [(client.parseDOM(i, "a", ret="href")[0], client.parseDOM(i, "a", ret="title")[0]) for i in result]
            result = [i for i in result if title == cleantitle.movie(i[1])]
            result = [i[0] for i in result if any(x in i[1] for x in years)][0]

            try: url = re.compile('//.+?(/.+)').findall(result)[0]
            except: url = result
            url = client.replaceHTMLCodes(url)
            url = url.encode('utf-8')
            return url
        except:
            return


    def get_sources(self, url, hosthdDict, hostDict, locDict):
        try:
            sources = []

            if url == None: return sources

            result = client.source(urlparse.urljoin(self.base_link, url))

            quality = client.parseDOM(result, "title")[0]
            if '[CAM]' in quality or '[TS]' in quality: quality = 'CAM'
            elif '[SCREENER]' in quality: quality = 'SCR'
            else: quality = 'HD'

            result = client.parseDOM(result, "div", attrs = { "class": "video-embed" })[0]

            url = None

            enigma = client.parseDOM(result, "span", ret="data-enigmav")
            if len(enigma) > 0:
                url = enigma[0].decode("unicode-escape")
                url = re.compile('file *: *"(.+?)"').findall(url)[-1]
                url += '|Referer=%s' % urllib.quote_plus(self.base_link)

            mega = re.compile('hashkey=([\w]+)').findall(result)
            mega += re.compile('ref=[\'|\"](.+?)[\'|\"]').findall(result)
            if len(mega) > 0:
                url = self.videomega_link % mega[0]
                url = videomega.resolve(url)

            if url == None: raise Exception()

            sources.append({'source': 'Videomega', 'quality': quality, 'provider': 'MoviesHD', 'url': url})

            return sources
        except:
            return sources


    def resolve(self, url):
        return url

