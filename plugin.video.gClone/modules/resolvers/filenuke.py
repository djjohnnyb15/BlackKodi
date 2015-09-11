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
from modules.libraries import client


def resolve(url):
    try:
        result = client.request(url)
        post = {}
        try: f = client.parseDOM(result, "form", attrs = { "method": "POST" })[0]
        except: f = ''
        k = client.parseDOM(f, "input", ret="name")
        for i in k: post.update({i: client.parseDOM(f, "input", ret="value", attrs = { "name": i })[0]})
        post = urllib.urlencode(post)

        result = client.request(url, post=post)

        url = re.compile("var\s+lnk\d* *= *'(http.+?)'").findall(result)[0]
        return url
    except:
        return

