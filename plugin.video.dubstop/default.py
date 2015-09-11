import urllib,urllib2,re,xbmcplugin,xbmcgui,base64,xbmcaddon


addon_id = 'plugin.video.dubstop'


def CATEGORIES():
        addDir('[COLOR yellow]Movies[/COLOR]','url',3,'','0')
        addDir('[COLOR yellow]TV Shows[/COLOR]','url',6,'','0')
        addDir('[COLOR yellow]Latest Added[/COLOR]','http://uflix.me/movies/date',10,'','0')
        addDir('[COLOR lightgreen]Search[/COLOR]','search',10,'','0')
                       
def INDEX(url):
        URL=url
        link=OPEN_URL(url)
        match=re.compile('style="background-image: url((.+?));".+?href="(.+?)" title="Watch (.+?) Online For FREE".+?src="(.+?)"',re.DOTALL).findall(link)
        for url,name, iconimage in match:
                addDir(name,url,2,iconimage,'','1')
        addDir('[COLOR green]Next Page>>[/COLOR]',URL,10,'','1')

def MOVIES(url):
        addDir('[COLOR lightgreen]Search[/COLOR]','search',10,'','0')
        addDir('[COLOR yellow]Rated[/COLOR]','http://uflix.me/movie-tags/comedy/uflixrating',10,'','0')
        addDir('[COLOR yellow]IMDB Rated Movies[/COLOR]','http://uflix.me/movies/imdb_rating',10,'','0')
        addDir("[COLOR yellow]Genre's[/COLOR]",'url',7,'','0')
        addDir('[COLOR yellow]Popular[/COLOR]','http://uflix.me/movies/favorites',10,'','0')
        addDir('[COLOR yellow]Years[/COLOR]','http://uflix.me/movies/year',10,'','0')


def GENRE(url):
        addDir('[COLOR lightgreen]Search[/COLOR]','search',10,'','0')
        addDir('[COLOR yellow]Action[/COLOR]','http://uflix.me/movie-tags/action',10,'','0')
        addDir('[COLOR yellow]Adventure[/COLOR]','http://uflix.me/movie-tags/adventure',10,'','0')
        addDir('[COLOR yellow]Animation[/COLOR]','http://uflix.me/movie-tags/animation',10,'','0')
        addDir('[COLOR yellow]Biography[/COLOR]','http://uflix.me/movie-tags/biography',10,'','0')
        addDir('[COLOR yellow]Comedy[/COLOR]','http://uflix.me/movie-tags/comedy',10,'','0')
        addDir('[COLOR yellow]Crime[/COLOR]','http://uflix.me/movie-tags/crime',10,'','0')
        addDir('[COLOR yellow]Documentary[/COLOR]','http://uflix.me/movie-tags/documentary',10,'','0')
        addDir('[COLOR yellow]Drama[/COLOR]','http://uflix.me/movie-tags/drama',10,'','0')
        addDir('[COLOR yellow]Family[/COLOR]','http://uflix.me/movie-tags/family',10,'','0')
        addDir('[COLOR yellow]Fantasy[/COLOR]','http://uflix.me/movie-tags/fantasy',10,'','0')
        addDir('[COLOR yellow]History[/COLOR]','http://uflix.me/movie-tags/history',10,'','0')
        addDir('[COLOR yellow]Horror[/COLOR]','http://uflix.me/movie-tags/horror',10,'','0')
        addDir('[COLOR yellow]Music[/COLOR]','http://uflix.me/movie-tags/music',10,'','0')
        addDir('[COLOR yellow]Musical[/COLOR]','http://uflix.me/movie-tags/musical',10,'','0')
        addDir('[COLOR yellow]Mystery[/COLOR]','http://uflix.me/movie-tags/mystery',10,'','0')
        addDir('[COLOR yellow]Romance[/COLOR]','http://uflix.me/movie-tags/romance',10,'','0')
        addDir('[COLOR yellow]Sci-Fi[/COLOR]','http://uflix.me/movie-tags/sci-fi',10,'','0')
        addDir('[COLOR yellow]Sport[/COLOR]','http://uflix.me/movie-tags/sport',10,'','0')
        addDir('[COLOR yellow]Thriller[/COLOR]','http://uflix.me/movie-tags/thriller',10,'','0')
        addDir('[COLOR yellow]War[/COLOR]','http://uflix.me/movie-tags/war',10,'','0')
        addDir('[COLOR yellow]Western[/COLOR]','http://uflix.me/movie-tags/western',10,'','0')

def SHOWS(url):
        addDir('[COLOR lightgreen]Search[/COLOR]','search',10,'','0')
        addDir('[COLOR yellow]Action[/COLOR]','http://uflix.me/tv-tags/action',10,'','0')
        addDir('[COLOR yellow]Adventure[/COLOR]','http://uflix.me/tv-tags/adventure',10,'','0')
        addDir('[COLOR yellow]Animation[/COLOR]','http://uflix.me/tv-tags/animation',10,'','0')
        addDir('[COLOR yellow]Biography[/COLOR]','http://uflix.me/tv-tags/biography',10,'','0')
        addDir('[COLOR yellow]Comedy[/COLOR]','http://uflix.me/tv-tags/comedy',10,'','0')
        addDir('[COLOR yellow]Crime[/COLOR]','http://uflix.me/tv-tags/crime',10,'','0')
        addDir('[COLOR yellow]Documentary[/COLOR]','http://uflix.me/tv-tags/documentary',10,'','0')
        addDir('[COLOR yellow]Drama[/COLOR]','http://uflix.me/tv-tags/drama',10,'','0')
        addDir('[COLOR yellow]Family[/COLOR]','http://uflix.me/tv-tags/family',10,'','0')
        addDir('[COLOR yellow]Fantasy[/COLOR]','http://uflix.me/tv-tags/fantasy',10,'','0')
        addDir('[COLOR yellow]History[/COLOR]','http://uflix.me/tv-tags/history',10,'','0')
        addDir('[COLOR yellow]Horror[/COLOR]','http://uflix.me/tv-tags/horror',10,'','0')
        addDir('[COLOR yellow]Music[/COLOR]','http://uflix.me/tv-tags/music',10,'','0')
        addDir('[COLOR yellow]Musical[/COLOR]','http://uflix.me/tv-tags/musical',10,'','0')
        addDir('[COLOR yellow]Mystery[/COLOR]','http://uflix.me/tv-tags/mystery',10,'','0')
        addDir('[COLOR yellow]Romance[/COLOR]','http://uflix.me/tv-tags/romance',10,'','0')
        addDir('[COLOR yellow]Sci-Fi[/COLOR]','http://uflix.me/tv-tags/sci-fi',10,'','0')
        addDir('[COLOR yellow]Sport[/COLOR]','http://uflix.me/tv-tags/sport',10,'','0')
        addDir('[COLOR yellow]Thriller[/COLOR]','http://uflix.me/tv-tags/thriller',10,'','0')
        addDir('[COLOR yellow]War[/COLOR]','http://uflix.me/tv-tags/war',10,'','0')
        addDir('[COLOR yellow]Western[/COLOR]','http://uflix.me/tv-tags/western',10,'','0')
        
def _SEARCH_(url):
        URL=url
        link=OPEN_URL(url)
        match=re.compile('href="(.+?)" title="Watch (.+?) Online For FREE".+?src="(.+?)"',re.DOTALL).findall(link)
        for url,name, iconimage in match:
                addDir(name,url,2,iconimage,'','1')
        addDir('[COLOR green]Next Page>>[/COLOR]',URL,10,'','1')

def NXTPG(url,page):
        URL=url
        PAGE=int(page)+1
        if 'search' in url:
            link=SEARCH()
        else:
            NEW_URL=url +'/' +str(PAGE)
            link = OPEN_URL(NEW_URL)
        link = link.split('<figure class="col-sm-3 col-md-3')

        for p in link:
            try: 
                url = re.compile('<a href="(.+?)"',re.DOTALL).findall(p)[0]
                name = re.compile('title="Watch (.+?) Online.+?">.',re.DOTALL).findall(p)[0]
                iconimage = re.compile('src="(.+?)"',re.DOTALL).findall(p)[0]
                if '/show/' in url:
                    mode = 4
                else:
                    mode = 2
                addDir(name,url,mode,iconimage,str(PAGE))
            except:pass

        if not 'search' in URL:    
            addDir('[COLOR green]Next Page>>[/COLOR]',URL,10,'',str(PAGE))

def EPISODES(url):
        link=OPEN_URL(url)
        match=re.compile('title="watch (.+?) online free" class="link" href="(.+?)"').findall(link)
        for name,url in match:
                addDir(name,url,5,'','')

def EPISODELINKS(url,name):
        link=OPEN_URL(url)
        match=re.compile('<a alt=".+?" title=".+? on (.+?)" class="btn btn-primary" href="(.+?)"').findall(link)

        for name,url in match:
                addDir(name.split('.')[0].upper(),url,200,None,'')

def VIDEOLINKS(url,name):
        link=OPEN_URL(url)
        match=re.compile('title=".+? on (.+?)" href="(.+?)"').findall(link)

        for name,url in match:
                addDir(name.split('.')[0].upper(),url,200,None,'')

def SEARCH():
         search_entered =''
         keyboard = xbmc.Keyboard(search_entered, 'Search DubStop')
         keyboard.doModal()
         if keyboard.isConfirmed():
                 search_entered = keyboard.getText().replace(' ','+')
         if len(search_entered)>1:
                 url = 'http://uflix.me/index.php?menu=search&query='+ search_entered
         link = OPEN_URL(url)
         return link
         

def OPEN_URL(url):
        req = urllib2.Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
        response = urllib2.urlopen(req)
        link=response.read()
        response.close()
        return link

def PLAY_STREAM(name,url,iconimage):
        import urlresolver
        if 'flix.me/watch.php' in url:
            url=re.compile('url=(.+?)&').findall(url)[0]
            url=base64.b64decode(url)        
        url= urlresolver.resolve(url)
        liz = xbmcgui.ListItem(name, iconImage='DefaultVideo.png', thumbnailImage=iconimage)
        liz.setInfo(type='Video', infoLabels={'Title':name })
        liz.setProperty("IsPlayable","true")
        liz.setPath(url)
        xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, liz)

def SHOW_STREAM(name,url,iconimage):
        import urlresolver        
        url= urlresolver.resolve(url)
        import resolvers
        liz = xbmcgui.ListItem(name, iconImage='DefaultVideo.png', thumbnailImage=iconimage)
        liz.setInfo(type='Video', infoLabels={'Title':name })
        liz.setProperty("IsPlayable","true")
        liz.setPath(url)
        xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, liz)
        

                
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




def addLink(name,url,iconimage):
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name } )
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=url,listitem=liz)
        return ok


def addDir(name,url,mode,iconimage,page):
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&page="+urllib.quote_plus(page)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name, "Fanart":'http://uflix.me/themes/imdb250.jpg'})
        liz.setProperty('Fanart_Image','http://uflix.me/themes/imdb250.jpg')
        if not mode==200:
                
            ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
        else:
            liz.setProperty("IsPlayable","true")                
            ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=False)            
        return ok
        
              
params=get_params()
url=None
name=None
mode=None
page=None

try:
        url=urllib.unquote_plus(params["url"])
except:
        pass
try:
        name=urllib.unquote_plus(params["name"])
except:
        pass
try:
        mode=int(params["mode"])
except:
        pass

try:
        page=urllib.unquote_plus(params["page"])
except:
        pass

print "Mode: "+str(mode)
print "URL: "+str(url)
print "Name: "+str(name)

if mode==None or url==None or len(url)<1:
        print ""
        CATEGORIES()
       
elif mode==1:
        print ""+url
        INDEX(url)

elif mode==3:
        print ""+url
        MOVIES(url)
        
elif mode==11:
        print ""+url
        SEARCH()

elif mode==12:
        print ""+url
        _SEARCH_(url)

elif mode==10:
        print ""+url
        NXTPG(url,page)

elif mode==4:
        print ""+url
        EPISODES(url)

elif mode==6:
        print ""+url
        SHOWS(url)

elif mode==7:
        print ""+url
        GENRE(url)
        
elif mode==2:
        print ""+url
        VIDEOLINKS(url,name)

elif mode==5:
        print ""+url
        EPISODELINKS(url,name)

elif mode==200:
        PLAY_STREAM(name,url,'')

elif mode==201:
        SHOW_STREAM(name,url,'')
        

xbmcplugin.endOfDirectory(int(sys.argv[1]))
