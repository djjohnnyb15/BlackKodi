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
from modules.libraries import client


def resolve(url):
    try:
        id = re.compile('//.+?/.+?/([\w]+)').findall(url)
        id += re.compile('//.+?/.+?v=([\w]+)').findall(url)
        id = id[0]

        url = 'http://embed.movshare.net/embed.php?v=%s' % id

        result = client.request(url)

        key = re.compile('flashvars.filekey=(.+?);').findall(result)[-1]
        try: key = re.compile('\s+%s="(.+?)"' % key).findall(result)[-1]
        except: pass

        url = 'http://www.movshare.net/api/player.api.php?key=%s&file=%s' % (key, id)
        result = client.request(url)

        url = re.compile('url=(.+?)&').findall(result)[0]
        return url
    except:
        return

