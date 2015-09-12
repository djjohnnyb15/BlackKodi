import urllib, urllib2, sys, re, xbmcplugin, xbmcgui, xbmcaddon, xbmc, os, base64


addon_id = ('plugin.video.vdubt')





ADDON = xbmcaddon.Addon(id='plugin.video.alltv')

ooOOOoo = ''
def ttTTtt(i, t1, t2=[]):
 t = ooOOOoo
 for c in t1:
  t += chr(c)
  i += 1
  if i > 1:
   t = t[:-1]
   i = 0  
 for c in t2:
  t += chr(c)
  i += 1
  if i > 1:
   t = t[:-1]
   i = 0
 return t



def CATEGORIES():
    
    response=OPEN_URL('http://www.demludi.com/Apps/AllTv/Playlist/AllTv.m3u')
    
    match=re.compile('#EXTINF:-1,(.+?)\n(.+?)\n').findall (response)
    for name , url in match:
        if '#' in name:
            iconimage=name.split('#IMG:')[1]
            name=name.split('#')[0]

        else:
            name=name
            iconimage=''        

        addDir(name.title(),url,200,iconimage,'')
    xbmcplugin.addSortMethod(int(sys.argv[1]), xbmcplugin.SORT_METHOD_VIDEO_TITLE)        
            
            
    setView('movies', 'default') 
       
       

       
    
               
 
def OPEN_URL(url):
    req = urllib2.Request(url)
    req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
    response = urllib2.urlopen(req)
    link=response.read()
    response.close()
    return link
    
    
    
def PLAY_STREAM(name,url,iconimage):
  
    if '.f4m' in url:
        import F4MProxy
        player=F4MProxy.f4mProxyHelper()
        player.playF4mLink(url, name)
        
    else:    
        liz = xbmcgui.ListItem(name, iconImage='DefaultVideo.png', thumbnailImage=iconimage)
        liz.setInfo(type='Video', infoLabels={'Title':name})
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

def addDir(name,url,mode,iconimage,description):
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&iconimage="+urllib.quote_plus(iconimage)+"&description="+urllib.quote_plus(description)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name, "Plot": description} )
        menu = []
        if mode ==200:
            if not '.f4m' in url:  
                liz.setProperty("IsPlayable","true")
            
            ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=False)
        else:
            
            xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
        return ok
        


def sawlive(embedcode, ref_url):
    url = re.search("<script type='text/javascript'> swidth='[0-9%]+', sheight='[0-9%]+';</script><script type='text/javascript' src='(.+?)'></script>", embedcode, re.DOTALL).group(1)
    ref_data = {'Referer': ref_url}

    try:
        ## Current SawLive resolving technique - always try to fix first
        html = net.http_GET(url,ref_data).content
        get_url(url, ref_data)
        link = re.search('src="(http://sawlive.tv/embed/watch/[A-Za-z0-9_/]+)">', html).group(1)
        addon.log(link)

    except Exception, e:
        ## Use if first section does not work - last resort which returns compiled javascript
        addon.log('SawLive resolving failed, attempting jsunpack.jeek.org, msg: %s' % e)
        Notify('small','SawLive', 'Resolve Failed. Using jsunpack','')
        
        jsunpackurl = 'http://jsunpack.jeek.org'
        data = {'urlin': url}
        html = get_url(jsunpackurl, data=data)
        link = re.search('src="(http://sawlive.tv/embed/watch/[A-Za-z0-9]+[/][A-Za-z0-9_]+)"',html).group(1)
        addon.log(link)

    html = get_url(link, headers=ref_data)
    
    swfPlayer = re.search('SWFObject\(\'(.+?)\'', html).group(1)
    playPath = re.search('\'file\', \'(.+?)\'', html).group(1)
    streamer = re.search('\'streamer\', \'(.+?)\'', html).group(1)
    appUrl = re.search('rtmp[e]*://.+?/(.+?)\'', html).group(1)
    rtmpUrl = ''.join([streamer,
       ' playpath=', playPath,
       ' app=', appUrl,
       ' pageURL=', url,
       ' swfUrl=', swfPlayer,
       ' live=true'
       ' timeout=15'])
    addon.log(rtmpUrl)
    return rtmpUrl

def streamlive(embedcode):
    
    channel = re.compile('embed/(.+?)&').findall (embedcode)[0]

    headers = {
            'Referer': 'http://www.streamlive.to/',
            'Host': 'www.streamlive.to',
            'Origin': 'www.streamlive.to'
        }
    
    if channel:
        #url = 'http://www.streamlive.to/embedplayer.php?channel=%s' % channel.group(1)
        url = 'http://www.streamlive.to/embedplayer.php?channel=%s' % channel
        html = get_url(url, headers=headers)
        
        token_url=re.compile('''.*getJSON\("([^'"]+)".*''').findall(html)[0]
        if not token_url.startswith('http'):
            token_url = 'http:' + token_url
            
        token_html = get_url(token_url, headers=headers)
        token=re.compile('{"token":"(.+?)"}').findall(token_html)[0]
        
        filename = re.search('file: "([^&]+).flv"', html).group(1)
        rtmp = re.search('streamer: "(.+?)",', html).group(1)
        rtmp = rtmp.replace("\\", "")
        app = re.search('rtmp://[\.\w:]*/([^\s]+)', rtmp).group(1)
    else:
        filename = re.search('streamer=rtmp://live.streamlive.to/edge&file=(.+?)&autostart=true&controlbar=bottom"', embedcode).group(1)
        url = 'http://www.streamlive.to/embedplayer.php'

    swf = 'http://player.streamlive.to/streamlive-plugin.swf'
    return rtmp + ' playPath=' + filename + ' swfUrl=' + swf + ' swfVfy=true live=true token=' + token + ' app=' + app + ' pageUrl=' + url

 
        
def setView(content, viewType):
        if content:
                xbmcplugin.setContent(int(sys.argv[1]), content)
        if ADDON.getSetting('auto-view') == 'true':#<<<----see here if auto-view is enabled(true) 
                xbmc.executebuiltin("Container.SetViewMode(%s)" % ADDON.getSetting(viewType) )#<<<-----then get the view type
                      
               
params=get_params()
url=None
name=None
mode=None
iconimage=None
description=None


try:
        url=urllib.unquote_plus(params["url"])
except:
        pass
try:
        name=urllib.unquote_plus(params["name"])
except:
        pass
try:
        iconimage=urllib.unquote_plus(params["iconimage"])
except:
        pass
try:        
        mode=int(params["mode"])
except:
        pass
try:        
        description=urllib.unquote_plus(params["description"])
except:
        pass

print "Mode: "+str(mode)
print "URL: "+str(url)
print "Name: "+str(name)
print "IconImage: "+str(iconimage)
   
        
#these are the modes which tells the plugin where to go
if mode==None or url==None or len(url)<1:
        print ""
        CATEGORIES()
       
elif mode==1:
        print ""+url
        GetContent(url)
        
elif mode==200:

        PLAY_STREAM(name,url,iconimage)

elif mode==20:

        sawlive(name,url)

elif mode==21:

        streamlive(name,url)
        
elif mode==2001:

        playall(name,url)        
       
xbmcplugin.endOfDirectory(int(sys.argv[1]))
