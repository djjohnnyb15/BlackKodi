# -*- coding: utf-8 -*-

'''
    GOmovies XBMC Addon
    Copyright (C) 2014 lambda

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

import urllib,urllib2,re,os,threading,datetime,time,base64,xbmc,xbmcplugin,xbmcgui,xbmcaddon,xbmcvfs
from operator import itemgetter
try:    import json
except: import simplejson as json
try:    import CommonFunctions
except: import commonfunctionsdummy as CommonFunctions
try:    import StorageServer
except: import storageserverdummy as StorageServer
from metahandler import metahandlers
from metahandler import metacontainers

action              = None
common              = CommonFunctions
metaget             = metahandlers.MetaData(preparezip=False)
language            = xbmcaddon.Addon().getLocalizedString
setSetting          = xbmcaddon.Addon().setSetting
getSetting          = xbmcaddon.Addon().getSetting
addonName           = xbmcaddon.Addon().getAddonInfo("name")
addonVersion        = xbmcaddon.Addon().getAddonInfo("version")
addonId             = xbmcaddon.Addon().getAddonInfo("id")
addonPath           = xbmcaddon.Addon().getAddonInfo("path")
addonFullId         = addonName + addonVersion
addonDesc           = language(30450).encode("utf-8")
cache               = StorageServer.StorageServer(addonFullId,1).cacheFunction
cache2              = StorageServer.StorageServer(addonFullId,24).cacheFunction
cache3              = StorageServer.StorageServer(addonFullId,720).cacheFunction
addonIcon           = os.path.join(addonPath,'icon.png')
addonFanart         = os.path.join(addonPath,'fanart.jpg')
addonLogos          = os.path.join(addonPath,'resources/logos')
addonArt            = os.path.join(addonPath,'resources/art')
addonPoster         = os.path.join(addonPath,'resources/art/Poster.png')
addonDownloads      = os.path.join(addonPath,'resources/art/Downloads.png')
addonGenres         = os.path.join(addonPath,'resources/art/Genres.png')
addonYears          = os.path.join(addonPath,'resources/art/Years.png')
addonLists          = os.path.join(addonPath,'resources/art/Lists.png')
addonNext           = os.path.join(addonPath,'resources/art/Next.png')
dataPath            = xbmc.translatePath('special://profile/addon_data/%s' % (addonId))
viewData            = os.path.join(dataPath,'views.cfg')
offData             = os.path.join(dataPath,'offset.cfg')
favData             = os.path.join(dataPath,'favourites.cfg')


class main:
    def __init__(self):
        global action
        cacheToDisc = True
        index().container_data()
        index().settings_reset()
        params = {}
        splitparams = sys.argv[2][sys.argv[2].find('?') + 1:].split('&')
        for param in splitparams:
            if (len(param) > 0):
                splitparam = param.split('=')
                key = splitparam[0]
                try:    value = splitparam[1].encode("utf-8")
                except: value = splitparam[1]
                params[key] = value

        try:        action = urllib.unquote_plus(params["action"])
        except:     action = None
        try:        name = urllib.unquote_plus(params["name"])
        except:     name = None
        try:        url = urllib.unquote_plus(params["url"])
        except:     url = None
        try:        image = urllib.unquote_plus(params["image"])
        except:     image = None
        try:        query = urllib.unquote_plus(params["query"])
        except:     query = None
        try:        source = urllib.unquote_plus(params["source"])
        except:     source = None
        try:        provider = urllib.unquote_plus(params["provider"])
        except:     provider = None
        try:        title = urllib.unquote_plus(params["title"])
        except:     title = None
        try:        year = urllib.unquote_plus(params["year"])
        except:     year = None
        try:        genre = urllib.unquote_plus(params["genre"])
        except:     genre = None
        try:        plot = urllib.unquote_plus(params["plot"])
        except:     plot = None
        try:        imdb = urllib.unquote_plus(params["imdb"])
        except:     imdb = None

        if action == None:                          root().get()
        elif action == 'root_search':               root().search()
        elif action == 'item_play':                 contextMenu().item_play()
        elif action == 'item_random_play':          contextMenu().item_random_play()
        elif action == 'item_queue':                contextMenu().item_queue()
        elif action == 'favourite_add':             contextMenu().favourite_add(favData, name, url, image, imdb, year)
        elif action == 'favourite_from_search':     contextMenu().favourite_from_search(favData, name, url, image, imdb, year)
        elif action == 'favourite_delete':          contextMenu().favourite_delete(favData, name, url)
        elif action == 'favourite_moveUp':          contextMenu().favourite_moveUp(favData, name, url)
        elif action == 'favourite_moveDown':        contextMenu().favourite_moveDown(favData, name, url)
        elif action == 'playlist_open':             contextMenu().playlist_open()
        elif action == 'settings_open':             contextMenu().settings_open()
        elif action == 'addon_home':                contextMenu().addon_home()
        elif action == 'view_movies':               contextMenu().view('movies')
        elif action == 'metadata_movies':           contextMenu().metadata('movie', imdb, '', '')
        elif action == 'metadata_movies2':          contextMenu().metadata('movie', imdb, '', '')
        elif action == 'playcount_movies':          contextMenu().playcount('movie', imdb, '', '')
        elif action == 'library_add':               contextMenu().library_add(name, title, imdb, year, url)
        elif action == 'library_batch':             contextMenu().library_batch(url)
        elif action == 'library_update':            contextMenu().library_update()
        elif action == 'library_service':           contextMenu().library_update(silent=True)
        elif action == 'download':                  contextMenu().download(name, url, provider)
        elif action == 'autoplay':                  contextMenu().autoplay(name, title, imdb, year, url)
        elif action == 'trailer':                   contextMenu().trailer(name, url)
        elif action == 'movies_favourites':         favourites().movies()
        elif action == 'movies':                    movies().get(url)
        elif action == 'movies_userlists':          movies().get(url)
        elif action == 'movies_popular':            movies().popular()
        elif action == 'movies_boxoffice':          movies().boxoffice()
        elif action == 'movies_views':              movies().views()
        elif action == 'movies_oscars':             movies().oscars()
        elif action == 'movies_added':              movies().added()
        elif action == 'movies_trending':           movies().trending()
        elif action == 'movies_search':             movies().search(query)
        elif action == 'actors_search':             actors().search(query)
        elif action == 'channels_movies':           channels().get()
        elif action == 'genres_movies':             genres().get()
        elif action == 'years_movies':              years().get()
        elif action == 'userlists_trakt':           userlists().trakt()
        elif action == 'userlists_imdb':            userlists().imdb()
        elif action == 'get_host':                  resolver().get_host(name, title, imdb, year, url, image, genre, plot)
        elif action == 'play_host':                 resolver().play_host(name, url, imdb, source, provider)
        elif action == 'play':                      resolver().play(name, title, imdb, year, url)

        if action is None:
            pass
        elif action.startswith('movies'):
            xbmcplugin.setContent(int(sys.argv[1]), 'movies')
            index().container_view('movies', {'skin.confluence' : 500})
            if not action.endswith('_search'): cacheToDisc = False
        elif action.startswith('channels'):
            xbmcplugin.setContent(int(sys.argv[1]), 'episodes')
            cacheToDisc = False
        xbmcplugin.setPluginFanart(int(sys.argv[1]), addonFanart)
        xbmcplugin.endOfDirectory(int(sys.argv[1]), cacheToDisc=cacheToDisc)
        return

class getUrl(object):
    def __init__(self, url, close=True, proxy=None, post=None, mobile=False, referer=None, cookie=None, output='', timeout='10'):
        if not proxy is None:
            proxy_handler = urllib2.ProxyHandler({'http':'%s' % (proxy)})
            opener = urllib2.build_opener(proxy_handler, urllib2.HTTPHandler)
            opener = urllib2.install_opener(opener)
        if output == 'cookie' or not close == True:
            import cookielib
            cookie_handler = urllib2.HTTPCookieProcessor(cookielib.LWPCookieJar())
            opener = urllib2.build_opener(cookie_handler, urllib2.HTTPBasicAuthHandler(), urllib2.HTTPHandler())
            opener = urllib2.install_opener(opener)
        if not post is None:
            request = urllib2.Request(url, post)
        else:
            request = urllib2.Request(url,None)
        if mobile == True:
            request.add_header('User-Agent', 'Mozilla/5.0 (iPhone; CPU; CPU iPhone OS 4_0 like Mac OS X; en-us) AppleWebKit/532.9 (KHTML, like Gecko) Version/4.0.5 Mobile/8A293 Safari/6531.22.7')
        else:
            request.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/29.0.1547.57 Safari/537.36')
        if not referer is None:
            request.add_header('Referer', referer)
        if not cookie is None:
            request.add_header('cookie', cookie)
        response = urllib2.urlopen(request, timeout=int(timeout))
        if output == 'cookie':
            result = str(response.headers.get('Set-Cookie'))
        elif output == 'geturl':
            result = response.geturl()
        else:
            result = response.read()
        if close == True:
            response.close()
        self.result = result

class uniqueList(object):
    def __init__(self, list):
        uniqueSet = set()
        uniqueList = []
        for n in list:
            if n not in uniqueSet:
                uniqueSet.add(n)
                uniqueList.append(n)
        self.list = uniqueList

class Thread(threading.Thread):
    def __init__(self, target, *args):
        self._target = target
        self._args = args
        threading.Thread.__init__(self)
    def run(self):
        self._target(*self._args)

class player(xbmc.Player):
    def __init__ (self):
        self.folderPath = xbmc.getInfoLabel('Container.FolderPath')
        self.PseudoTVRunning = index().getProperty('PseudoTVRunning')
        self.loadingStarting = time.time()
        xbmc.Player.__init__(self)

    def run(self, name, url, imdb='0'):
        self.video_info(name, imdb)

        if self.folderPath.startswith(sys.argv[0]) or self.PseudoTVRunning == 'True':
            item = xbmcgui.ListItem(path=url)
            xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, item)
        else:
            try:
                file = self.name + '.strm'
                file = file.translate(None, '\/:*?"<>|')

                meta = xbmc.executeJSONRPC('{"jsonrpc": "2.0", "method": "VideoLibrary.GetMovies", "params": {"filter":{"or": [{"field": "year", "operator": "is", "value": "%s"}, {"field": "year", "operator": "is", "value": "%s"}, {"field": "year", "operator": "is", "value": "%s"}]}, "properties" : ["title", "genre", "year", "rating", "director", "trailer", "tagline", "plot", "plotoutline", "originaltitle", "lastplayed", "playcount", "writer", "studio", "mpaa", "country", "imdbnumber", "runtime", "votes", "fanart", "thumbnail", "file", "sorttitle", "resume", "dateadded"]}, "id": 1}' % (self.year, str(int(self.year)+1), str(int(self.year)-1)))
                meta = unicode(meta, 'utf-8', errors='ignore')
                meta = json.loads(meta)
                meta = meta['result']['movies']
                self.meta = [i for i in meta if i['file'].endswith(file)][0]
                meta = {'title': self.meta['title'], 'originaltitle': self.meta['originaltitle'], 'year': self.meta['year'], 'genre': str(self.meta['genre']).replace("[u'", '').replace("']", '').replace("', u'", ' / '), 'director': str(self.meta['director']).replace("[u'", '').replace("']", '').replace("', u'", ' / '), 'country': str(self.meta['country']).replace("[u'", '').replace("']", '').replace("', u'", ' / '), 'rating': self.meta['rating'], 'votes': self.meta['votes'], 'mpaa': self.meta['mpaa'], 'duration': self.meta['runtime'], 'trailer': self.meta['trailer'], 'writer': str(self.meta['writer']).replace("[u'", '').replace("']", '').replace("', u'", ' / '), 'studio': str(self.meta['studio']).replace("[u'", '').replace("']", '').replace("', u'", ' / '), 'tagline': self.meta['tagline'], 'plotoutline': self.meta['plotoutline'], 'plot': self.meta['plot']}
                poster = self.meta['thumbnail']
            except:
                meta = {'label': self.name, 'title': self.name}
                poster = ''
            item = xbmcgui.ListItem(path=url, iconImage="DefaultVideo.png", thumbnailImage=poster)
            item.setInfo( type="Video", infoLabels= meta )
            xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, item)

        for i in range(0, 250):
            try: self.totalTime = self.getTotalTime()
            except: self.totalTime = 0
            if not self.totalTime == 0: continue
            xbmc.sleep(1000)
        if self.totalTime == 0: return

        while True:
            try: self.currentTime = self.getTime()
            except: break
            xbmc.sleep(1000)

    def video_info(self, name, imdb):
        self.name = name
        self.content = 'movie'
        self.title = self.name.rsplit(' (', 1)[0].strip()
        self.year = '%04d' % int(self.name.rsplit(' (', 1)[-1].split(')')[0])
        if imdb == '0': imdb = metaget.get_meta('movie', self.title ,year=str(self.year))['imdb_id']
        self.imdb = re.sub('[^0-9]', '', imdb)
        self.subtitle = subtitles().get(self.name, self.imdb, '', '')

    def offset_add(self):
        try:
            file = xbmcvfs.File(offData)
            read = file.read()
            file.close()
            write = [i.strip('\n').strip('\r') for i in read.splitlines(True) if i.strip('\r\n')]
            write.append('"%s"|"%s"|"%s"' % (self.name, self.imdb, self.currentTime))
            write = '\r\n'.join(write)
            file = xbmcvfs.File(offData, 'w')
            file.write(str(write))
            file.close()
        except:
            return

    def offset_delete(self):
        try:
            file = xbmcvfs.File(offData)
            read = file.read()
            file.close()
            write = [i.strip('\n').strip('\r') for i in read.splitlines(True) if i.strip('\r\n')]
            write = [i for i in write if not '"%s"|"%s"|"' % (self.name, self.imdb) in i]
            write = '\r\n'.join(write)
            file = xbmcvfs.File(offData, 'w')
            file.write(str(write))
            file.close()
        except:
            return

    def offset_read(self):
        try:
            self.offset = '0'
            file = xbmcvfs.File(offData)
            read = file.read()
            file.close()
            read = [i for i in read.splitlines(True) if '"%s"|"%s"|"' % (self.name, self.imdb) in i][0]
            self.offset = re.compile('".+?"[|]".+?"[|]"(.+?)"').findall(read)[0]
        except:
            return

    def change_watched(self):
        try:
            xbmc.executeJSONRPC('{"jsonrpc": "2.0", "method": "VideoLibrary.SetMovieDetails", "params": {"movieid" : %s, "playcount" : 1 }, "id": 1 }' % str(self.meta['movieid']))
        except:
            metaget.change_watched(self.content, '', self.imdb, season='', episode='', year='', watched=7)

    def resume_playback(self):
        offset = float(self.offset)
        if not offset > 0: return
        minutes, seconds = divmod(offset, 60)
        hours, minutes = divmod(minutes, 60)
        offset_time = '%02d:%02d:%02d' % (hours, minutes, seconds)
        yes = index().yesnoDialog('%s %s' % (language(30350).encode("utf-8"), offset_time), '', self.name, language(30351).encode("utf-8"), language(30352).encode("utf-8"))
        if yes: self.seekTime(offset)

    def onPlayBackStarted(self):
        try: self.setSubtitles(self.subtitle)
        except: pass

        if self.PseudoTVRunning == 'True': return

        if getSetting("playback_info") == 'true':
            elapsedTime = '%s %.2f seconds' % (language(30319).encode("utf-8"), (time.time() - self.loadingStarting))     
            index().infoDialog(elapsedTime, header=self.name)

        if getSetting("resume_playback") == 'true':
            self.offset_read()
            self.resume_playback()

    def onPlayBackEnded(self):
        if self.PseudoTVRunning == 'True': return
        self.change_watched()
        self.offset_delete()

    def onPlayBackStopped(self):
        if self.PseudoTVRunning == 'True': return
        if self.currentTime / self.totalTime >= .9:
            self.change_watched()
        self.offset_delete()
        self.offset_add()

class subtitles:
    def get(self, name, imdb, season, episode):
        if not getSetting("subtitles") == 'true': return
        quality = ['bluray', 'hdrip', 'brrip', 'bdrip', 'dvdrip', 'webrip', 'hdtv']
        langDict = {'Afrikaans': 'afr', 'Albanian': 'alb', 'Arabic': 'ara', 'Armenian': 'arm', 'Basque': 'baq', 'Bengali': 'ben', 'Bosnian': 'bos', 'Breton': 'bre', 'Bulgarian': 'bul', 'Burmese': 'bur', 'Catalan': 'cat', 'Chinese': 'chi', 'Croatian': 'hrv', 'Czech': 'cze', 'Danish': 'dan', 'Dutch': 'dut', 'English': 'eng', 'Esperanto': 'epo', 'Estonian': 'est', 'Finnish': 'fin', 'French': 'fre', 'Galician': 'glg', 'Georgian': 'geo', 'German': 'ger', 'Greek': 'ell', 'Hebrew': 'heb', 'Hindi': 'hin', 'Hungarian': 'hun', 'Icelandic': 'ice', 'Indonesian': 'ind', 'Italian': 'ita', 'Japanese': 'jpn', 'Kazakh': 'kaz', 'Khmer': 'khm', 'Korean': 'kor', 'Latvian': 'lav', 'Lithuanian': 'lit', 'Luxembourgish': 'ltz', 'Macedonian': 'mac', 'Malay': 'may', 'Malayalam': 'mal', 'Manipuri': 'mni', 'Mongolian': 'mon', 'Montenegrin': 'mne', 'Norwegian': 'nor', 'Occitan': 'oci', 'Persian': 'per', 'Polish': 'pol', 'Portuguese': 'por,pob', 'Portuguese(Brazil)': 'pob,por', 'Romanian': 'rum', 'Russian': 'rus', 'Serbian': 'scc', 'Sinhalese': 'sin', 'Slovak': 'slo', 'Slovenian': 'slv', 'Spanish': 'spa', 'Swahili': 'swa', 'Swedish': 'swe', 'Syriac': 'syr', 'Tagalog': 'tgl', 'Tamil': 'tam', 'Telugu': 'tel', 'Thai': 'tha', 'Turkish': 'tur', 'Ukrainian': 'ukr', 'Urdu': 'urd'}

        langs = []
        try: langs.append(langDict[getSetting("sublang1")])
        except: pass
        try: langs.append(langDict[getSetting("sublang2")])
        except: pass
        langs = ','.join(langs)

        try:
            import xmlrpclib
            server = xmlrpclib.Server('http://api.opensubtitles.org/xml-rpc', verbose=0)
            token = server.LogIn('', '', 'en', 'XBMC_Subtitles_v1')['token']
            result = server.SearchSubtitles(token, [{'sublanguageid': langs, 'imdbid': imdb}])['data']
            result = [i for i in result if i['SubSumCD'] == '1']
        except:
            return

        subtitles = []
        for lang in langs.split(','):
            filter = [i for i in result if lang == i['SubLanguageID']]
            if filter == []: continue
            for q in quality: subtitles += [i for i in filter if q in i['MovieReleaseName'].lower()]
            subtitles += [i for i in filter if not any(x in i['MovieReleaseName'].lower() for x in quality)]
            try: lang = xbmc.convertLanguage(lang, xbmc.ISO_639_1)
            except: pass
            break

        try:
            import zlib, base64
            content = [subtitles[0]["IDSubtitleFile"],]
            content = server.DownloadSubtitles(token, content)
            content = base64.b64decode(content['data'][0]['data'])
            content = zlib.decompressobj(16+zlib.MAX_WBITS).decompress(content)

            subtitle = xbmc.translatePath('special://temp/')
            subtitle = os.path.join(subtitle, 'TemporarySubs.%s.srt' % lang)
            file = open(subtitle, 'wb')
            file.write(content)
            file.close()

            return subtitle
        except:
            index().infoDialog(language(30317).encode("utf-8"), name)
            return

class index:
    def infoDialog(self, str, header=addonName):
        try: xbmcgui.Dialog().notification(header, str, addonIcon, 3000, sound=False)
        except: xbmc.executebuiltin("Notification(%s,%s, 3000, %s)" % (header, str, addonIcon))

    def okDialog(self, str1, str2, header=addonName):
        xbmcgui.Dialog().ok(header, str1, str2)

    def selectDialog(self, list, header=addonName):
        select = xbmcgui.Dialog().select(header, list)
        return select

    def yesnoDialog(self, str1, str2, header=addonName, str3='', str4=''):
        answer = xbmcgui.Dialog().yesno(header, str1, str2, '', str4, str3)
        return answer

    def getProperty(self, str):
        property = xbmcgui.Window(10000).getProperty(str)
        return property

    def setProperty(self, str1, str2):
        xbmcgui.Window(10000).setProperty(str1, str2)

    def clearProperty(self, str):
        xbmcgui.Window(10000).clearProperty(str)

    def addon_status(self, id):
        check = xbmcaddon.Addon(id=id).getAddonInfo("name")
        if not check == addonName: return True

    def container_refresh(self):
        xbmc.executebuiltin("Container.Refresh")

    def container_data(self):
        if not xbmcvfs.exists(dataPath):
            xbmcvfs.mkdir(dataPath)
        if not xbmcvfs.exists(favData):
            file = xbmcvfs.File(favData, 'w')
            file.write('')
            file.close()
        if not xbmcvfs.exists(viewData):
            file = xbmcvfs.File(viewData, 'w')
            file.write('')
            file.close()
        if not xbmcvfs.exists(offData):
            file = xbmcvfs.File(offData, 'w')
            file.write('')
            file.close()

    def settings_reset(self):
        try:
            if getSetting("settings_version") == '2.6.0': return
            settings = os.path.join(addonPath,'resources/settings.xml')
            file = xbmcvfs.File(settings)
            read = file.read()
            file.close()
            for i in range (1,12): setSetting('hosthd' + str(i), common.parseDOM(read, "setting", ret="default", attrs = {"id": 'hosthd' + str(i)})[0])
            for i in range (1,16): setSetting('host' + str(i), common.parseDOM(read, "setting", ret="default", attrs = {"id": 'host' + str(i)})[0])
            setSetting('settings_version', '2.6.0')
        except:
            return

    def container_view(self, content, viewDict):
        try:
            skin = xbmc.getSkinDir()
            file = xbmcvfs.File(viewData)
            read = file.read().replace('\n','')
            file.close()
            view = re.compile('"%s"[|]"%s"[|]"(.+?)"' % (skin, content)).findall(read)[0]
            xbmc.executebuiltin('Container.SetViewMode(%s)' % str(view))
        except:
            try:
                id = str(viewDict[skin])
                xbmc.executebuiltin('Container.SetViewMode(%s)' % id)
            except:
                pass

    def rootList(self, rootList):
        total = len(rootList)
        for i in rootList:
            try:
                name = language(i['name']).encode("utf-8")
                image = '%s/%s' % (addonArt, i['image'])
                action = i['action']
                u = '%s?action=%s' % (sys.argv[0], action)

                cm = []
                cm.append((language(30426).encode("utf-8"), 'RunPlugin(%s?action=library_update)' % (sys.argv[0])))
                if action == 'movies_added' or action == 'movies_trending':
                    cm.append((language(30422).encode("utf-8"), 'RunPlugin(%s?action=library_batch&url=%s)' % (sys.argv[0], action)))

                item = xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=image)
                item.setInfo( type="Video", infoLabels={ "Label": name, "Title": name, "Plot": addonDesc } )
                item.setProperty("Fanart_Image", addonFanart)
                item.addContextMenuItems(cm, replaceItems=False)
                xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=item,totalItems=total,isFolder=True)
            except:
                pass

    def pageList(self, pageList):
        if pageList == None: return

        total = len(pageList)
        for i in pageList:
            try:
                name, url, image = i['name'], i['url'], i['image']
                sysname, sysurl, sysimage = urllib.quote_plus(name), urllib.quote_plus(url), urllib.quote_plus(image)

                u = '%s?action=movies&url=%s' % (sys.argv[0], sysurl)

                item = xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=image)
                item.setInfo( type="Video", infoLabels={ "Label": name, "Title": name, "Plot": addonDesc } )
                item.setProperty("Fanart_Image", addonFanart)
                item.addContextMenuItems([], replaceItems=False)
                xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=item,totalItems=total,isFolder=True)
            except:
                pass

    def userList(self, userList):
        if userList == None: return

        total = len(userList)
        for i in userList:
            try:
                name, url, image = i['name'], i['url'], i['image']
                sysname, sysurl, sysimage = urllib.quote_plus(name), urllib.quote_plus(url), urllib.quote_plus(image)

                u = '%s?action=movies_userlists&url=%s' % (sys.argv[0], sysurl)

                cm = []
                cm.append((language(30422).encode("utf-8"), 'RunPlugin(%s?action=library_batch&url=%s)' % (sys.argv[0], sysurl)))

                item = xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=image)
                item.setInfo( type="Video", infoLabels={ "Label": name, "Title": name, "Plot": addonDesc } )
                item.setProperty("Fanart_Image", addonFanart)
                item.addContextMenuItems(cm, replaceItems=False)
                xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=item,totalItems=total,isFolder=True)
            except:
                pass

    def nextList(self, nextList):
        try: next = nextList[0]['next']
        except: return
        if next == '': return
        name, url, image = language(30361).encode("utf-8"), next, addonNext
        sysurl = urllib.quote_plus(url)

        u = '%s?action=movies&url=%s' % (sys.argv[0], sysurl)

        item = xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=image)
        item.setInfo( type="Video", infoLabels={ "Label": name, "Title": name, "Plot": addonDesc } )
        item.setProperty("Fanart_Image", addonFanart)
        item.addContextMenuItems([], replaceItems=False)
        xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=item,isFolder=True)

    def downloadList(self):
        u = getSetting("downloads")
        if u == '': return
        name, image = language(30363).encode("utf-8"), addonDownloads

        item = xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=image)
        item.setInfo( type="Video", infoLabels={ "Label": name, "Title": name, "Plot": addonDesc } )
        item.setProperty("Fanart_Image", addonFanart)
        item.addContextMenuItems([], replaceItems=False)
        xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=item,isFolder=True)

    def channelList(self, channelList):
        if channelList == None: return

        total = len(channelList)
        for i in channelList:
            try:
                channel, title, year, imdb, genre, plot = i['name'], i['title'], i['year'], i['imdb'], i['genre'], i['plot']
                image = '%s/%s.png' % (addonLogos, channel)
                name = '%s (%s)' % (title, year)
                label = "[B]%s[/B] : %s" % (channel.upper(), name)
                if plot == '': plot = addonDesc
                if genre == '': genre = ' '

                sysname, sysurl, sysimage, systitle, sysyear, sysimdb, sysgenre, sysplot = urllib.quote_plus(name), urllib.quote_plus(name), urllib.quote_plus(image), urllib.quote_plus(title), urllib.quote_plus(year), urllib.quote_plus(imdb), urllib.quote_plus(genre), urllib.quote_plus(plot)

                if not getSetting("autoplay") == 'false':
                    u = '%s?action=play&name=%s&title=%s&imdb=%s&year=%s&url=%s&t=%s' % (sys.argv[0], sysname, systitle, sysimdb, sysyear, sysurl, datetime.datetime.now().strftime("%Y%m%d%H%M%S%f"))
                    isFolder = False
                else:
                    u = '%s?action=get_host&name=%s&title=%s&imdb=%s&year=%s&url=%s&image=%s&genre=%s&plot=%s&t=%s' % (sys.argv[0], sysname, systitle, sysimdb, sysyear, sysurl, sysimage, sysgenre, sysplot, datetime.datetime.now().strftime("%Y%m%d%H%M%S%f"))
                    isFolder = True

                meta = {'Label': title, 'Title': title, 'Studio': channel, 'Duration': '1440', 'Plot': plot}

                cm = []
                cm.append((language(30433).encode("utf-8"), 'RunPlugin(%s?action=autoplay&name=%s&title=%s&imdb=%s&year=%s&url=%s)' % (sys.argv[0], sysname, systitle, sysimdb, sysyear, sysurl)))
                cm.append((language(30416).encode("utf-8"), 'RunPlugin(%s?action=trailer&name=%s&url=%s)' % (sys.argv[0], sysname, sysurl)))
                cm.append((language(30409).encode("utf-8"), 'RunPlugin(%s?action=settings_open)' % (sys.argv[0])))
                cm.append((language(30411).encode("utf-8"), 'RunPlugin(%s?action=addon_home)' % (sys.argv[0])))

                item = xbmcgui.ListItem(label, iconImage=image, thumbnailImage=image)
                item.setInfo( type="Video", infoLabels = meta )
                item.setProperty("IsPlayable", "true")
                item.setProperty("Video", "true")
                item.setProperty("Fanart_Image", addonFanart)
                item.addContextMenuItems(cm, replaceItems=True)
                xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=item,totalItems=total,isFolder=isFolder)
            except:
                pass

    def movieList(self, movieList):
        if movieList == None: return

        autoplay = getSetting("autoplay")
        if index().getProperty('PseudoTVRunning') == 'True': autoplay = 'true'

        getmeta = getSetting("meta")
        if action == 'movies_search': getmeta = ''

        file = xbmcvfs.File(favData)
        favRead = file.read()
        file.close()

        total = len(movieList)
        for i in movieList:
            try:
                name, url, image, title, year, imdb, genre, plot = i['name'], i['url'], i['image'], i['title'], i['year'], i['imdb'], i['genre'], i['plot']
                if plot == '': plot = addonDesc
                if genre == '': genre = ' '

                sysname, sysurl, sysimage, systitle, sysyear, sysimdb, sysgenre, sysplot = urllib.quote_plus(name), urllib.quote_plus(url), urllib.quote_plus(image), urllib.quote_plus(title), urllib.quote_plus(year), urllib.quote_plus(imdb), urllib.quote_plus(genre), urllib.quote_plus(plot)

                if not autoplay == 'false':
                    u = '%s?action=play&name=%s&title=%s&imdb=%s&year=%s&url=%s&t=%s' % (sys.argv[0], sysname, systitle, sysimdb, sysyear, sysurl, datetime.datetime.now().strftime("%Y%m%d%H%M%S%f"))
                    isFolder = False
                else:
                    u = '%s?action=get_host&name=%s&title=%s&imdb=%s&year=%s&url=%s&image=%s&genre=%s&plot=%s' % (sys.argv[0], sysname, systitle, sysimdb, sysyear, sysurl, sysimage, sysgenre, sysplot)
                    isFolder = True

                if getmeta == 'true':
                    meta = metaget.get_meta('movie', title ,year=year)
                    playcountMenu = language(30407).encode("utf-8")
                    if meta['overlay'] == 6: playcountMenu = language(30408).encode("utf-8")
                    metaimdb = urllib.quote_plus(re.sub('[^0-9]', '', meta['imdb_id']))
                    trailer, poster = urllib.quote_plus(meta['trailer_url']), meta['cover_url']
                    if trailer == '': trailer = sysurl
                    if poster == '': poster = image
                else:
                    meta = {'label': title, 'title': title, 'year': year, 'imdb_id' : imdb, 'genre' : genre, 'plot': plot}
                    trailer, poster = sysurl, image
                if getmeta == 'true' and getSetting("fanart") == 'true':
                    fanart = meta['backdrop_url']
                    if fanart == '': fanart = addonFanart
                else:
                    fanart = addonFanart

                cm = []
                cm.append((language(30433).encode("utf-8"), 'RunPlugin(%s?action=autoplay&name=%s&title=%s&imdb=%s&year=%s&url=%s)' % (sys.argv[0], sysname, systitle, sysimdb, sysyear, sysurl)))

                if action == 'movies_favourites':
                    if not getSetting("fav_sort") == '2': cm.append((language(30412).encode("utf-8"), 'Action(Info)'))
                    cm.append((language(30416).encode("utf-8"), 'RunPlugin(%s?action=trailer&name=%s&url=%s)' % (sys.argv[0], sysname, trailer)))
                    if getmeta == 'true': cm.append((language(30415).encode("utf-8"), 'RunPlugin(%s?action=metadata_movies&imdb=%s)' % (sys.argv[0], metaimdb)))
                    if getmeta == 'true': cm.append((playcountMenu, 'RunPlugin(%s?action=playcount_movies&imdb=%s)' % (sys.argv[0], metaimdb)))
                    cm.append((language(30422).encode("utf-8"), 'RunPlugin(%s?action=library_add&name=%s&title=%s&imdb=%s&year=%s&url=%s)' % (sys.argv[0], sysname, systitle, sysimdb, sysyear, sysurl)))
                    cm.append((language(30428).encode("utf-8"), 'RunPlugin(%s?action=view_movies)' % (sys.argv[0])))
                    if getSetting("fav_sort") == '2': cm.append((language(30419).encode("utf-8"), 'RunPlugin(%s?action=favourite_moveUp&name=%s&url=%s)' % (sys.argv[0], systitle, sysurl)))
                    if getSetting("fav_sort") == '2': cm.append((language(30420).encode("utf-8"), 'RunPlugin(%s?action=favourite_moveDown&name=%s&url=%s)' % (sys.argv[0], systitle, sysurl)))
                    cm.append((language(30421).encode("utf-8"), 'RunPlugin(%s?action=favourite_delete&name=%s&url=%s)' % (sys.argv[0], systitle, sysurl)))
                elif action == 'movies_search':
                    cm.append((language(30412).encode("utf-8"), 'Action(Info)'))
                    cm.append((language(30416).encode("utf-8"), 'RunPlugin(%s?action=trailer&name=%s&url=%s)' % (sys.argv[0], sysname, trailer)))
                    cm.append((language(30422).encode("utf-8"), 'RunPlugin(%s?action=library_add&name=%s&title=%s&imdb=%s&year=%s&url=%s)' % (sys.argv[0], sysname, systitle, sysimdb, sysyear, sysurl)))
                    cm.append((language(30417).encode("utf-8"), 'RunPlugin(%s?action=favourite_from_search&name=%s&imdb=%s&url=%s&image=%s&year=%s)' % (sys.argv[0], systitle, sysimdb, sysurl, sysimage, sysyear)))
                    cm.append((language(30428).encode("utf-8"), 'RunPlugin(%s?action=view_movies)' % (sys.argv[0])))
                    cm.append((language(30409).encode("utf-8"), 'RunPlugin(%s?action=settings_open)' % (sys.argv[0])))
                    cm.append((language(30411).encode("utf-8"), 'RunPlugin(%s?action=addon_home)' % (sys.argv[0])))
                elif action == 'movies_userlists':
                    cm.append((language(30412).encode("utf-8"), 'Action(Info)'))
                    cm.append((language(30416).encode("utf-8"), 'RunPlugin(%s?action=trailer&name=%s&url=%s)' % (sys.argv[0], sysname, trailer)))
                    if getmeta == 'true': cm.append((language(30415).encode("utf-8"), 'RunPlugin(%s?action=metadata_movies2&imdb=%s)' % (sys.argv[0], metaimdb)))
                    if getmeta == 'true': cm.append((playcountMenu, 'RunPlugin(%s?action=playcount_movies&imdb=%s)' % (sys.argv[0], metaimdb)))
                    cm.append((language(30422).encode("utf-8"), 'RunPlugin(%s?action=library_add&name=%s&title=%s&imdb=%s&year=%s&url=%s)' % (sys.argv[0], sysname, systitle, sysimdb, sysyear, sysurl)))
                    if not '"%s"' % url in favRead: cm.append((language(30417).encode("utf-8"), 'RunPlugin(%s?action=favourite_add&name=%s&imdb=%s&url=%s&image=%s&year=%s)' % (sys.argv[0], systitle, sysimdb, sysurl, sysimage, sysyear)))
                    else: cm.append((language(30418).encode("utf-8"), 'RunPlugin(%s?action=favourite_delete&name=%s&url=%s)' % (sys.argv[0], systitle, sysurl)))
                    cm.append((language(30428).encode("utf-8"), 'RunPlugin(%s?action=view_movies)' % (sys.argv[0])))
                else:
                    cm.append((language(30412).encode("utf-8"), 'Action(Info)'))
                    cm.append((language(30416).encode("utf-8"), 'RunPlugin(%s?action=trailer&name=%s&url=%s)' % (sys.argv[0], sysname, trailer)))
                    if getmeta == 'true': cm.append((language(30415).encode("utf-8"), 'RunPlugin(%s?action=metadata_movies2&imdb=%s)' % (sys.argv[0], metaimdb)))
                    if getmeta == 'true': cm.append((playcountMenu, 'RunPlugin(%s?action=playcount_movies&imdb=%s)' % (sys.argv[0], metaimdb)))
                    cm.append((language(30422).encode("utf-8"), 'RunPlugin(%s?action=library_add&name=%s&title=%s&imdb=%s&year=%s&url=%s)' % (sys.argv[0], sysname, systitle, sysimdb, sysyear, sysurl)))
                    if not '"%s"' % url in favRead: cm.append((language(30417).encode("utf-8"), 'RunPlugin(%s?action=favourite_add&name=%s&imdb=%s&url=%s&image=%s&year=%s)' % (sys.argv[0], systitle, sysimdb, sysurl, sysimage, sysyear)))
                    else: cm.append((language(30418).encode("utf-8"), 'RunPlugin(%s?action=favourite_delete&name=%s&url=%s)' % (sys.argv[0], systitle, sysurl)))
                    cm.append((language(30428).encode("utf-8"), 'RunPlugin(%s?action=view_movies)' % (sys.argv[0])))
                    cm.append((language(30411).encode("utf-8"), 'RunPlugin(%s?action=addon_home)' % (sys.argv[0])))

                item = xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=poster)
                item.setInfo( type="Video", infoLabels = meta )
                item.setProperty("IsPlayable", "true")
                item.setProperty("Video", "true")
                item.setProperty("art(poster)", poster)
                item.setProperty("Fanart_Image", fanart)
                item.addContextMenuItems(cm, replaceItems=True)
                xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=item,totalItems=total,isFolder=isFolder)
            except:
                pass

    def sourceList(self, sourceList):
        if sourceList == None: return

        try:
            name, image, title, year, imdb, genre, plot = sourceList[0]['name'], sourceList[0]['image'], sourceList[0]['title'], sourceList[0]['year'], sourceList[0]['imdb'], sourceList[0]['genre'], sourceList[0]['plot']
            if plot == '': plot = addonDesc
            if genre == '': genre = ' '

            if getSetting("meta") == 'true':
                meta = metaget.get_meta('movie', title ,year=year)
                meta.update({'playcount': 0, 'overlay': 0})
                trailer, poster = urllib.quote_plus(meta['trailer_url']), meta['cover_url']
                if trailer == '': trailer = urllib.quote_plus(name)
                if poster == '': poster = image
            else:
                meta = {'label': title, 'title': title, 'year': year, 'imdb_id' : imdb, 'genre' : genre, 'plot': plot}
                trailer, poster = urllib.quote_plus(name), image
            if getSetting("meta") == 'true' and getSetting("fanart") == 'true':
                fanart = meta['backdrop_url']
                if fanart == '': fanart = addonFanart
            else:
                fanart = addonFanart
        except:
            return

        total = len(sourceList)
        for i in sourceList:
            try:
                url, source, provider = i['url'], i['source'], i['provider']
                sysname, sysurl, sysimdb, syssource, sysprovider = urllib.quote_plus(name), urllib.quote_plus(url), urllib.quote_plus(imdb), urllib.quote_plus(source), urllib.quote_plus(provider)

                u = '%s?action=play_host&name=%s&url=%s&imdb=%s&source=%s&provider=%s&t=%s' % (sys.argv[0], sysname, sysurl, sysimdb, syssource, sysprovider, datetime.datetime.now().strftime("%Y%m%d%H%M%S%f"))

                cm = []
                cm.append((language(30405).encode("utf-8"), 'RunPlugin(%s?action=item_queue)' % (sys.argv[0])))
                cm.append((language(30406).encode("utf-8"), 'RunPlugin(%s?action=download&name=%s&url=%s&provider=%s)' % (sys.argv[0], sysname, sysurl, sysprovider)))
                cm.append((language(30412).encode("utf-8"), 'Action(Info)'))
                cm.append((language(30416).encode("utf-8"), 'RunPlugin(%s?action=trailer&name=%s&url=%s)' % (sys.argv[0], sysname, trailer)))
                cm.append((language(30409).encode("utf-8"), 'RunPlugin(%s?action=settings_open)' % (sys.argv[0])))
                cm.append((language(30410).encode("utf-8"), 'RunPlugin(%s?action=playlist_open)' % (sys.argv[0])))

                item = xbmcgui.ListItem(source, iconImage="DefaultVideo.png", thumbnailImage=poster)
                item.setInfo( type="Video", infoLabels = meta )
                item.setProperty("IsPlayable", "true")
                item.setProperty("Video", "true")
                item.setProperty("art(poster)", poster)
                item.setProperty("Fanart_Image", fanart)
                item.addContextMenuItems(cm, replaceItems=True)
                xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=item,totalItems=total,isFolder=False)
            except:
                pass

class contextMenu:
    def item_play(self):
        playlist = xbmc.PlayList(xbmc.PLAYLIST_VIDEO)
        playlist.clear()
        xbmc.executebuiltin('Action(Queue)')
        playlist.unshuffle()
        xbmc.Player().play(playlist)

    def item_random_play(self):
        playlist = xbmc.PlayList(xbmc.PLAYLIST_VIDEO)
        playlist.clear()
        xbmc.executebuiltin('Action(Queue)')
        playlist.shuffle()
        xbmc.Player().play(playlist)

    def item_queue(self):
        xbmc.executebuiltin('Action(Queue)')

    def playlist_open(self):
        xbmc.executebuiltin('ActivateWindow(VideoPlaylist)')

    def settings_open(self):
        xbmc.executebuiltin('Addon.OpenSettings(%s)' % (addonId))

    def addon_home(self):
        xbmc.executebuiltin('Container.Update(plugin://%s/,replace)' % (addonId))

    def view(self, content):
        try:
            skin = xbmc.getSkinDir()
            skinPath = xbmc.translatePath('special://skin/')
            xml = os.path.join(skinPath,'addon.xml')
            file = xbmcvfs.File(xml)
            read = file.read().replace('\n','')
            file.close()
            try: src = re.compile('defaultresolution="(.+?)"').findall(read)[0]
            except: src = re.compile('<res.+?folder="(.+?)"').findall(read)[0]
            src = os.path.join(skinPath, src)
            src = os.path.join(src, 'MyVideoNav.xml')
            file = xbmcvfs.File(src)
            read = file.read().replace('\n','')
            file.close()
            views = re.compile('<views>(.+?)</views>').findall(read)[0]
            views = [int(x) for x in views.split(',')]
            for view in views:
                label = xbmc.getInfoLabel('Control.GetLabel(%s)' % (view))
                if not (label == '' or label is None): break
            file = xbmcvfs.File(viewData)
            read = file.read()
            file.close()
            write = [i.strip('\n').strip('\r') for i in read.splitlines(True) if i.strip('\r\n')]
            write = [i for i in write if not '"%s"|"%s"|"' % (skin, content) in i]
            write.append('"%s"|"%s"|"%s"' % (skin, content, str(view)))
            write = '\r\n'.join(write)
            file = xbmcvfs.File(viewData, 'w')
            file.write(str(write))
            file.close()
            viewName = xbmc.getInfoLabel('Container.Viewmode')
            index().infoDialog('%s%s%s' % (language(30301).encode("utf-8"), viewName, language(30302).encode("utf-8")))
        except:
            return

    def favourite_add(self, data, name, url, image, imdb, year):
        try:
            index().container_refresh()
            file = xbmcvfs.File(data)
            read = file.read()
            file.close()
            write = [i.strip('\n').strip('\r') for i in read.splitlines(True) if i.strip('\r\n')]
            write.append('"%s"|"%s"|"%s"|"%s"|"%s"' % (name, year, imdb, url, image))
            write = '\r\n'.join(write)
            file = xbmcvfs.File(data, 'w')
            file.write(str(write))
            file.close()
            index().infoDialog(language(30303).encode("utf-8"), name)
        except:
            return

    def favourite_from_search(self, data, name, url, image, imdb, year):
        try:
            file = xbmcvfs.File(data)
            read = file.read()
            file.close()
            if '"%s"' % url in read:
                index().infoDialog(language(30307).encode("utf-8"), name)
                return
            write = [i.strip('\n').strip('\r') for i in read.splitlines(True) if i.strip('\r\n')]
            write.append('"%s"|"%s"|"%s"|"%s"|"%s"' % (name, year, imdb, url, image))
            write = '\r\n'.join(write)
            file = xbmcvfs.File(data, 'w')
            file.write(str(write))
            file.close()
            index().infoDialog(language(30303).encode("utf-8"), name)
        except:
            return

    def favourite_delete(self, data, name, url):
        try:
            index().container_refresh()
            file = xbmcvfs.File(data)
            read = file.read()
            file.close()
            write = [i.strip('\n').strip('\r') for i in read.splitlines(True) if i.strip('\r\n')]
            write = [i for i in write if not '"%s"' % url in i]
            write = '\r\n'.join(write)
            file = xbmcvfs.File(data, 'w')
            file.write(str(write))
            file.close()
            index().infoDialog(language(30304).encode("utf-8"), name)
        except:
            return

    def favourite_moveUp(self, data, name, url):
        try:
            index().container_refresh()
            file = xbmcvfs.File(data)
            read = file.read()
            file.close()
            write = [i.strip('\n').strip('\r') for i in read.splitlines(True) if i.strip('\r\n')]
            i = write.index([i for i in write if '"%s"' % url in i][0])
            if i == 0 : return
            write[i], write[i-1] = write[i-1], write[i]
            write = '\r\n'.join(write)
            file = xbmcvfs.File(data, 'w')
            file.write(str(write))
            file.close()
            index().infoDialog(language(30305).encode("utf-8"), name)
        except:
            return

    def favourite_moveDown(self, data, name, url):
        try:
            index().container_refresh()
            file = xbmcvfs.File(data)
            read = file.read()
            file.close()
            write = [i.strip('\n').strip('\r') for i in read.splitlines(True) if i.strip('\r\n')]
            i = write.index([i for i in write if '"%s"' % url in i][0])
            if i+1 == len(write): return
            write[i], write[i+1] = write[i+1], write[i]
            write = '\r\n'.join(write)
            file = xbmcvfs.File(data, 'w')
            file.write(str(write))
            file.close()
            index().infoDialog(language(30306).encode("utf-8"), name)
        except:
            return

    def metadata(self, content, imdb, season, episode):
        try:
            if content == 'movie' or content == 'tvshow':
                metaget.update_meta(content, '', imdb, year='')
                index().container_refresh()
            elif content == 'season':
                metaget.update_episode_meta('', imdb, season, episode)
                index().container_refresh()
            elif content == 'episode':
                metaget.update_season('', imdb, season)
                index().container_refresh()
        except:
            return

    def playcount(self, content, imdb, season, episode):
        try:
            metaget.change_watched(content, '', imdb, season=season, episode=episode, year='', watched='')
            index().container_refresh()
        except:
            return

    def library_add(self, name, title, imdb, year, url, update=True, silent=False):
        try:
            lib = self.library(name, title, imdb, year, url, check=True)
            if (silent == False and lib == False):
                yes = index().yesnoDialog(language(30347).encode("utf-8"), language(30349).encode("utf-8"), name)
                if yes:
                    self.library(name, title, imdb, year, url)
                else:
                    return
            elif lib == False:
                return

            if silent == False:
                index().container_refresh()
                index().infoDialog(language(30311).encode("utf-8"), name)
            if update == True:
                xbmc.executebuiltin('UpdateLibrary(video)')
        except:
            return

    def library_update(self, silent=False):
        if getSetting("trakt_import") == '1' and not (link().trakt_user == '' or link().trakt_password == ''):
            url = link().trakt_collection % (link().trakt_key, link().trakt_user)
            self.library_batch(url, silent=silent)
        elif getSetting("trakt_import") == '2' and not (link().trakt_user == '' or link().trakt_password == ''):
            url = link().trakt_watchlist % (link().trakt_key, link().trakt_user)
            self.library_batch(url, silent=silent)

    def library_batch(self, url, update=True, silent=False):
        if url == 'movies_added':
            movieList = movies().added(idx=False)
        elif url == 'movies_trending':
            movieList = movies().trending(idx=False)
        else:
            movieList = movies().get(url, idx=False)

        if movieList == None: return
        for i in movieList:
            try: self.library(i['name'], i['title'], i['imdb'], i['year'], i['url'], check=True)
            except: pass
        if silent == False:
            index().infoDialog(language(30311).encode("utf-8"))
        if update == True and getSetting("updatelibrary") == 'true':
            xbmc.executebuiltin('UpdateLibrary(video)')

    def library(self, name, title, imdb, year, url, check=False):
        try:
            library = xbmc.translatePath(getSetting("movie_library"))
            sysname, systitle, sysimdb, sysyear = urllib.quote_plus(name), urllib.quote_plus(title), urllib.quote_plus(imdb), urllib.quote_plus(year)
            content = '%s?action=play&name=%s&title=%s&imdb=%s&year=%s' % (sys.argv[0], sysname, systitle, sysimdb, sysyear)
            enc_name = name.translate(None, '\/:*?"<>|')
            folder = os.path.join(library, enc_name)
            stream = os.path.join(folder, enc_name + '.strm')
        except:
            return

        try:
            if check == False: raise Exception()
            data = xbmc.executeJSONRPC('{"jsonrpc": "2.0", "method": "VideoLibrary.GetMovies", "params": {"filter":{"or": [{"field": "year", "operator": "is", "value": "%s"}, {"field": "year", "operator": "is", "value": "%s"}, {"field": "year", "operator": "is", "value": "%s"}]}, "properties" : ["imdbnumber", "file"]}, "id": 1}' % (year, str(int(year)+1), str(int(year)-1)))
            data = unicode(data, 'utf-8', errors='ignore')
            data = json.loads(data)
            data = data['result']['movies']
            data = [i for i in data if imdb in i['imdbnumber']][0]
            if data['file'] == stream: raise Exception()
            return False
        except:
            pass

        try:
            xbmcvfs.mkdir(dataPath)
            xbmcvfs.mkdir(library)
            xbmcvfs.mkdir(folder)
            file = xbmcvfs.File(stream, 'w')
            file.write(str(content))
            file.close()
        except:
            return

    def download(self, name, url, provider):
        try:
            property = (addonName+name)+'download'
            download = xbmc.translatePath(getSetting("downloads"))
            enc_name = name.translate(None, '\/:*?"<>|')
            xbmcvfs.mkdir(dataPath)
            xbmcvfs.mkdir(download)

            file = [i for i in xbmcvfs.listdir(download)[1] if i.startswith(enc_name + '.')]
            if not file == []: file = os.path.join(download, file[0])
            else: file = None

            if download == '':
            	yes = index().yesnoDialog(language(30341).encode("utf-8"), language(30342).encode("utf-8"))
            	if yes: contextMenu().settings_open()
            	return

            if file is None:
            	pass
            elif not file.endswith('.tmp'):
            	yes = index().yesnoDialog(language(30343).encode("utf-8"), language(30344).encode("utf-8"), name)
            	if yes:
            	    xbmcvfs.delete(file)
            	else:
            	    return
            elif file.endswith('.tmp'):
            	if index().getProperty(property) == 'open':
            	    yes = index().yesnoDialog(language(30345).encode("utf-8"), language(30346).encode("utf-8"), name)
            	    if yes: index().setProperty(property, 'cancel')
            	    return
            	else:
            	    xbmcvfs.delete(file)

            url = resolver().sources_resolve(url, provider)
            if url is None: return
            url = url.rsplit('|', 1)[0]
            ext = url.rsplit('/', 1)[-1].rsplit('?', 1)[0].rsplit('|', 1)[0].strip().lower()
            ext = os.path.splitext(ext)[1][1:]
            if ext == '' or ext == 'php': ext = 'mp4'
            stream = os.path.join(download, enc_name + '.' + ext)
            temp = stream + '.tmp'

            count = 0
            CHUNK = 16 * 1024
            request = urllib2.Request(url)
            request.add_header('User-Agent', 'Mozilla/5.0 (iPhone; CPU; CPU iPhone OS 4_0 like Mac OS X; en-us) AppleWebKit/532.9 (KHTML, like Gecko) Version/4.0.5 Mobile/8A293 Safari/6531.22.7')
            request.add_header('Cookie', 'video=true')
            response = urllib2.urlopen(request, timeout=10)
            size = response.info()["Content-Length"]

            file = xbmcvfs.File(temp, 'w')
            index().setProperty(property, 'open')
            index().infoDialog(language(30308).encode("utf-8"), name)
            while True:
            	chunk = response.read(CHUNK)
            	if not chunk: break
            	if index().getProperty(property) == 'cancel': raise Exception()
            	if xbmc.abortRequested == True: raise Exception()
            	part = xbmcvfs.File(temp)
            	quota = int(100 * float(part.size())/float(size))
            	part.close()
            	if not count == quota and count in [0,10,20,30,40,50,60,70,80,90]:
            		index().infoDialog(language(30309).encode("utf-8") + str(count) + '%', name)
            	file.write(chunk)
            	count = quota
            response.close()
            file.close()

            index().clearProperty(property)
            xbmcvfs.rename(temp, stream)
            index().infoDialog(language(30310).encode("utf-8"), name)
        except:
            file.close()
            index().clearProperty(property)
            xbmcvfs.delete(temp)
            sys.exit()
            return

    def autoplay(self, name, title, imdb, year, url):
        meta = {'title': xbmc.getInfoLabel('ListItem.title'), 'originaltitle': xbmc.getInfoLabel('ListItem.originaltitle'), 'year': xbmc.getInfoLabel('ListItem.year'), 'genre': xbmc.getInfoLabel('ListItem.genre'), 'director': xbmc.getInfoLabel('ListItem.director'), 'country': xbmc.getInfoLabel('ListItem.country'), 'rating': xbmc.getInfoLabel('ListItem.rating'), 'votes': xbmc.getInfoLabel('ListItem.votes'), 'mpaa': xbmc.getInfoLabel('ListItem.mpaa'), 'duration': xbmc.getInfoLabel('ListItem.duration'), 'trailer': xbmc.getInfoLabel('ListItem.trailer'), 'writer': xbmc.getInfoLabel('ListItem.writer'), 'studio': xbmc.getInfoLabel('ListItem.studio'), 'tagline': xbmc.getInfoLabel('ListItem.tagline'), 'plotoutline': xbmc.getInfoLabel('ListItem.plotoutline'), 'plot': xbmc.getInfoLabel('ListItem.plot')}
        label, poster, fanart = xbmc.getInfoLabel('ListItem.label'), xbmc.getInfoLabel('ListItem.icon'), xbmc.getInfoLabel('ListItem.Property(Fanart_Image)')

        sysname, systitle, sysimdb, sysyear = urllib.quote_plus(name), urllib.quote_plus(title), urllib.quote_plus(imdb), urllib.quote_plus(year)
        u = '%s?action=play&name=%s&title=%s&imdb=%s&year=%s&url=play://' % (sys.argv[0], sysname, systitle, sysimdb, sysyear)

        playlist = xbmc.PlayList(xbmc.PLAYLIST_VIDEO)
        playlist.clear()
        item = xbmcgui.ListItem(label, iconImage="DefaultVideo.png", thumbnailImage=poster)
        item.setInfo( type="Video", infoLabels= meta )
        item.setProperty("IsPlayable", "true")
        item.setProperty("Video", "true")
        item.setProperty("Fanart_Image", fanart)
        xbmc.Player().play(u, item)

    def trailer(self, name, url):
        url = trailer().run(name, url)
        if url is None: return
        item = xbmcgui.ListItem(path=url)
        item.setProperty("IsPlayable", "true")
        xbmc.Player().play(url, item)

class favourites:
    def __init__(self):
        self.list = []

    def movies(self):
        file = xbmcvfs.File(favData)
        read = file.read()
        file.close()

        match = re.compile('"(.+?)"[|]"(.+?)"[|]"(.+?)"[|]"(.+?)"[|]"(.+?)"').findall(read)
        for title, year, imdb, url, image in match:
            name = '%s (%s)' % (title, year)
            self.list.append({'name': name, 'url': url, 'image': image, 'title': title, 'year': year, 'imdb': imdb, 'genre': '', 'plot': ''})

        if getSetting("fav_sort") == '0':
            self.list = sorted(self.list, key=itemgetter('title'))
        elif getSetting("fav_sort") == '1':
            self.list = sorted(self.list, key=itemgetter('title'))[::-1]
            self.list = sorted(self.list, key=itemgetter('year'))[::-1]

        index().movieList(self.list)

class root:
    def get(self):
        rootList = []
        rootList.append({'name': 30501, 'image': 'BOXoffice.png', 'action': 'movies_boxoffice'})
        rootList.append({'name': 30502, 'image': 'Views.png', 'action': 'movies_views'})
        rootList.append({'name': 30503, 'image': 'Popular.png', 'action': 'movies_popular'})
        rootList.append({'name': 30504, 'image': 'Oscars.png', 'action': 'movies_oscars'})
        rootList.append({'name': 30505, 'image': 'Added.png', 'action': 'movies_added'})
        rootList.append({'name': 30506, 'image': 'Trending.png', 'action': 'movies_trending'})
        rootList.append({'name': 30507, 'image': 'Channels.png', 'action': 'channels_movies'})
        rootList.append({'name': 30508, 'image': 'Genres.png', 'action': 'genres_movies'})
        rootList.append({'name': 30509, 'image': 'Years.png', 'action': 'years_movies'})
        if not (getSetting("trakt_user") == '' or getSetting("trakt_password") == ''):
            rootList.append({'name': 30511, 'image': 'Trakt.png', 'action': 'userlists_trakt'})
        if not (getSetting("imdb_user") == ''):
            rootList.append({'name': 30510, 'image': 'IMDb.png', 'action': 'userlists_imdb'})
        rootList.append({'name': 30512, 'image': 'Favourites.png', 'action': 'movies_favourites'})
        rootList.append({'name': 30513, 'image': 'Search.png', 'action': 'root_search'})
        index().rootList(rootList)
        index().downloadList()

    def search(self):
        rootList = []
        rootList.append({'name': 30521, 'image': 'Movies.png', 'action': 'movies_search'})
        rootList.append({'name': 30522, 'image': 'Actors.png', 'action': 'actors_search'})
        index().rootList(rootList)


class link:
    def __init__(self):
        self.imdb_base = 'http://www.imdb.com'
        self.imdb_akas = 'http://akas.imdb.com'
        self.imdb_mobile = 'http://m.imdb.com'
        self.imdb_genre = 'http://akas.imdb.com/genre/'
        self.imdb_title = 'http://www.imdb.com/title/tt%s/'
        self.imdb_image = 'http://i.media-imdb.com/images/SFaa265aa19162c9e4f3781fbae59f856d/nopicture/medium/film.png'
        self.imdb_genres = 'http://akas.imdb.com/search/title?title_type=feature,tv_movie&sort=boxoffice_gross_us&count=25&start=1&genres=%s'
        self.imdb_years = 'http://akas.imdb.com/search/title?title_type=feature,tv_movie&sort=boxoffice_gross_us&count=25&start=1&&year=%s,%s'
        self.imdb_popular = 'http://akas.imdb.com/search/title?title_type=feature,tv_movie&sort=moviemeter,asc&count=25&start=1'
        self.imdb_boxoffice = 'http://akas.imdb.com/search/title?title_type=feature,tv_movie&sort=boxoffice_gross_us,desc&count=25&start=1'
        self.imdb_views = 'http://akas.imdb.com/search/title?title_type=feature,tv_movie&sort=num_votes,desc&count=25&start=1'
        self.imdb_oscars = 'http://akas.imdb.com/search/title?title_type=feature,tv_movie&groups=oscar_best_picture_winners&sort=year,desc&count=25&start=1'
        self.imdb_search = 'http://akas.imdb.com/search/title?title_type=feature,tv_movie&sort=moviemeter,asc&count=25&start=1&title=%s'
        self.imdb_actors_search = 'http://www.imdb.com/search/name?count=100&name=%s'
        self.imdb_actors = 'http://m.imdb.com/name/nm%s/filmotype/%s'

        self.imdb_userlists = 'http://akas.imdb.com/user/%s/lists?tab=all&sort=modified:desc&filter=titles'
        self.imdb_watchlist ='http://akas.imdb.com/user/%s/watchlist?sort=moviemeter,asc&mode=detail&page=1'
        self.imdb_watchadded ='http://akas.imdb.com/user/%s/watchlist?sort=date_added,desc&mode=detail&page=1'
        self.imdb_watchtitle ='http://akas.imdb.com/user/%s/watchlist?sort=alpha,asc&mode=detail&page=1'
        self.imdb_list ='http://akas.imdb.com/list/%s/?view=detail&count=100&sort=listorian:asc&start=1'
        self.imdb_user = 'ur' + getSetting("imdb_user").replace('ur', '')

        self.trakt_base = 'http://api.trakt.tv'
        self.trakt_key = base64.urlsafe_b64decode('YmU2NDI5MWFhZmJiYmU2MmZkYzRmM2FhMGVkYjQwNzM=')
        self.trakt_summary = 'http://api.trakt.tv/show/summary.json/%s/%s'
        self.trakt_trending = 'http://api.trakt.tv/movies/trending.json/%s'
        self.trakt_user, self.trakt_password = getSetting("trakt_user"), getSetting("trakt_password")
        self.trakt_watchlist = 'http://api.trakt.tv/user/watchlist/movies.json/%s/%s'
        self.trakt_collection = 'http://api.trakt.tv/user/library/movies/collection.json/%s/%s'
        self.trakt_watched = 'http://api.trakt.tv/user/library/movies/watched.json/%s/%s'
        self.trakt_rated = 'http://api.trakt.tv/user/ratings/movies.json/%s/%s/rating/extended'
        self.trakt_lists = 'http://api.trakt.tv/user/lists.json/%s/%s'
        self.trakt_list= 'http://api.trakt.tv/user/list.json/%s/%s'

class actors:
    def __init__(self):
        self.list = []

    def search(self, query=None):
        if query is None:
            self.query = common.getUserInput(language(30362).encode("utf-8"), '')
        else:
            self.query = query
        if not (self.query is None or self.query == ''):
            self.query = link().imdb_actors_search % urllib.quote_plus(self.query)
            self.list = self.imdb_list(self.query)
            index().pageList(self.list)

    def imdb_list(self, url):
        try:
            result = getUrl(url).result
            result = result.decode('iso-8859-1').encode('utf-8')
            actors = common.parseDOM(result, "tr", attrs = { "class": ".+? detailed" })
        except:
            return
        for actor in actors:
            try:
                name = common.parseDOM(actor, "a", ret="title")[0]
                name = common.replaceHTMLCodes(name)
                name = name.encode('utf-8')

                url = common.parseDOM(actor, "a", ret="href")[0]
                url = re.findall('nm(\d*)', url, re.I)[0]
                type = common.parseDOM(actor, "span", attrs = { "class": "description" })[0]
                if 'Actress' in type: type = 'actress'
                elif 'Actor' in type: type = 'actor'
                else: raise Exception()
                url = link().imdb_actors % (url, type)
                url = common.replaceHTMLCodes(url)
                url = url.encode('utf-8')

                image = common.parseDOM(actor, "img", ret="src")[0]
                if not ('._SX' in image or '._SY' in image): raise Exception()
                image = image.rsplit('._SX', 1)[0].rsplit('._SY', 1)[0] + '._SX500.' + image.rsplit('.', 1)[-1]
                image = common.replaceHTMLCodes(image)
                image = image.encode('utf-8')

                self.list.append({'name': name, 'url': url, 'image': image})
            except:
                pass

        return self.list

class genres:
    def __init__(self):
        self.list = []

    def get(self):
        #self.list = self.imdb_list()
        self.list = cache3(self.imdb_list)
        index().pageList(self.list)

    def imdb_list(self):
        try:
            result = getUrl(link().imdb_genre).result
            result = common.parseDOM(result, "table", attrs = { "class": "genre-table" })[0]
            genres = common.parseDOM(result, "h3")
        except:
            return
        for genre in genres:
            try:
                name = common.parseDOM(genre, "a")[0]
                name = name.split('<', 1)[0].rsplit('>', 1)[0].strip()
                name = common.replaceHTMLCodes(name)
                name = name.encode('utf-8')

                url = common.parseDOM(genre, "a", ret="href")[0]
                url = re.compile('/genre/(.+?)/').findall(url)[0]
                url = link().imdb_genres % url
                url = common.replaceHTMLCodes(url)
                url = url.encode('utf-8')

                image = addonGenres.encode('utf-8')

                self.list.append({'name': name, 'url': url, 'image': image})
            except:
                pass

        return self.list

class years:
    def __init__(self):
        self.list = []

    def get(self):
        self.list = self.imdb_list()
        index().pageList(self.list)

    def imdb_list(self):
        year = (datetime.datetime.utcnow() - datetime.timedelta(hours = 5)).strftime("%Y")

        for i in range(int(year)-0, int(year)-50, -1):
            name = str(i).encode('utf-8')
            url = link().imdb_years % (str(i), str(i))
            url = url.encode('utf-8')
            image = addonYears.encode('utf-8')
            self.list.append({'name': name, 'url': url, 'image': image})

        return self.list

class userlists:
    def __init__(self):
        self.list = []

    def trakt(self):
        post = urllib.urlencode({'username': link().trakt_user, 'password': link().trakt_password})
        info = (link().trakt_key, link().trakt_user)
        image = addonLists.encode('utf-8')

        self.list.append({'name': language(30531).encode("utf-8"), 'url': link().trakt_watchlist % info, 'image': image})
        self.list.append({'name': language(30532).encode("utf-8"), 'url': link().trakt_collection % info, 'image': image})
        self.list.append({'name': language(30533).encode("utf-8"), 'url': link().trakt_watched % info, 'image': image})
        self.list.append({'name': language(30534).encode("utf-8"), 'url': link().trakt_rated % info, 'image': image})

        try:
            userlists = []
            result = getUrl(link().trakt_lists % info, post=post).result
            userlists = json.loads(result)
        except:
            pass

        for userlist in userlists:
            try:
                name = userlist['name']
                name = common.replaceHTMLCodes(name)
                name = name.encode('utf-8')

                url = userlist['slug']
                url = '%s/%s' % (link().trakt_list % info, url)
                url = common.replaceHTMLCodes(url)
                url = url.encode('utf-8')

                self.list.append({'name': name, 'url': url, 'image': image})
            except:
                pass

        index().userList(self.list)

    def imdb(self):
        image = addonLists.encode('utf-8')

        self.list.append({'name': language(30541).encode("utf-8"), 'url': 'watchlist', 'image': image})
        self.list.append({'name': language(30542).encode("utf-8"), 'url': 'watchadded', 'image': image})
        self.list.append({'name': language(30543).encode("utf-8"), 'url': 'watchtitle', 'image': image})

        try:
            userlists = []
            result = getUrl(link().imdb_userlists % link().imdb_user).result
            result = result.decode('iso-8859-1').encode('utf-8')
            userlists = common.parseDOM(result, "div", attrs = { "class": "list_name" })
        except:
            pass

        for userlist in userlists:
            try:
                name = common.parseDOM(userlist, "a")[0]
                name = common.replaceHTMLCodes(name)
                name = name.encode('utf-8')

                url = common.parseDOM(userlist, "a", ret="href")[0]
                url = url.split('/list/', 1)[-1].replace('/', '')
                url = common.replaceHTMLCodes(url)
                url = url.encode('utf-8')

                self.list.append({'name': name, 'url': url, 'image': image})
            except:
                pass

        index().userList(self.list)

class channels:
    def __init__(self):
        self.list = []
        self.sky_now_link = 'http://epgservices.sky.com/5.1.1/api/2.0/channel/json/%s/now/nn/0'
        self.sky_programme_link = 'http://tv.sky.com/programme/channel/%s/%s/%s.json'

    def get(self):
        threads = []

        threads.append(Thread(self.sky_list, '01', 'Sky Premiere', '1409'))
        threads.append(Thread(self.sky_list, '02', 'Sky Premiere +1', '1823'))
        threads.append(Thread(self.sky_list, '03', 'Sky Showcase', '1814'))
        threads.append(Thread(self.sky_list, '04', 'Sky Greats', '1815'))
        threads.append(Thread(self.sky_list, '05', 'Sky Disney', '1838'))
        threads.append(Thread(self.sky_list, '06', 'Sky Family', '1808'))
        threads.append(Thread(self.sky_list, '07', 'Sky Action', '1001'))
        threads.append(Thread(self.sky_list, '08', 'Sky Comedy', '1002'))
        threads.append(Thread(self.sky_list, '09', 'Sky Crime', '1818'))
        threads.append(Thread(self.sky_list, '10', 'Sky Sci Fi', '1807'))
        threads.append(Thread(self.sky_list, '11', 'Sky Select', '1811'))

        [i.start() for i in threads]
        [i.join() for i in threads]

        self.list = sorted(self.list, key=itemgetter('num'))
        index().channelList(self.list)

    def sky_list(self, num, channel, id):
        try:
            url = self.sky_now_link % id
            result = getUrl(url).result
            result = json.loads(result)
            match = result['listings'][id][0]['url']

            dt = self.uk_datetime()
            dt1 = '%04d' % dt.year + '-' + '%02d' % dt.month + '-' + '%02d' % dt.day
            dt2 = int(dt.hour)
            if (dt2 < 6): dt2 = 0
            elif (dt2 >= 6 and dt2 < 12): dt2 = 1
            elif (dt2 >= 12 and dt2 < 18): dt2 = 2
            elif (dt2 >= 18): dt2 = 3
            url = self.sky_programme_link % (id, str(dt1), str(dt2))

            result = getUrl(url).result
            result = json.loads(result)
            result = result['listings'][id]
            result = [i for i in result if i['url'] == match][0]

            y = result['d']
            y = re.findall('.+?[(](\d{4})[)]', y)[0].strip()

            t = result['t']
            t = t.replace('(%s)' % y, '').strip()

            imdb_api = self.imdb_api(t, y)
            if imdb_api == None: imdb_api = self.imdb_api(t, str(int(y)+1))
            if imdb_api == None: imdb_api = self.imdb_api(t, str(int(y)-1))
            if imdb_api == None: raise Exception()

            title, year, imdb, plot = imdb_api

            title = common.replaceHTMLCodes(title)
            title = title.encode('utf-8')

            year = year.encode('utf-8')

            imdb = re.sub('[^0-9]', '', str(imdb))
            imdb = imdb.encode('utf-8')

            plot = common.replaceHTMLCodes(plot)
            plot = plot.encode('utf-8')

            self.list.append({'name': channel, 'title': title, 'year': year, 'imdb': imdb, 'genre': '', 'plot': plot, 'num': num})
        except:
            return

    def imdb_api(self, t, y=''):
        try:
            search = 'http://www.imdbapi.com/?t=%s' % urllib.quote_plus(t)
            if not y == '': search += '&y=%s' % y
            search = getUrl(search).result
            search = json.loads(search)

            title, year, imdb, plot = search['Title'], search['Year'], search['imdbID'], search['Plot']
            return (title, year, imdb, plot)
        except:
            return

    def uk_datetime(self):
        dt = datetime.datetime.utcnow() + datetime.timedelta(hours = 0)
        d = datetime.datetime(dt.year, 4, 1)
        dston = d - datetime.timedelta(days=d.weekday() + 1)
        d = datetime.datetime(dt.year, 11, 1)
        dstoff = d - datetime.timedelta(days=d.weekday() + 1)
        if dston <=  dt < dstoff:
            return dt + datetime.timedelta(hours = 1)
        else:
            return dt

class movies:
    def __init__(self):
        self.list = []
        self.data = []

    def get(self, url, idx=True):
        if url.startswith(link().imdb_base) or url.startswith(link().imdb_akas):
            #self.list = self.imdb_list(url)
            self.list = cache(self.imdb_list, url)
        elif url.startswith(link().imdb_mobile):
            #self.list = self.imdb_list2(url)
            self.list = cache(self.imdb_list2, url)
        elif url.startswith(link().trakt_base):
            self.list = self.trakt_list(url)
        elif url == 'watchlist':
            self.list = self.imdb_list3(link().imdb_watchlist % link().imdb_user)
        elif url == 'watchadded':
            self.list = self.imdb_list3(link().imdb_watchadded % link().imdb_user)
        elif url == 'watchtitle':
            self.list = self.imdb_list3(link().imdb_watchtitle % link().imdb_user)
        else:
            self.list = self.imdb_list4(link().imdb_list % url)
            self.list = sorted(self.list, key=itemgetter('name'))

        if idx == False: return self.list
        index().movieList(self.list)
        index().nextList(self.list)

    def popular(self):
        #self.list = self.imdb_list(link().imdb_popular)
        self.list = cache(self.imdb_list, link().imdb_popular)
        index().movieList(self.list)
        index().nextList(self.list)

    def boxoffice(self):
        #self.list = self.imdb_list(link().imdb_boxoffice)
        self.list = cache(self.imdb_list, link().imdb_boxoffice)
        index().movieList(self.list)
        index().nextList(self.list)

    def views(self):
        #self.list = self.imdb_list(link().imdb_views)
        self.list = cache(self.imdb_list, link().imdb_views)
        index().movieList(self.list)
        index().nextList(self.list)

    def oscars(self):
        #self.list = self.imdb_list(link().imdb_oscars)
        self.list = cache(self.imdb_list, link().imdb_oscars)
        index().movieList(self.list)
        index().nextList(self.list)

    def added(self, idx=True):
        #self.list = self.ice_list()
        self.list = cache2(self.ice_list)
        if idx == False: return self.list[:100]
        index().movieList(self.list[:100])

    def trending(self, idx=True):
        #self.list = self.trakt_list(link().trakt_trending % link().trakt_key)
        self.list = cache2(self.trakt_list, link().trakt_trending % link().trakt_key)
        if idx == False: return self.list[:100]
        index().movieList(self.list[:100])

    def search(self, query=None):
        if query is None:
            self.query = common.getUserInput(language(30362).encode("utf-8"), '')
        else:
            self.query = query
        if not (self.query is None or self.query == ''):
            self.query = link().imdb_search % urllib.quote_plus(self.query)
            self.list = self.imdb_list(self.query)
            index().movieList(self.list)

    def imdb_list(self, url):
        try:
            result = getUrl(url.replace(link().imdb_base, link().imdb_akas)).result
            result = result.decode('iso-8859-1').encode('utf-8')
            movies = common.parseDOM(result, "tr", attrs = { "class": ".+?" })
        except:
            return

        try:
            next = common.parseDOM(result, "span", attrs = { "class": "pagination" })[0]
            name = common.parseDOM(next, "a")[-1]
            if 'laquo' in name: raise Exception()
            next = common.parseDOM(next, "a", ret="href")[-1]
            next = '%s%s' % (link().imdb_akas, next)
            next = common.replaceHTMLCodes(next)
            next = next.encode('utf-8')
        except:
            next = ''

        for movie in movies:
            try:
                title = common.parseDOM(movie, "a")[1]
                title = common.replaceHTMLCodes(title)
                title = title.encode('utf-8')

                year = common.parseDOM(movie, "span", attrs = { "class": "year_type" })[0]
                year = re.sub('[^0-9]', '', year)[:4]
                year = year.encode('utf-8')

                if int(year) > int((datetime.datetime.utcnow() - datetime.timedelta(hours = 5)).strftime("%Y")): raise Exception()

                name = '%s (%s)' % (title, year)
                try: name = name.encode('utf-8')
                except: pass

                url = common.parseDOM(movie, "a", ret="href")[0]
                url = '%s%s' % (link().imdb_base, url)
                url = common.replaceHTMLCodes(url)
                url = url.encode('utf-8')

                try:
                    image = common.parseDOM(movie, "img", ret="src")[0]
                    if not ('._SX' in image or '._SY' in image): raise Exception()
                    image = image.rsplit('._SX', 1)[0].rsplit('._SY', 1)[0] + '._SX500.' + image.rsplit('.', 1)[-1]
                except:
                    image = link().imdb_image
                image = common.replaceHTMLCodes(image)
                image = image.encode('utf-8')

                imdb = re.sub('[^0-9]', '', url.rsplit('tt', 1)[-1])
                imdb = imdb.encode('utf-8')

                try:
                    genre = common.parseDOM(movie, "span", attrs = { "class": "genre" })
                    genre = common.parseDOM(genre, "a")
                    genre = " / ".join(genre)
                    genre = common.replaceHTMLCodes(genre)
                    genre = genre.encode('utf-8')
                except:
                    genre = ''

                try:
                    plot = common.parseDOM(movie, "span", attrs = { "class": "outline" })[0]
                    plot = common.replaceHTMLCodes(plot)
                    plot = plot.encode('utf-8')
                except:
                    plot = ''

                self.list.append({'name': name, 'url': url, 'image': image, 'title': title, 'year': year, 'imdb': imdb, 'genre': genre, 'plot': plot, 'next': next})
            except:
                pass

        return self.list

    def imdb_list2(self, url):
        try:
            result = getUrl(url, mobile=True).result
            result = result.decode('iso-8859-1').encode('utf-8')
            movies = common.parseDOM(result, "div", attrs = { "class": "col-xs.+?" })
        except:
            return

        for movie in movies:
            try:
                title = common.parseDOM(movie, "span", attrs = { "class": "h3" })[0]
                title = common.replaceHTMLCodes(title)
                title = title.encode('utf-8')

                year = common.parseDOM(movie, "div", attrs = { "class": "unbold" })[0]
                year = re.sub("\n|[(]|[)]|\s", "", year)
                year = year.encode('utf-8')

                if not year.isdigit(): raise Exception()
                if int(year) > int((datetime.datetime.utcnow() - datetime.timedelta(hours = 5)).strftime("%Y")): raise Exception()

                name = '%s (%s)' % (title, year)
                try: name = name.encode('utf-8')
                except: pass

                url = common.parseDOM(movie, "a", ret="href")[0]
                url = re.findall('tt(\d*)', url, re.I)[0]
                url = link().imdb_title % url
                url = common.replaceHTMLCodes(url)
                url = url.encode('utf-8')

                try:
                    image = common.parseDOM(movie, "img", ret="src")[0]
                    if not ('_SX' in image or '_SY' in image): raise Exception()
                    image = image.rsplit('_SX', 1)[0].rsplit('_SY', 1)[0] + '_SX500.' + image.rsplit('.', 1)[-1]
                except:
                    image = link().imdb_image
                image = common.replaceHTMLCodes(image)
                image = image.encode('utf-8')

                imdb = re.sub('[^0-9]', '', url.rsplit('tt', 1)[-1])
                imdb = imdb.encode('utf-8')

                self.list.append({'name': name, 'url': url, 'image': image, 'title': title, 'year': year, 'imdb': imdb, 'genre': '', 'plot': ''})
            except:
                pass

        return self.list

    def imdb_list3(self, url):
        try:
            URL = url.replace(link().imdb_base, link().imdb_akas)
            url = 'http://9proxy.in/b.php?u=%s&b=28' % urllib.quote_plus(urllib.unquote_plus(url))
            result = getUrl(url, referer=url).result

            try:
                threads = []
                pages = common.parseDOM(result, "div", attrs = { "class": "desc" })
                pages = [re.compile('of (\d+) titles').findall(i)[0] for i in pages][0]
                pages = (int(pages)+100)/100
                for i in range(1, int(pages)):
                    self.data.append('')
                    moviesUrl = URL.replace('&page=1', '&page=%s' % str(i+1))
                    moviesUrl = 'http://9proxy.in/b.php?u=%s&b=28' % urllib.quote_plus(urllib.unquote_plus(moviesUrl))
                    threads.append(Thread(self.thread, moviesUrl, i-1))
                [i.start() for i in threads]
                [i.join() for i in threads]
                for i in self.data: result += i
            except:
                pass

            result = result.replace('\n','')
            movies = common.parseDOM(result, "div", attrs = { "class": "lister-item mode-detail" })
        except:
            return

        for movie in movies:
            try:
                title = common.parseDOM(movie, "h3", attrs = { "class": "lister-item-header" })[0]
                title = common.parseDOM(title, "a")[0]
                title = common.replaceHTMLCodes(title)
                title = title.encode('utf-8')

                year = common.parseDOM(movie, "span", attrs = { "class": "lister-item-year.+?" })[0]
                year = re.compile('[(](\d{4})[)]').findall(year)[-1]
                year = year.encode('utf-8')

                if int(year) > int((datetime.datetime.utcnow() - datetime.timedelta(hours = 5)).strftime("%Y")): raise Exception()

                name = '%s (%s)' % (title, year)
                try: name = name.encode('utf-8')
                except: pass

                imdb = common.parseDOM(movie, "img", ret="data-tconst")[0]
                imdb = re.sub('[^0-9]', '', str(imdb))
                imdb = imdb.encode('utf-8')

                url = link().imdb_title % imdb
                url = common.replaceHTMLCodes(url)
                url = url.encode('utf-8')

                try:
                    image = common.parseDOM(movie, "img", ret="src")[0]
                    image = urllib.unquote_plus(image)
                    image = image[image.find('?') + 1:].split('&')
                    image = [i.split('=', 1)[-1] for i in image if i.startswith('u=')][0]
                    image = 'http' + image.split('http' , 1)[-1]
                    if not ('_SX' in image or '_SY' in image): raise Exception()
                    image = image.rsplit('_SX', 1)[0].rsplit('_SY', 1)[0] + '_SX500.' + image.rsplit('.', 1)[-1]
                except:
                    image = link().imdb_image
                image = common.replaceHTMLCodes(image)
                image = image.encode('utf-8')

                try:
                    plot = common.parseDOM(movie, "p", attrs = { "class": "" })[0]
                    plot = plot.rsplit('<span>', 1)[0].rsplit('<a href', 1)[0].strip()
                    plot = common.replaceHTMLCodes(plot)
                    plot = plot.encode('utf-8')
                except:
                    plot = ''

                self.list.append({'name': name, 'url': url, 'image': image, 'title': title, 'year': year, 'imdb': imdb, 'genre': '', 'plot': plot})
            except:
                pass

        return self.list

    def imdb_list4(self, url):
        try:
            url = url.replace(link().imdb_base, link().imdb_akas)
            result = getUrl(url).result

            try:
                threads = []
                pages = common.parseDOM(result, "div", attrs = { "class": "pagination" })[0]
                pages = re.compile('.+?\d+.+?(\d+)').findall(pages)[0]

                for i in range(1, int(pages)):
                    self.data.append('')
                    moviesUrl = url.replace('&start=1', '&start=%s' % str(i*100+1))
                    threads.append(Thread(self.thread, moviesUrl, i-1))
                [i.start() for i in threads]
                [i.join() for i in threads]
                for i in self.data: result += i
            except:
                pass

            result = result.replace('\n','')
            movies = common.parseDOM(result, "div", attrs = { "class": "list_item.+?" })
        except:
            return

        for movie in movies:
            try:
                title = common.parseDOM(movie, "a", attrs = { "onclick": ".+?" })[-1]
                title = common.replaceHTMLCodes(title)
                title = title.encode('utf-8')

                year = common.parseDOM(movie, "span", attrs = { "class": "year_type" })[0]
                year = year.replace('(', '').replace(')', '')
                year = year.encode('utf-8')

                if not year.isdigit(): raise Exception()
                if int(year) > int((datetime.datetime.utcnow() - datetime.timedelta(hours = 5)).strftime("%Y")): raise Exception()

                name = '%s (%s)' % (title, year)
                try: name = name.encode('utf-8')
                except: pass

                url = common.parseDOM(movie, "a", ret="href")[0]
                url = '%s%s' % (link().imdb_base, url)
                url = common.replaceHTMLCodes(url)
                url = url.encode('utf-8')

                try:
                    image = common.parseDOM(movie, "img", ret="src")[0]
                    if not ('._SX' in image or '._SY' in image): raise Exception()
                    image = image.rsplit('._SX', 1)[0].rsplit('._SY', 1)[0] + '._SX500.' + image.rsplit('.', 1)[-1]
                except:
                    image = link().imdb_image
                image = common.replaceHTMLCodes(image)
                image = image.encode('utf-8')

                imdb = re.sub('[^0-9]', '', url.rsplit('tt', 1)[-1])
                imdb = imdb.encode('utf-8')

                try:
                    plot = common.parseDOM(movie, "div", attrs = { "class": "item_description" })[0]
                    plot = plot.rsplit('<span>', 1)[0].strip()
                    plot = common.replaceHTMLCodes(plot)
                    plot = plot.encode('utf-8')
                except:
                    plot = ''

                self.list.append({'name': name, 'url': url, 'image': image, 'title': title, 'year': year, 'imdb': imdb, 'genre': '', 'plot': plot})
            except:
                pass

        return self.list

    def trakt_list(self, url):
        try:
            post = urllib.urlencode({'username': link().trakt_user, 'password': link().trakt_password})

            result = getUrl(url, post=post).result
            result = json.loads(result)

            movies = []
            try: result = result['items']
            except: pass
            for i in result:
                try: movies.append(i['movie'])
                except: pass
            if movies == []: 
                movies = result
        except:
            return

        for movie in movies:
            try:
                title = movie['title']
                title = common.replaceHTMLCodes(title)
                title = title.encode('utf-8')

                year = movie['year']
                year = re.sub('[^0-9]', '', str(year))
                year = year.encode('utf-8')

                if int(year) > int((datetime.datetime.utcnow() - datetime.timedelta(hours = 5)).strftime("%Y")): raise Exception()

                name = '%s (%s)' % (title, year)
                try: name = name.encode('utf-8')
                except: pass

                imdb = movie['imdb_id']
                imdb = re.sub('[^0-9]', '', str(imdb))
                imdb = imdb.encode('utf-8')

                url = link().imdb_title % imdb
                url = common.replaceHTMLCodes(url)
                url = url.encode('utf-8')

                try: image = movie['images']['poster']
                except: image = movie['poster']
                image = common.replaceHTMLCodes(image)
                image = image.encode('utf-8')

                try:
                    genre = movie['genres']
                    genre = " / ".join(genre)
                    genre = common.replaceHTMLCodes(genre)
                    genre = genre.encode('utf-8')
                except:
                    genre = ''

                try:
                    plot = movie['overview']
                    plot = common.replaceHTMLCodes(plot)
                    plot = plot.encode('utf-8')
                except:
                    plot = ''

                self.list.append({'name': name, 'url': url, 'image': image, 'title': title, 'year': year, 'imdb': imdb, 'genre': genre, 'plot': plot})
            except:
                pass

        return self.list

    def ice_list(self):
        try:
            url = 'http://www.icefilms.info/movies/added/1'
            result = getUrl(url).result
            movies = common.parseDOM(result, "span", attrs = { "class": "list" })[0]
            movies = movies.split('<br>')
        except:
            return

        for movie in movies:
            try:
                title = common.parseDOM(movie, "a", attrs = { "href": ".+?" })[0]
                title = re.compile('(.+?)[(]\d{4}[)]').findall(title)[0]
                title = re.sub('\s[(].+?[)]', '', title.strip())
                title = common.replaceHTMLCodes(title)
                title = title.encode('utf-8')

                year = common.parseDOM(movie, "a", attrs = { "href": ".+?" })[0]
                year = re.compile('[(](\d{4})[)]').findall(year)[-1]
                year = year.encode('utf-8')

                name = '%s (%s)' % (title, year)
                try: name = name.encode('utf-8')
                except: pass

                imdb = common.parseDOM(movie, "a", ret="id")[0]
                imdb = re.sub('[^0-9]', '', str(imdb))
                imdb = imdb.encode('utf-8')

                url = link().imdb_title % imdb
                url = common.replaceHTMLCodes(url)
                url = url.encode('utf-8')

                image = link().imdb_image
                image = common.replaceHTMLCodes(image)
                image = image.encode('utf-8')

                self.list.append({'name': name, 'url': url, 'image': image, 'title': title, 'year': year, 'imdb': imdb, 'genre': '', 'plot': ''})
            except:
                pass

        return self.list

    def thread(self, url, i):
        try:
            result = getUrl(url, referer=url).result
            self.data[i] = result
        except:
            return


class trailer:
    def __init__(self):
        self.youtube_base = 'http://www.youtube.com'
        self.youtube_query = 'http://gdata.youtube.com/feeds/api/videos?q='
        self.youtube_watch = 'http://www.youtube.com/watch?v=%s'
        self.youtube_info = 'http://gdata.youtube.com/feeds/api/videos/%s?v=2'

    def run(self, name, url):
        try:
            if url.startswith(self.youtube_base):
                url = self.youtube(url)
                if url is None: raise Exception()
                return url
            elif not url.startswith('http://'):
                url = self.youtube_watch % url
                url = self.youtube(url)
                if url is None: raise Exception()
                return url
            else:
                raise Exception()
        except:
            url = self.youtube_query + name + ' trailer'
            url = self.youtube_search(url)
            if url is None: return
            return url

    def youtube_search(self, url):
        try:
            if index().addon_status('plugin.video.youtube') is None:
                index().okDialog(language(30321).encode("utf-8"), language(30322).encode("utf-8"))
                return

            query = url.split("?q=")[-1].split("/")[-1].split("?")[0]
            url = url.replace(query, urllib.quote_plus(query))
            result = getUrl(url).result
            result = common.parseDOM(result, "entry")
            result = common.parseDOM(result, "id")

            for url in result[:5]:
                url = url.split("/")[-1]
                url = self.youtube_watch % url
                url = self.youtube(url)
                if not url is None: return url
        except:
            return

    def youtube(self, url):
        try:
            if index().addon_status('plugin.video.youtube') is None:
                index().okDialog(language(30321).encode("utf-8"), language(30322).encode("utf-8"))
                return
            id = url.split("?v=")[-1].split("/")[-1].split("?")[0].split("&")[0]
            state, reason = None, None
            result = getUrl(self.youtube_info % id).result
            try:
                state = common.parseDOM(result, "yt:state", ret="name")[0]
                reason = common.parseDOM(result, "yt:state", ret="reasonCode")[0]
            except:
                pass
            if state == 'deleted' or state == 'rejected' or state == 'failed' or reason == 'requesterRegion' : return
            try:
                result = getUrl(self.youtube_watch % id).result
                alert = common.parseDOM(result, "div", attrs = { "id": "watch7-notification-area" })[0]
                return
            except:
                pass
            url = 'plugin://plugin.video.youtube/?action=play_video&videoid=%s' % id
            return url
        except:
            return

class resolver:
    def __init__(self):
        self.sources_dict()
        self.sources = []

    def get_host(self, name, title, imdb, year, url, image, genre, plot):
        try:
            self.sources = self.sources_get(name, title, imdb, year, self.hostDict)
            self.sources = self.sources_filter()
            if self.sources == []: raise Exception()

            for i in range(0,len(self.sources)):
                self.sources[i].update({'name': name, 'image': image, 'title': title, 'year': year, 'imdb': imdb, 'genre': genre, 'plot': plot})

            index().sourceList(self.sources)
        except:
            return

    def play_host(self, name, url, imdb, source, provider):
        try:
            url = self.sources_resolve(url, provider)
            if url is None: raise Exception()

            if getSetting("playback_info") == 'true':
                index().infoDialog(source, header=name)

            player().run(name, url, imdb)
            return url
        except:
            index().infoDialog(language(30318).encode("utf-8"))
            return

    def play(self, name, title, imdb, year, url):
        try:
            self.sources = self.sources_get(name, title, imdb, year, self.hostDict)
            self.sources = self.sources_filter()
            if self.sources == []: raise Exception()

            autoplay = getSetting("autoplay")
            if index().getProperty('PseudoTVRunning') == 'True':
                autoplay = 'true'
            elif not xbmc.getInfoLabel('Container.FolderPath').startswith(sys.argv[0]):
                autoplay = getSetting("autoplay_library")

            if url == 'play://':
                url = self.sources_direct()
            elif not autoplay == 'true':
                url = self.sources_dialog()
            else:
                url = self.sources_direct()


            if url is None: raise Exception()
            if url == 'close://': return

            if getSetting("playback_info") == 'true':
                index().infoDialog(self.selectedSource, header=name)

            player().run(name, url, imdb)
            return url
        except:
            if not index().getProperty('PseudoTVRunning') == 'True':
                index().infoDialog(language(30318).encode("utf-8"))
            return

    def sources_get(self, name, title, imdb, year, hostDict):
        threads = []

        global icefilms_sources
        icefilms_sources = []
        if getSetting("icefilms") == 'true':
            threads.append(Thread(icefilms().get, name, title, imdb, year, hostDict))

        global primewire_sources
        primewire_sources = []
        if getSetting("primewire") == 'true':
            threads.append(Thread(primewire().get, name, title, imdb, year, hostDict))

        global movie25_sources
        movie25_sources = []
        threads.append(Thread(movie25().get, name, title, imdb, year, hostDict))

        global flixanity_sources
        flixanity_sources = []
        if getSetting("flixanity") == 'true':
            threads.append(Thread(flixanity().get, name, title, imdb, year, hostDict))

        global vkbox_sources
        vkbox_sources = []
        if getSetting("vkbox") == 'true':
            threads.append(Thread(vkbox().get, name, title, imdb, year, hostDict))

        global istreamhd_sources
        istreamhd_sources = []
        if getSetting("istreamhd") == 'true':
            threads.append(Thread(istreamhd().get, name, title, imdb, year, hostDict))

        global simplymovies_sources
        simplymovies_sources = []
        if getSetting("simplymovies") == 'true':
            threads.append(Thread(simplymovies().get, name, title, imdb, year, hostDict))

        global movieshd_sources
        movieshd_sources = []
        if getSetting("movieshd") == 'true':
            threads.append(Thread(movieshd().get, name, title, imdb, year, hostDict))

        global glowgaze_sources
        glowgaze_sources = []
        if getSetting("glowgaze") == 'true':
            threads.append(Thread(glowgaze().get, name, title, imdb, year, hostDict))

        global movietube_sources
        movietube_sources = []
        if getSetting("movietube") == 'true':
            threads.append(Thread(movietube().get, name, title, imdb, year, hostDict))

        global yify_sources
        yify_sources = []
        if getSetting("yify") == 'true':
            threads.append(Thread(yify().get, name, title, imdb, year, hostDict))

        global moviestorm_sources
        moviestorm_sources = []
        if getSetting("moviestorm") == 'true':
            threads.append(Thread(moviestorm().get, name, title, imdb, year, hostDict))

        global noobroom_sources
        noobroom_sources = []
        if getSetting("noobroom") == 'true':
            threads.append(Thread(noobroom().get, name, title, imdb, year, hostDict))

        global einthusan_sources
        einthusan_sources = []
        if getSetting("einthusan") == 'true':
            threads.append(Thread(einthusan().get, name, title, imdb, year, hostDict))

        [i.start() for i in threads]
        [i.join() for i in threads]

        self.sources = icefilms_sources + primewire_sources + movie25_sources + flixanity_sources + vkbox_sources + istreamhd_sources + simplymovies_sources + movieshd_sources + glowgaze_sources + movietube_sources + yify_sources + moviestorm_sources + noobroom_sources + einthusan_sources

        return self.sources

    def sources_resolve(self, url, provider):
        try:
            if provider == 'Icefilms': url = icefilms().resolve(url)
            elif provider == 'Primewire': url = primewire().resolve(url)
            elif provider == 'Movie25': url = movie25().resolve(url)
            elif provider == 'Flixanity': url = flixanity().resolve(url)
            elif provider == 'VKBox': url = vkbox().resolve(url)
            elif provider == 'iStreamHD': url = istreamhd().resolve(url)
            elif provider == 'Simplymovies': url = simplymovies().resolve(url)
            elif provider == 'MoviesHD': url = movieshd().resolve(url)
            elif provider == 'Glowgaze': url = glowgaze().resolve(url)
            elif provider == 'Movietube': url = movietube().resolve(url)
            elif provider == 'YIFY': url = yify().resolve(url)
            elif provider == 'Moviestorm': url = moviestorm().resolve(url)
            elif provider == 'Noobroom': url = noobroom().resolve(url)
            elif provider == 'Einthusan': url = einthusan().resolve(url)
            return url
        except:
            return

    def sources_filter(self):
        #hd_rank = ['VK', 'MoviesHD', 'Glowgaze', 'Movietube', 'YIFY', 'Noobroom', 'Movreel', 'Billionuploads', '180upload', 'Hugefiles', 'Einthusan']
        #sd_rank = ['VK', 'Glowgaze', 'iShared', 'Noobroom', 'Firedrive', 'Putlocker', 'Sockshare', 'Played', 'Promptfile', 'Mightyupload', 'Gorillavid', 'Divxstage', 'Movreel', 'Flashx', 'Sharesix']
        hd_rank = [getSetting("hosthd1"), getSetting("hosthd2"), getSetting("hosthd3"), getSetting("hosthd4"), getSetting("hosthd5"), getSetting("hosthd6"), getSetting("hosthd7"), getSetting("hosthd8"), getSetting("hosthd9"), getSetting("hosthd10"), getSetting("hosthd11")]
        sd_rank = [getSetting("host1"), getSetting("host2"), getSetting("host3"), getSetting("host4"), getSetting("host5"), getSetting("host6"), getSetting("host7"), getSetting("host8"), getSetting("host9"), getSetting("host10"), getSetting("host11"), getSetting("host12"), getSetting("host13"), getSetting("host14"), getSetting("host15")]

        for i in range(len(self.sources)): self.sources[i]['source'] = self.sources[i]['source'].lower()
        self.sources = sorted(self.sources, key=itemgetter('source'))

        filter = []
        for host in hd_rank: filter += [i for i in self.sources if i['quality'] == 'HD' and i['source'].lower() == host.lower()]
        for host in sd_rank: filter += [i for i in self.sources if not i['quality'] == 'HD' and i['source'].lower() == host.lower()]
        filter += [i for i in self.sources if not i['quality'] == 'HD' and not any(x == i['source'].lower() for x in [r.lower() for r in sd_rank])]
        self.sources = filter

        filter = []
        filter += [i for i in self.sources if i['quality'] == 'HD']
        filter += [i for i in self.sources if i['quality'] == 'SD']
        filter += [i for i in self.sources if i['quality'] == 'SCR']
        filter += [i for i in self.sources if i['quality'] == 'CAM']
        self.sources = filter

        if not getSetting("quality") == 'true':
            self.sources = [i for i in self.sources if not i['quality'] == 'HD']

        count = 1
        for i in range(len(self.sources)):
            self.sources[i]['source'] = ''+ str('%02d' % count) + ' | [B]' + self.sources[i]['provider'].upper() + '[/B] | ' + self.sources[i]['source'].upper() + ' | ' + self.sources[i]['quality']
            count = count + 1

        return self.sources

    def sources_dialog(self):
        try:
            sourceList, urlList, providerList = [], [], []

            for i in self.sources:
                sourceList.append(i['source'])
                urlList.append(i['url'])
                providerList.append(i['provider'])

            select = index().selectDialog(sourceList)
            if select == -1: return 'close://'

            url = self.sources_resolve(urlList[select], providerList[select])
            self.selectedSource = self.sources[select]['source']
            return url
        except:
            return

    def sources_direct(self):
        u = None
        for i in self.sources:
            try:
                if i['provider'] == 'Icefilms' and i['quality'] == 'HD': raise Exception()
                url = self.sources_resolve(i['url'], i['provider'])
                xbmc.sleep(1000)
                if url is None: raise Exception()
                if u is None: u == url

                if url.startswith('http://'):
                    request = urllib2.Request(url.rsplit('|', 1)[0])
                    request.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/29.0.1547.57 Safari/537.36')
                    request.add_header('Cookie', 'video=true')
                    response = urllib2.urlopen(request, timeout=20)
                    chunk = response.read(16 * 1024)
                    response.close()
                    if 'text/html' in str(response.info()["Content-Type"]): raise Exception()

                self.selectedSource = i['source']
                return url
            except:
                pass

    def sources_dict(self):
        self.hostDict = [
        '2gb-hosting',
        'allmyvideos',
        #'180upload',
        'bayfiles',
        'bestreams',
        #'billionuploads',
        'castamp',
        #'clicktoview',
        'daclips',
        'divxstage',
        'donevideo',
        'ecostream',
        'filenuke',
        'firedrive',
        'flashx',
        'gorillavid',
        'hostingbulk',
        #'hugefiles',
        'ishared',
        'jumbofiles',
        'lemuploads',
        'limevideo',
        #'megarelease',
        'mightyupload',
        'movdivx',
        'movpod',
        'movreel',
        'movshare',
        'movzap',
        'muchshare',
        'nosvideo',
        'novamov',
        'nowvideo',
        'played',
        'playwire',
        'primeshare',
        'promptfile',
        'purevid',
        'putlocker',
        'sharerepo',
        'sharesix',
        'sockshare',
        'stagevu',
        'streamcloud',
        'thefile',
        'uploadc',
        'vidbull',
        'videobb',
        'videoweed',
        'videozed',
        #'vidhog',
        #'vidplay',
        'vidx',
        #'vidxden',
        #'watchfreeinhd',
        'xvidstage',
        'youtube',
        'yourupload',
        'youwatch',
        'zalaa'
        ]


class icefilms:
    def __init__(self):
        self.base_link = 'http://www.icefilms.info'
        self.search_link = 'http://www.icefilms.info/movies/a-z/%s'
        self.video_link = 'http://www.icefilms.info/membersonly/components/com_iceplayer/video.php?vid=%s'
        self.post_link = 'http://www.icefilms.info/membersonly/components/com_iceplayer/video.phpAjaxResp.php'

    def get(self, name, title, imdb, year, hostDict):
        try:
            global icefilms_sources
            icefilms_sources = []

            query = title.upper()
            if query.startswith('THE '): query = query.replace('THE ', '')
            elif query.startswith('A '): query = query.replace('A ', '')
            if not query[0].isalpha(): query = '1'
            query = self.search_link % query[0]

            result = getUrl(query).result
            result = result.decode('iso-8859-1').encode('utf-8')
            id = re.compile('id=%s>.+?href=/ip.php[?]v=(.+?)&' % imdb).findall(result)[0]
            url = self.video_link % id
            url = common.replaceHTMLCodes(url)
            url = url.encode('utf-8')

            result = getUrl(url).result
            result = result.decode('iso-8859-1').encode('utf-8')
            sec = re.compile('lastChild[.]value="(.+?)"').findall(result)[0]
            links = common.parseDOM(result, "div", attrs = { "class": "ripdiv" })

            import random

            try:
                hd_links = ''
                hd_links = [i for i in links if '>HD 720p<' in i][0]
                hd_links = re.compile("onclick='go[(](.+?)[)]'>Source(.+?)</a>").findall(hd_links)
            except:
                pass

            for url, host in hd_links:
                try:
                    hosts = ['movreel', 'billionuploads', '180upload', 'hugefiles']
                    host = re.sub('<span\s.+?>|</span>|#\d*:','', host)
                    host = host.strip().lower()
                    if not host in hosts: raise Exception()
                    url = 'id=%s&t=%s&sec=%s&s=%s&m=%s&cap=&iqs=&url=' % (url, id, sec, random.randrange(5, 50), random.randrange(100, 300) * -1)
                    icefilms_sources.append({'source': host, 'quality': 'HD', 'provider': 'Icefilms', 'url': url})
                except:
                    pass

            try:
                sd_links = ''
                sd_links = [i for i in links if '>DVDRip / Standard Def<' in i]
                if len(sd_links) == 0: sd_links = [i for i in links if '>DVD Screener<' in i]
                if len(sd_links) == 0: sd_links = [i for i in links if '>R5/R6 DVDRip<' in i]
                sd_links = sd_links[0]
                sd_links = re.compile("onclick='go[(](.+?)[)]'>Source(.+?)</a>").findall(sd_links)
            except:
                pass

            for url, host in sd_links:
                try:
                    hosts = ['movreel']
                    host = re.sub('<span\s.+?>|</span>|#\d*:','', host)
                    host = host.strip().lower()
                    if not host in hosts: raise Exception()
                    url = 'id=%s&t=%s&sec=%s&s=%s&m=%s&cap=&iqs=&url=' % (url, id, sec, random.randrange(5, 50), random.randrange(100, 300) * -1)
                    icefilms_sources.append({'source': host, 'quality': 'SD', 'provider': 'Icefilms', 'url': url})
                except:
                    pass
        except:
            return

    def resolve(self, url):
        try:
            result = getUrl(self.post_link, post=url).result
            url = result.split("?url=", 1)[-1]
            url = urllib.unquote_plus(url)

            import commonresolvers
            url = commonresolvers.resolvers().get(url)
            return url
        except:
            return

class primewire:
    def __init__(self):
        self.base_link = 'http://www.primewire.ag'
        self.key_link = 'http://www.primewire.ag/index.php?search'
        self.search_link = 'http://www.primewire.ag/index.php?search_keywords=%s&key=%s&search_section=1'
        self.proxy_base_link = 'http://9proxy.in'
        self.proxy_link = 'http://9proxy.in/b.php?u=%s&b=28'

    def get(self, name, title, imdb, year, hostDict):
        try:
            global primewire_sources
            primewire_sources = []

            try:
                result = getUrl(self.key_link).result
                key = common.parseDOM(result, "input", ret="value", attrs = { "name": "key" })[0]
                query = self.search_link % (urllib.quote_plus(re.sub('\'', '', title)), key)
            except:
                result = getUrl(self.proxy_link % urllib.quote_plus(urllib.unquote_plus(self.key_link)), referer=self.proxy_base_link).result
                key = common.parseDOM(result, "input", ret="value", attrs = { "name": "key" })[0]
                query = self.search_link % (urllib.quote_plus(re.sub('\'', '', title)), key)
                query = self.proxy_link % urllib.quote_plus(urllib.unquote_plus(query))
                self.base_link = self.proxy_base_link

            result = getUrl(query, referer=self.base_link, close=False).result
            result = result.decode('iso-8859-1').encode('utf-8')
            result = common.parseDOM(result, "div", attrs = { "class": "index_item.+?" })
            result = [i for i in result if any(x in re.compile('title="Watch (.+?)"').findall(i)[0] for x in ['(%s)' % str(year), '(%s)' % str(int(year)+1), '(%s)' % str(int(year)-1)])]
            result = uniqueList(result).list

            match = [common.parseDOM(i, "a", ret="href")[0] for i in result]
            if match == []: return
            for i in match[:5]:
                try:
                    if not i.startswith('http://'): i = '%s%s' % (self.base_link, i)
                    result = getUrl(i, referer=i).result
                    if any(x in self.cleantitle(result) for x in [str('>' + self.cleantitle(title) + '(%s)' % str(year) + '<')]):
                        match2 = i
                    if any(x in self.cleantitle(result) for x in [str('>' + self.cleantitle(title) + '<')]):
                        match2 = i
                    if str('tt' + imdb) in result:
                        match2 = i
                        break
                except:
                    pass

            url = match2
            result = getUrl(url, referer=url).result
            result = result.decode('iso-8859-1').encode('utf-8')
            links = common.parseDOM(result, "tbody")

            for i in links:
                try:
                    url = common.parseDOM(i, "a", ret="href")[0]
                    url = urllib.unquote_plus(url)
                    url = re.compile('url=(.+?)&').findall(url)[0]
                    url = base64.urlsafe_b64decode(url.encode('utf-8'))
                    if 'primewire.ag' in url: raise Exception()
                    url = common.replaceHTMLCodes(url)
                    url = url.encode('utf-8')

                    host = common.parseDOM(i, "a", ret="href")[0]
                    host = urllib.unquote_plus(host)
                    host = re.compile('domain=(.+?)&').findall(host)[0]
                    host = base64.urlsafe_b64decode(host.encode('utf-8'))
                    host = host.rsplit('.', 1)[0]
                    host = [x for x in hostDict if host.lower() == x.lower()][0]
                    host = host.encode('utf-8')

                    quality = common.parseDOM(i, "span", ret="class")[0]
                    if quality == 'quality_cam' or quality == 'quality_ts': quality = 'CAM'
                    elif quality == 'quality_dvd': quality = 'SD'
                    else:  raise Exception()
                    quality = quality.encode('utf-8')

                    primewire_sources.append({'source': host, 'quality': quality, 'provider': 'Primewire', 'url': url})
                except:
                    pass
        except:
            return

    def cleantitle(self, title):
        title = re.sub('\n|([[].+?[]])|([(].+?[)])|\s(vs|v[.])\s|(:|;|-|"|,|\'|\.|\?)|\s', '', title).lower()
        return title

    def resolve(self, url):
        try:
            import commonresolvers
            url = commonresolvers.resolvers().get(url)
            return url
        except:
            return

class movie25:
    def __init__(self):
        self.base_link = 'http://www.movie25.so'
        self.search_link = 'http://www.movie25.so/search.php?key=%s'

    def get(self, name, title, imdb, year, hostDict):
        try:
            global movie25_sources
            movie25_sources = []

            query = self.search_link % urllib.quote_plus(title)

            result = getUrl(query).result
            result = result.decode('iso-8859-1').encode('utf-8')
            result = common.parseDOM(result, "div", attrs = { "class": "movie_table" })[0]
            result = common.parseDOM(result, "li")

            match = [i for i in result if any(x in i for x in [' (%s)' % str(year), ' (%s)' % str(int(year)+1), ' (%s)' % str(int(year)-1)])]
            match2 = [self.base_link + common.parseDOM(i, "a", ret="href")[0] for i in match]
            if match2 == []: return
            for i in match2[:10]:
                try:
                    result = getUrl(i).result
                    result = result.decode('iso-8859-1').encode('utf-8')
                    if str('tt' + imdb) in result:
                        match3 = result
                        break
                except:
                    pass

            result = common.parseDOM(match3, "div", attrs = { "class": "links_quality" })[0]

            quality = common.parseDOM(result, "h1")[0]
            quality = quality.replace('\n','').rsplit(' ', 1)[-1]
            if quality == 'CAM' or quality == 'TS': quality = 'CAM'
            elif quality == 'SCREENER': quality = 'SCR'
            else: quality = 'SD'

            links = common.parseDOM(result, "ul")
            for i in links:
                try:
                    name = common.parseDOM(i, "a")[0]
                    name = common.replaceHTMLCodes(name)
                    if name.isdigit(): raise Exception()
                    host = common.parseDOM(i, "li", attrs = { "class": "link_name" })[0]
                    host = common.replaceHTMLCodes(host)
                    host = host.encode('utf-8')
                    host = [x for x in hostDict if host.lower() == x.lower()][0]
                    url = common.parseDOM(i, "a", ret="href")[0]
                    url = '%s%s' % (self.base_link, url)
                    url = common.replaceHTMLCodes(url)
                    url = url.encode('utf-8')
                    movie25_sources.append({'source': host, 'quality': quality, 'provider': 'Movie25', 'url': url})
                except:
                    pass
        except:
            return

    def resolve(self, url):
        try:
            result = getUrl(url).result
            result = result.decode('iso-8859-1').encode('utf-8')
            url = common.parseDOM(result, "input", ret="onclick")
            url = [i for i in url if 'location.href' in i and 'http://' in i][0]
            url = url.split("'", 1)[-1].rsplit("'", 1)[0]

            import commonresolvers
            url = commonresolvers.resolvers().get(url)
            return url
        except:
            return

class flixanity:
    def __init__(self):
        self.base_link = 'http://www.flixanity.com'
        self.search_link = 'http://www.flixanity.com/ajax/search.php?q=%s&limit=5'

    def get(self, name, title, imdb, year, hostDict):
        try:
            global flixanity_sources
            flixanity_sources = []

            query = self.search_link % urllib.quote_plus(title)

            result = getUrl(query).result
            result = json.loads(result)
            result = [i for i in result if 'Movie' in i['meta']]

            url = [i for i in result if any(x in self.cleantitle(i['title']) for x in [self.cleantitle(title)]) and any(x in i['title'] for x in [' (%s)' % str(year), ' (%s)' % str(int(year)+1), ' (%s)' % str(int(year)-1)])]
            if len(url) == 0:
                url = [i for i in result if any(x == self.cleantitle(i['title']) for x in [self.cleantitle(title)])]
            url = url[0]['permalink']
            url = common.replaceHTMLCodes(url)
            url = url.encode('utf-8')

            result = getUrl(url).result
            if not str('tt' + imdb) in result: raise Exception()

            result = common.parseDOM(result, "script")
            result = [i for i in result if 'var embeds' in i][0]
            result = result.replace('IFRAME', 'iframe').replace('SRC=', 'src=')
            links = common.parseDOM(result, "iframe", ret="src")
            links = [i.split('player.php?', 1)[-1] for i in links]

            for url in links:
                try:
                    host = re.compile('://(.+?)/').findall(url)[0]
                    host = host.rsplit('.', 1)[0].split('w.', 1)[-1]
                    host = [x for x in hostDict if host.lower() == x.lower()][0]

                    flixanity_sources.append({'source': host, 'quality': 'SD', 'provider': 'Flixanity', 'url': url})
                except:
                    pass
        except:
            return

    def cleantitle(self, title):
        title = re.sub('\n|([[].+?[]])|([(].+?[)])|\s(vs|v[.])\s|(:|;|-|"|,|\'|\.|\?)|\s', '', title).lower()
        return title

    def resolve(self, url):
        try:
            import commonresolvers
            url = commonresolvers.resolvers().get(url)
            return url
        except:
            return

class vkbox:
    def __init__(self):
        self.base_link = 'http://mobapps.cc'
        self.data_link = 'http://mobapps.cc/data/data_en.zip'
        self.movie_link = 'http://mobapps.cc/api/serials/get_movie_data/?id=%s'
        self.movies_link = 'movies_lite.json'

    def get(self, name, title, imdb, year, hostDict):
        try:
            global vkbox_sources
            vkbox_sources = []

            #result = self.getdata()
            result = cache2(self.getdata)
            result = json.loads(result)

            match = [i['id'] for i in result if any(x == self.cleantitle(i['title']) for x in [self.cleantitle(title), self.cleantitle(title)]) and any(x == i['year'] for x in [str(year), str(int(year)+1), str(int(year)-1)])][0]
            url = self.movie_link % match
            url = common.replaceHTMLCodes(url)
            url = url.encode('utf-8')

            request = urllib2.Request(url,None)
            request.add_header('User-Agent', 'android-async-http/1.4.1 (http://loopj.com/android-async-http)')
            response = urllib2.urlopen(request, timeout=10)
            result = response.read()
            response.close()
            param = re.findall('"lang":"en","apple":(\d+?),"google":(\d+?),"microsoft":"(.+?)"', result, re.I)
            num = int(match) + 537
            url = 'https://vk.com/video_ext.php?oid=%s&id=%s&hash=%s' % (str(int(param[0][0]) + num), str(int(param[0][1]) + num), param[0][2])

            import commonresolvers
            url = commonresolvers.resolvers().vk(url)
            for i in url: vkbox_sources.append({'source': 'VK', 'quality': i['quality'], 'provider': 'VKBox', 'url': i['url']})
        except:
            return

    def getdata(self):
        try:
            import zipfile, StringIO
            data = urllib2.urlopen(self.data_link, timeout=10).read()
            zip = zipfile.ZipFile(StringIO.StringIO(data))
            read = zip.open(self.movies_link)
            result = read.read()
            return result
        except:
            return

    def cleantitle(self, title):
        title = re.sub('\n|([[].+?[]])|([(].+?[)])|\s(vs|v[.])\s|(:|;|-|"|,|\'|\.|\?)|\s', '', title).lower()
        return title

    def resolve(self, url):
        return url

class istreamhd:
    def __init__(self):
        self.base_link = 'http://istreamhd.org'
        self.login_link = 'aHR0cDovL2lzdHJlYW1oZC5vcmcvYXBpL2F1dGhlbnRpY2F0ZS5waHA='
        self.search_link = 'aHR0cDovL2lzdHJlYW1oZC5vcmcvYXBpL3NlYXJjaC5waHA='
        self.show_link = 'aHR0cDovL2lzdHJlYW1oZC5vcmcvYXBpL2dldF9zaG93LnBocA=='
        self.get_link = 'aHR0cDovL2lzdHJlYW1oZC5vcmcvYXBpL2dldF92aWRlby5waHA='
        self.mail, self.password = getSetting("istreamhd_mail"), getSetting("istreamhd_password")

    def get(self, name, title, imdb, year, hostDict):
        try:
            global istreamhd_sources
            istreamhd_sources = []

            if (self.mail == '' or self.password == ''): raise Exception()

            post = urllib.urlencode({'e-mail': self.mail, 'password': self.password})
            result = getUrl(base64.urlsafe_b64decode(self.login_link), post=post).result
            result = json.loads(result)
            token = result['auth']['token']

            post = urllib.urlencode({'token': token, 'query': title})
            result = getUrl(base64.urlsafe_b64decode(self.search_link), post=post).result
            result = json.loads(result)
            url = result['result']['items']
            url = [i for i in url if str('tt' + imdb) in i['imdb_id']][0]
            url = url['id']

            post = urllib.urlencode({'token': token, 'vid_id': url})
            result = getUrl(base64.urlsafe_b64decode(self.get_link), post=post).result
            result = json.loads(result)
            url = result['video']['url']
            url = url.replace('http://', 'https://')
            url = common.replaceHTMLCodes(url)
            url = url.encode('utf-8')

            import commonresolvers
            url = commonresolvers.resolvers().vk(url)
            for i in url: istreamhd_sources.append({'source': 'VK', 'quality': i['quality'], 'provider': 'iStreamHD', 'url': i['url']})
        except:
            return

    def resolve(self, url):
        return url

class simplymovies:
    def __init__(self):
        self.base_link = 'http://simplymovies.net'
        self.search_link = 'http://simplymovies.net/index.php?searchTerm='

    def get(self, name, title, imdb, year, hostDict):
        try:
            global simplymovies_sources
            simplymovies_sources = []

            query = self.search_link + urllib.quote_plus(title.replace(' ', '-'))

            result = getUrl(query).result
            url = common.parseDOM(result, "div", attrs = { "class": "movieInfoHolder" })
            try: match = [i for i in url if any(x in self.cleantitle(i) for x in [str('>' + self.cleantitle(title) + '<')]) and any(x in i for x in [', %s<' % str(year), ', %s<' % str(int(year)+1), ', %s<' % str(int(year)-1)])][0]
            except: pass
            try: match = [i for i in url if str('tt' + imdb) in i][0]
            except: pass
            url = common.parseDOM(match, "a", ret="href")[0]
            url = '%s/%s' % (self.base_link, url)
            url = common.replaceHTMLCodes(url)
            url = url.encode('utf-8')

            result = getUrl(url).result
            url = common.parseDOM(result, "iframe", ret="src", attrs = { "class": "videoPlayerIframe" })[0]
            url = common.replaceHTMLCodes(url)
            url = url.replace('http://', 'https://')
            url = url.encode('utf-8')

            import commonresolvers
            url = commonresolvers.resolvers().vk(url)
            for i in url: simplymovies_sources.append({'source': 'VK', 'quality': i['quality'], 'provider': 'Simplymovies', 'url': i['url']})
        except:
            return

    def cleantitle(self, title):
        title = re.sub('\n|([[].+?[]])|([(].+?[)])|\s(vs|v[.])\s|(:|;|-|"|,|\'|\.|\?)|\s', '', title).lower()
        return title

    def resolve(self, url):
        return url

class movieshd:
    def __init__(self):
        self.base_link = 'http://movieshd.co'
        self.search_link = 'http://movieshd.co/?s=%s'
        self.player_link = 'http://videomega.tv/iframe.php?ref=%s'

    def get(self, name, title, imdb, year, hostDict):
        try:
            global movieshd_sources
            movieshd_sources = []

            query = self.search_link % (urllib.quote_plus(title))

            result = getUrl(query).result
            url = common.parseDOM(result, "ul", attrs = { "class": "listing-videos.+?" })[0]
            url = common.parseDOM(url, "li", attrs = { "class": ".+?" })
            url = [i for i in url if any(x in self.cleantitle(re.sub('[(]\d{4}[)]', '<', i)) for x in [str('>' + self.cleantitle(title) + '<')]) and any(x in i for x in [' (%s)' % str(year), ' (%s)' % str(int(year)+1), ' (%s)' % str(int(year)-1)])][0]
            url = common.parseDOM(url, "a", ret="href")[0]
            url = common.replaceHTMLCodes(url)
            url = url.encode('utf-8')

            result = getUrl(url).result
            url = common.parseDOM(result, "div", attrs = { "class": "video-embed" })[0]
            url = re.compile("ref='(.+?)'").findall(url)[0]
            url = self.player_link % url
            url = url.encode('utf-8')

            import commonresolvers
            url = commonresolvers.resolvers().videomega(url)
            if url == None: return

            movieshd_sources.append({'source': 'MoviesHD', 'quality': 'HD', 'provider': 'MoviesHD', 'url': url})
        except:
            return

    def cleantitle(self, title):
        title = re.sub('\n|([[].+?[]])|([(].+?[)])|\s(vs|v[.])\s|(:|;|-|"|,|\'|\.|\?)|\s', '', title).lower()
        return title

    def resolve(self, url):
        return url

class glowgaze:
    def __init__(self):
        self.base_link = 'http://g2g.fm'
        self.forum_link = 'http://g2g.fm/forum'
        self.search_link = 'http://g2g.fm/forum/search.php?do=process&titleonly=1&query=online+%s'

    def get(self, name, title, imdb, year, hostDict):
        try:
            global glowgaze_sources
            glowgaze_sources = []

            query = self.search_link % (urllib.quote_plus(title))

            result = getUrl(query).result
            result = result.decode('iso-8859-1').encode('utf-8')
            url = common.parseDOM(result, "div", attrs = { "class": "threadinfo thread" })
            url = [i for i in url if any(x in self.cleantitle(re.sub('[(]\d{4}[)]', '<', i)) for x in [str('>' + self.cleantitle(title) + '<')]) and any(x in i for x in [' (%s)' % str(year), ' (%s)' % str(int(year)+1), ' (%s)' % str(int(year)-1)])][0]
            name = common.parseDOM(url, "a", attrs = { "class": "title" })[0]
            url = common.parseDOM(url, "a", ret="href", attrs = { "class": "title" })[0]
            url = re.findall('(.+?[?]\d+)-', url, re.I)[0]
            url = '%s/%s' % (self.forum_link, url)
            url = common.replaceHTMLCodes(url)
            url = url.encode('utf-8')

            if ' Season ' in name and ' Episode ' in name: raise Exception()
            if ' 1080p ' in name or ' 720p ' in name: quality = 'HD'
            else: quality = 'SD'

            url = getUrl(url).result
            url = url.decode('iso-8859-1').encode('utf-8')
            url = common.parseDOM(url, "iframe", ret="src", attrs = { "webkitallowfullscreen": ".+?" })[0]
            url = getUrl(url, referer=self.base_link).result
            url = common.parseDOM(url, "iframe", ret="src")[0]
            url = getUrl(url, referer=self.base_link).result

            u = re.compile('"(https://redirector.googlevideo.com/.+?)"').findall(url)
            u += re.compile('"(http://redirector.googlevideo.com/.+?)"').findall(url)
            u += re.compile('"(https://docs.google.com/.+?)"').findall(url)
            u += re.compile('"(http://docs.google.com/.+?)"').findall(url)
            url = u[-1]

            if 'docs.google.com' in url:
                import commonresolvers
                url = commonresolvers.resolvers().googledocs(url)
                if url == None: return
            elif 'googlevideo.com' in url:
                url = getUrl(url, output='geturl').result

            glowgaze_sources.append({'source': 'Glowgaze', 'quality': quality, 'provider': 'Glowgaze', 'url': url})
        except:
            return

    def cleantitle(self, title):
        title = re.sub('\n|([[].+?[]])|([(].+?[)])|\s(vs|v[.])\s|(:|;|-|"|,|\'|\.|\?)|\s', '', title).lower()
        return title

    def resolve(self, url):
        try:
            url = getUrl(url, output='geturl').result
            if 'requiressl=yes' in url: url = url.replace('http://', 'https://')
            else: url = url.replace('https://', 'http://')
            return url
        except:
            return

class movietube:
    def __init__(self):
        self.base_link = 'http://www.movietube.cc'
        self.index_link = 'http://www.movietube.cc/index.php'

    def get(self, name, title, imdb, year, hostDict):
        try:
            global movietube_sources
            movietube_sources = []

            post = urllib.urlencode({'a': 'retrieve', 'c': 'result', 'p': '{"KeyWord":"%s","Page":"1","NextToken":""}' % title})
            result = getUrl(self.index_link, post=post).result
            result = result.decode('iso-8859-1').encode('utf-8')
            url = common.parseDOM(result, "tr")
            url = [i for i in url if any(x in self.cleantitle(re.sub('[(]\d{4}[)]', '<', i)) for x in [str('>' + self.cleantitle(title) + '<')]) and any(x in i for x in [' (%s)' % str(year), ' (%s)' % str(int(year)+1), ' (%s)' % str(int(year)-1)])][0]
            url = common.parseDOM(url, "a", ret="href")[0]
            url = url.split('?v=')[-1]

            post = urllib.urlencode({'a': 'getmoviealternative', 'c': 'result', 'p': '{"KeyWord":"%s"}' % url})
            result = getUrl(self.index_link, post=post).result
            if not result == '':
                result = re.compile('(<a.+?</a>)').findall(result)
                result = [i for i in result if '0000000008400000' in i or '0000000008100000' in i]
                u = [i for i in result if '>1080p<' in i]
                u += [i for i in result if '>720p<' in i]
                u = [common.parseDOM(i, "a", ret="href")[0] for i in u]
                u = [i.split('?v=')[-1] for i in u]
                u = u[:3]
            else:
                u = [url]

            for i in u:
                try:
                    post = urllib.urlencode({'a': 'getplayerinfo', 'c': 'result', 'p': '{"KeyWord":"%s"}' % url})
                    result = getUrl(self.index_link, post=post).result

                    try: url = common.parseDOM(result, "source", ret="src", attrs = { "type": "video/mp4" })[0]
                    except: url = common.parseDOM(result, "iframe", ret="src")[0]

                    if 'docs.google.com' in url:
                        import commonresolvers
                        url = commonresolvers.resolvers().googledocs(url)
                        if url == None: raise Exception()
                    elif 'googlevideo.com' in url:
                        url = getUrl(url, output='geturl').result

                    movietube_sources.append({'source': 'Movietube', 'quality': 'HD', 'provider': 'Movietube', 'url': url})
                    return
                except:
                    pass
        except:
            return

    def cleantitle(self, title):
        title = re.sub('\n|([[].+?[]])|([(].+?[)])|\s(vs|v[.])\s|(:|;|-|"|,|\'|\.|\?)|\s', '', title).lower()
        return title

    def resolve(self, url):
        try:
            url = getUrl(url, output='geturl').result
            if 'requiressl=yes' in url: url = url.replace('http://', 'https://')
            else: url = url.replace('https://', 'http://')
            return url
        except:
            return

class yify:
    def __init__(self):
        self.base_link = 'http://yify.tv'
        self.ajax_link = 'http://yify.tv/wp-admin/admin-ajax.php'
        self.post_link = 'action=ajaxy_sf&sf_value=%s'
        self.player_link = 'http://yify.tv/reproductor2/pk/pk/plugins/player_p2.php?url=%s'

    def get(self, name, title, imdb, year, hostDict):
        try:
            global yify_sources
            yify_sources = []

            query = self.post_link % (urllib.quote_plus(title))

            result = getUrl(self.ajax_link, post=query).result
            result = result.replace('&#8211;','-')
            url = json.loads(result)
            url = url['post']['all']
            url = [i['post_link'] for i in url if any(x == self.cleantitle(i['post_title']) for x in [self.cleantitle(title), self.cleantitle(title)])][0]
            url = common.replaceHTMLCodes(url)
            url = url.encode('utf-8')

            result = getUrl(url).result
            if not str('tt' + imdb) in result: raise Exception()

            url = re.compile('showPkPlayer[(]"(.+?)"[)]').findall(result)[0]
            url = self.player_link % url

            result = getUrl(url, referer=url).result
            result = json.loads(result)

            url = [i['url'] for i in result if 'x-shockwave-flash' in i['type']]
            url += [i['url'] for i in result if 'video/mpeg4' in i['type']]
            url = url[-1]

            yify_sources.append({'source': 'YIFY', 'quality': 'HD', 'provider': 'YIFY', 'url': url})
        except:
            return

    def cleantitle(self, title):
        title = re.sub('\n|([[].+?[]])|([(].+?[)])|\s(vs|v[.])\s|(:|;|-|"|,|\'|\.|\?)|\s', '', title).lower()
        return title

    def resolve(self, url):
        try:
            url = getUrl(url, output='geturl').result
            if 'requiressl=yes' in url: url = url.replace('http://', 'https://')
            else: url = url.replace('https://', 'http://')
            return url
        except:
            return

class moviestorm:
    def __init__(self):
        self.base_link = 'http://moviestorm.eu'
        self.search_link = 'http://moviestorm.eu/search?q=%s'

    def get(self, name, title, imdb, year, hostDict):
        try:
            global moviestorm_sources
            moviestorm_sources = []

            query = self.search_link % (urllib.quote_plus(title))

            result = getUrl(query).result
            url = common.parseDOM(result, "div", attrs = { "class": "movie_box" })
            url = [i for i in url if str('tt' + imdb) in i][0]
            url = common.parseDOM(url, "a", ret="href")[0]
            url = common.replaceHTMLCodes(url)
            url = url.encode('utf-8')

            result = getUrl(url).result
            result = common.parseDOM(result, "div", attrs = { "class": "links" })[0]
            links = common.parseDOM(result, "tr")
            links = [i for i in links if 'http://ishared.eu/' in i]

            sd_links = [re.compile('"(http://ishared.eu/.+?)"').findall(i)[0] for i in links if not any(x in common.parseDOM(i, "td", attrs = { "class": "quality_td" })[0] for x in ['CAM', 'TS'])]
            ts_links = [re.compile('"(http://ishared.eu/.+?)"').findall(i)[0] for i in links if any(x in common.parseDOM(i, "td", attrs = { "class": "quality_td" })[0] for x in ['CAM', 'TS'])]

            if (len(sd_links) == 1):
                moviestorm_sources.append({'source': 'iShared', 'quality': 'SD', 'provider': 'Moviestorm', 'url': sd_links[0]})
            if (len(ts_links) == 1):
                moviestorm_sources.append({'source': 'iShared', 'quality': 'CAM', 'provider': 'Moviestorm', 'url': ts_links[0]})
        except:
            return

    def resolve(self, url):
        try:
            import commonresolvers
            url = commonresolvers.resolvers().get(url)
            return url
        except:
            return

class noobroom:
    def __init__(self):
        self.base_link = 'http://noobroom5.com'
        self.search_link = 'http://noobroom5.com/search.php?q=%s'
        self.login_link = 'http://noobroom5.com/login.php'
        self.login2_link = 'http://noobroom5.com/login2.php'
        self.mail, self.password = getSetting("noobroom_mail"), getSetting("noobroom_password")

    def get(self, name, title, imdb, year, hostDict):
        try:
            global noobroom_sources
            noobroom_sources = []

            if (self.mail == '' or self.password == ''): raise Exception()

            query = self.search_link % (urllib.quote_plus(title))

            result = self.login()
            result = getUrl(query).result

            url = re.compile('(<i>Movies</i>.+)').findall(result)[0]
            url = url.split("'tippable'")
            url = [i for i in url if any(x in self.cleantitle(i) for x in [str('>' + self.cleantitle(title) + '<')]) and any(x in i for x in [' (%s)' % str(year), ' (%s)' % str(int(year)+1), ' (%s)' % str(int(year)-1)])][0]
            url = re.compile("href='(.+?)'").findall(url)[0]
            url = '%s%s' % (self.base_link, url)
            url = common.replaceHTMLCodes(url)
            url = url.encode('utf-8')

            result = getUrl(url).result

            if not str('tt' + imdb) in result: raise Exception()

            links = re.compile('"file": "(.+?)"').findall(result)
            try: u = [i for i in links if 'type=flv' in i][0]
            except: pass
            try: u = [i for i in links if 'type=mp4' in i][0]
            except: pass
            url = '%s%s' % (self.base_link, u)
            url = common.replaceHTMLCodes(url)
            url = url.encode('utf-8')

            try:
                quality = 'SD'
                q = re.compile('"width": "(.+?)"').findall(result)[0]
                if int(q) > 720: quality = 'HD'
            except:
                pass

            noobroom_sources.append({'source': 'Noobroom', 'quality': quality, 'provider': 'Noobroom', 'url': url})
        except:
            return

    def login(self):
        try:
            post = urllib.urlencode({'email': self.mail, 'password': self.password})
            result = getUrl(self.login_link, close=False).result
            cookie = getUrl(self.login_link, output='cookie').result
            result = urllib2.Request(self.login2_link, post)
            result = urllib2.urlopen(result, timeout=10)
        except:
            return

    def cleantitle(self, title):
        title = re.sub('\n|([[].+?[]])|([(].+?[)])|\s(vs|v[.])\s|(:|;|-|"|,|\'|\.|\?)|\s', '', title).lower()
        return title

    def resolve(self, url):
        try:
            result = self.login()
            try: u = getUrl(url, output='geturl').result
            except: pass
            try: u = getUrl(url.replace('&hd=0', '&hd=1'), output='geturl').result
            except: pass
            return u
        except:
            return

class einthusan:
    def __init__(self):
        self.base_link = 'http://www.einthusan.com'
        self.search_link = 'http://www.einthusan.com/search/?search_query=%s&lang=%s'

    def get(self, name, title, imdb, year, hostDict):
        try:
            global einthusan_sources
            einthusan_sources = []

            search = 'http://www.imdbapi.com/?i=tt%s' % imdb
            search = getUrl(search).result
            search = json.loads(search)
            country = [i.strip() for i in search['Country'].split(',')]
            if not 'India' in country: return

            language = [i.strip().lower() for i in search['Language'].split(',')]
            language = [i for i in language if any(x == i for x in ['hindi', 'tamil', 'telugu', 'malayalam'])][0]

            query = self.search_link % (urllib.quote_plus(title), language)

            result = getUrl(query).result
            result = common.parseDOM(result, "div", attrs = { "class": "search-category" })
            result = [i for i in result if 'Movies' in common.parseDOM(i, "p")[0]][0]
            result = common.parseDOM(result, "li")

            url = [i for i in result if any(x in self.cleantitle(common.parseDOM(i, "a")[0]) for x in [self.cleantitle(title)]) and any(x in common.parseDOM(i, "a")[0] for x in [' (%s)' % str(year), ' (%s)' % str(int(year)+1), ' (%s)' % str(int(year)-1)])]
            if len(url) == 0:
                url = [i for i in result if any(x == self.cleantitle(common.parseDOM(i, "a")[0]) for x in [self.cleantitle(title)])]
            url = common.parseDOM(url, "a", ret="href")[0]
            url = url.replace('../', '%s/' % self.base_link)
            url = common.replaceHTMLCodes(url)
            url = url.encode('utf-8')

            result = getUrl(url).result

            y = common.parseDOM(result, "div", attrs = { "class": "movie-description" })[0]
            if not any(x in y for x in [str(year), str(int(year)+1), str(int(year)-1)]): return

            url = re.compile("'file': '(.+?)'").findall(result)[0]

            einthusan_sources.append({'source': 'Einthusan', 'quality': 'HD', 'provider': 'Einthusan', 'url': url})
        except:
            return

    def cleantitle(self, title):
        title = re.sub('\n|([[].+?[]])|([(].+?[)])|\s(vs|v[.])\s|(:|;|-|"|,|\'|\.|\?)|\s', '', title).lower()
        return title

    def resolve(self, url):
        return url


main()