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
from modules.resolvers import googleplus


class source:
    def __init__(self):
        self.base_link = 'https://afdah.org'
        self.search_link = '/results?q=%s'
        self.info_link = '/video_info'


    def get_movie(self, imdb, title, year):
        try:
            query = urlparse.urljoin(self.base_link, self.search_link % (urllib.quote_plus(title)))

            result = client.source(query)
            result = client.parseDOM(result, "div", attrs = { "class": "cell_container" })

            title = cleantitle.movie(title)
            years = ['%s' % str(year), '%s' % str(int(year)+1), '%s' % str(int(year)-1)]
            result = [(client.parseDOM(i, "a", ret="href")[0], client.parseDOM(i, "a", ret="title")[0]) for i in result]
            result = [(i[0], re.compile('(.+?) [(](\d{4})[)]').findall(i[1])) for i in result]
            result = [(i[0], i[1][0][0], i[1][0][1]) for i in result if len(i[1]) > 0]
            result = [i for i in result if title == cleantitle.movie(i[1])]
            result = [i[0] for i in result if any(x in i[2] for x in years)][0]

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

            url = urlparse.urljoin(self.base_link, url)

            result = client.source(url)

            video_id = re.compile('video_id *= *[\'|\"](.+?)[\'|\"]').findall(result)[0]
            post = urllib.urlencode({'video_id': video_id})

            result = client.source(urlparse.urljoin(self.base_link, self.info_link), post=post)

            u = [i for i in result.split('&') if 'google' in i][0]
            u = urllib.unquote_plus(u)
            u = [urllib.unquote_plus(i.split('|')[-1]) for i in u.split(',')]
            u = [googleplus.tag(i)[0] for i in u]
            u = [i for i in u if i['quality'] in ['1080p', 'HD']]

            for i in u: sources.append({'source': 'GVideo', 'quality': i['quality'], 'provider': 'Afdah', 'url': i['url']})

            return sources
        except:
            return sources


    def resolve(self, url):
        try:
            if url.startswith('stack://'): return url

            url = client.request(url, output='geturl')
            if 'requiressl=yes' in url: url = url.replace('http://', 'https://')
            else: url = url.replace('https://', 'http://')
            return url
        except:
            return

