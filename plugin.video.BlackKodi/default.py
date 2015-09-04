import xbmc, xbmcaddon, xbmcgui, xbmcplugin,os,shutil,urllib2,urllib,re,extract,downloader,time,socket
from t0mm0.common.net import Net as net

addon_id        = 'plugin.video.BlackKodi'
ADDON           = xbmcaddon.Addon(id=addon_id)
selfAddon       = xbmcaddon.Addon(id=addon_id)
datapath        = xbmc.translatePath(selfAddon.getAddonInfo('profile'))
icon            = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id, 'icon.png'))
user            = selfAddon.getSetting('bkusername')
passw           = selfAddon.getSetting('bkpassword')
cookie_file     = os.path.join(os.path.join(datapath,''), 'bk.lwp')

socket.setdefaulttimeout(60)
if user == '' or passw == '':
    if os.path.exists(cookie_file):
        try: os.remove(cookie_file)
        except: pass
    dialog = xbmcgui.Dialog()
    ret = dialog.yesno('Update Wizard 2.0', 'Please enter your assigned username and password','If you dont have these check your emails','Or contact support for further instructions','Cancel','Login')
    if ret == 1:
        keyb = xbmc.Keyboard('', 'Enter Username')
        keyb.doModal()
        if (keyb.isConfirmed()):
            search = keyb.getText()
            username=search
            keyb = xbmc.Keyboard('', 'Enter Password:')
            keyb.doModal()
            if (keyb.isConfirmed()):
                search = keyb.getText()
                password=search
                selfAddon.setSetting('bkusername',username)
                selfAddon.setSetting('bkpassword',password)
user = selfAddon.getSetting('bkusername')
passw = selfAddon.getSetting('bkpassword')

def CATEGORIES():
    setCookie('http://www.blackkodi.co.uk/amember/member')
    response = net().http_GET('http://www.blackkodi.co.uk/amember/member')
    if not 'Logged in as' in response.content:
        dialog = xbmcgui.Dialog()
        dialog.ok('Update Wizard 2.0', 'An error has ocurred logging in','Please check your details in addon settings','')
        quit()
    link = OPEN_URL('http://www.blackkodi.co.uk/amember/content/f/id/1/').replace('\n','').replace('\r','')
    print link
    match = re.compile('name="(.+?)".+?rl="(.+?)".+?mg="(.+?)".+?anart="(.+?)".+?escription="(.+?)"').findall(link)
    for name,url,iconimage,fanart,description in match:
        addDir(name,url,1,iconimage,fanart,description)
    setView('movies', 'MAIN')
         
def OPEN_URL(url):
    req = urllib2.Request(url)
    req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
    response = urllib2.urlopen(req)
    link=response.read()
    response.close()
    return link
        
def wizard(name,url,description):
    path = xbmc.translatePath(os.path.join('special://home/addons','packages'))
    dp = xbmcgui.DialogProgress()
    dp.create("Black Kodi Wizard","Downloading configuration files",'', 'Please Wait')
    lib=os.path.join(path, name+'.zip')
    try:
       os.remove(lib)
    except:
       pass
    downloader.download(url, lib, dp)
    addonfolder = xbmc.translatePath(os.path.join('special://','home'))
    time.sleep(2)
    dp.update(0,"", "Just a little while longer :)")
    extract.all(lib,addonfolder,dp)
    dialog = xbmcgui.Dialog()
    dialog.ok("Black Kodi Wizard", "Configuration files prepared", "[COLOR red]PLEASE DISCONNECT THE POWER FROM YOUR DEVICE[/COLOR]")

def setCookie(srDomain):
    html = net().http_GET(srDomain).content
    r = re.findall(r'<input type="hidden" name="(.+?)" value="(.+?)" />', html, re.I)
    post_data = {}
    post_data['amember_login'] = user
    post_data['amember_pass'] = passw
    for name, value in r:
        post_data[name] = value
    net().http_GET('http://www.blackkodi.co.uk/amember/member')
    net().http_POST('http://www.blackkodi.co.uk/amember/member',post_data)
    net().save_cookies(cookie_file)
    net().set_cookies(cookie_file)

def addDir(name,url,mode,iconimage,fanart,description=''):
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&description="+str(description)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name, 'plot': description } )
        liz.setProperty('fanart_image', fanart)
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=False)
        return ok
    
def setView(content, viewType):
    if content:
        xbmcplugin.setContent(int(sys.argv[1]), content)
    if ADDON.getSetting('auto-view')=='true':
        xbmc.executebuiltin("Container.SetViewMode(%s)" % ADDON.getSetting(viewType) )
        
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
                            
params=get_params();url=None;name=None;mode=None;iconimage=None;description=None
try:url=urllib.unquote_plus(params["url"])
except:pass
try:name=urllib.unquote_plus(params["name"])
except:pass
try:iconimage=urllib.unquote_plus(params["iconimage"])
except:pass
try:mode=int(params["mode"])
except:pass
try:description=urllib.unquote_plus(params["description"])
except:pass

if mode==None or url==None or len(url)<1:CATEGORIES()
elif mode==1:wizard(name,url,description)
xbmcplugin.endOfDirectory(int(sys.argv[1]))

