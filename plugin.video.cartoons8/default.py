import urllib,urllib2,re,xbmcplugin,xbmcgui,sys,xbmc,xbmcaddon,os
from t0mm0.common.addon import Addon

addon_id = 'plugin.video.cartoons8'
selfAddon = xbmcaddon.Addon(id=addon_id)
datapath= xbmc.translatePath(selfAddon.getAddonInfo('profile'))
addon = Addon(addon_id, sys.argv)
fanart = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id , 'fanart.jpg'))
icon = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id, 'icon.png'))

def CATEGORIES():
        addDir('New Cartoons','http://cartoons8.com/new/page/1',1,icon,fanart)
        addDir('Top Cartoons','http://cartoons8.com/top/page/1',1,icon,fanart)
        addDir('Cartoon Series','http://cartoons8.com/series/page/1',1,icon,fanart)
        addDir('Latest Updates','http://cartoons8.com/latestupdate/page/1',4,icon,fanart)
        addDir('Full Cartoon List','http://cartoons8.com/list/page/1',5,icon,fanart)
        addDir('Cartoon Genres','http://cartoons8.com',6,icon,fanart)
        addLink('','url','mode',icon,fanart)
        addDir('Search','http://cartoons8.com',8,icon,fanart)

        xbmc.executebuiltin('Container.SetViewMode(50)')
        
def GETMOVIES(url,name):
        pagenum = url.split('page/')
        curpage = int(pagenum[1])
        nextpage = curpage + 1
        nextpageurl = pagenum[0]+'page/'+str(nextpage)
        link = open_url(url)
        link=link.replace('\n','').replace('  ','')
        match=re.compile('<div class="thumbs"><a href="(.+?)"><img alt=".+?" title="(.+?)" src="(.+?)" /></a></div>').findall(link)
        for url, name, iconimage in match:
                name = cleanHex(name)
                addDir(name,url,2,iconimage,fanart)
        try:
                addDir('Next Page>>',nextpageurl,1,icon,fanart)
        except: pass
                
def GETEPISODES(url,name,iconimage):
        link = open_url(url)
        link=link.replace('\n','').replace('  ','')

        match=re.compile('<atitle="(.+?)" href="(.+?)">.+?</a>',re.DOTALL).findall(link)

        
        for name, url in match:
                name = cleanHex(name)
                addLink(name,url,100,iconimage,fanart)
        if len(match)==1:PLAYLINK(name,url)

def GETLATEST(url,name):
        link = open_url(url)
        link=link.replace('\n','').replace('  ','')
        match=re.compile('<a style="float: left" title="" href=".+?">(.+?)</a><span style="float: right; margin-right: 30px;"><a href="(.+?)">(.+?)</a></span>').findall(link)
        for name, url, episode in match:
                name = cleanHex(name)+' - '+episode
                addLink(name,url,100,icon,fanart)
        if len(match)==1:PLAYLINK(name,url)

def GETFULL(url,name):
        pagenum = url.split('page/')
        curpage = int(pagenum[1])
        nextpage = curpage + 1
        nextpageurl = pagenum[0]+'page/'+str(nextpage)
        link = open_url(url)
        link=link.replace('\n','').replace('  ','')
        match=re.compile('<a style="float: left" title="" href="(.+?)"> (.+?) </a>').findall(link)
        for url, name in match:
                addDir(name,url,2,iconimage,fanart)
        try:
                addDir('Next Page>>',nextpageurl,5,icon,fanart)
        except: pass

def GETGENRES(url):
        link = open_url(url)
        link=link.replace('\n','').replace('  ','')
        match=re.compile('href="(.+?)">(.+?)</a>').findall(link)
        for url, name in match:
                if 'genres' in url:
                        addDir(name,url,7,icon,fanart)
                
def GETGENREMOVIES(url):
        link = open_url(url)
        link=link.replace('\n','').replace('  ','')
        match=re.compile('<img src="(.+?)" /></a></div><div class="info"><a href="(.+?)"><span class="title">(.+?)</span>').findall(link)
        for iconimage,url, name in match:
                addDir(name,url,2,iconimage,fanart)

def SEARCH():
    search_entered =''
    keyboard = xbmc.Keyboard(search_entered, 'Search Cartoons')
    keyboard.doModal()
    if keyboard.isConfirmed():
        search_entered = keyboard.getText().replace(' ','+')
    if len(search_entered)>1:
        url = 'http://cartoons8.com/search/?s='+ search_entered
        link = open_url(url)
        GETGENREMOVIES(url)
        

def PLAYLINK(name,url):
        link = open_url(url)
        match=re.compile("var txha = '(.+?)';").findall(link)[0]    
        playlist = xbmc.PlayList(1)
        playlist.clear()
        listitem = xbmcgui.ListItem(name, iconImage=icon, thumbnailImage=icon)
        listitem.setInfo("Video", {"Title":name})
        listitem.setProperty('mimetype', 'video/x-msvideo')
        listitem.setProperty('IsPlayable', 'true')
        playlist.add(match,listitem)
        xbmcPlayer = xbmc.Player(xbmc.PLAYER_CORE_AUTO)
        xbmcPlayer.play(playlist)

def get_params():
        param=[]
        paramstring=sys.argv[2]
        if len(paramstring)>=2:
                params=sys.argv[2]
                cleanedparams=params.replace('?','')
                if (params[len(params)-1]=='/'):
                        params=params[0:len(params)-2]
                pairsofparams=cleanedparams.split('&')
                param={}
                for i in range(len(pairsofparams)):
                        splitparams={}
                        splitparams=pairsofparams[i].split('=')
                        if (len(splitparams))==2:
                                param[splitparams[0]]=splitparams[1]
        return param

def addDir(name,url,mode,iconimage,description=''):
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&iconimage="+urllib.quote_plus(iconimage)+"&description="+urllib.quote_plus(description)
        ok=True
        liz=xbmcgui.ListItem(name.strip(), iconImage="DefaultFolder.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name, "Plot": description} )
        liz.setProperty('fanart_image', fanart)
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
        return ok

def addLink(name,url,mode,iconimage,fanart,description=''):
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&iconimage="+urllib.quote_plus(iconimage)+"&description="+urllib.quote_plus(description)
        ok=True
        liz=xbmcgui.ListItem(name.strip(), iconImage="DefaultFolder.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name, "Plot": description} )
        liz.setProperty('fanart_image', fanart)
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=False)
        return ok
        
def open_url(url):
    req = urllib2.Request(url)
    req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
    response = urllib2.urlopen(req)
    link=response.read()
    response.close()
    return link
                
def cleanHex(text):
    def fixup(m):
        text = m.group(0)
        if text[:3] == "&#x": return unichr(int(text[3:-1], 16)).encode('utf-8')
        else: return unichr(int(text[2:-1])).encode('utf-8')
    return re.sub("(?i)&#\w+;", fixup, text.decode('ISO-8859-1').encode('utf-8'))

def setView(content, viewType):
    if content:
        xbmcplugin.setContent(int(sys.argv[1]), content)
    if selfAddon.getSetting('auto-view')=='true':
        xbmc.executebuiltin("Container.SetViewMode(%s)" % selfAddon.getSetting(viewType) )

params=get_params(); url=None; name=None; mode=None; site=None; iconimage=None
try: site=urllib.unquote_plus(params["site"])
except: pass
try: url=urllib.unquote_plus(params["url"])
except: pass
try: name=urllib.unquote_plus(params["name"])
except: pass
try: mode=int(params["mode"])
except: pass
try: iconimage=urllib.unquote_plus(params["iconimage"])
except: pass

print "Site: "+str(site); print "Mode: "+str(mode); print "URL: "+str(url); print "Name: "+str(name); print "IconImage: "+str(iconimage)
print params

if mode==None or url==None or len(url)<1: CATEGORIES()
elif mode==1: GETMOVIES(url,name)
elif mode==2: GETEPISODES(url,name,iconimage)
elif mode==3: SEARCH()
elif mode==4: GETLATEST(url,name)
elif mode==5: GETFULL(url,name)
elif mode==6: GETGENRES(url)
elif mode==7: GETGENREMOVIES(url)
elif mode==8: SEARCH()
elif mode==100: PLAYLINK(name,url)

xbmcplugin.endOfDirectory(int(sys.argv[1]))

