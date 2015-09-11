import urllib,urllib2,sys,re,xbmcplugin,xbmcgui,xbmcaddon,xbmc
import urlresolver, os
from t0mm0.common.net import Net
import datetime
import time

ADDON = xbmcaddon.Addon(id='plugin.video.dailyflix')
net = Net()
img = ''

PATH = "dailyflix"       
VERSION = "1.40"

icon = 'http://board.dailyflix.net/public/style_images/5_1_DF05.png'
divxicon = 'http://icons.iconarchive.com/icons/deleket/folder/256/Divx-Movies-icon.png'
hdicon = 'http://icons.iconarchive.com/icons/deleket/folder/256/My-Videos-icon.png'
flashicon = 'http://icons.iconarchive.com/icons/deleket/folder/256/Macromedia-Flash-icon.png'
searchicon = 'http://icons.iconarchive.com/icons/iconleak/atrous/256/search-icon.png'
imdbicon = 'http://www.glitterazi.com/wp-content/uploads/2012/11/imdb-e1352114214951.jpeg'


#      addDir('name','url','mode','iconimage','description') mode is where it tells the plugin where to go scroll to bottom to see where mode is
def CATEGORIES():
        addDir('HD Movies','structure_HD_movies',4,hdicon,'HD Movies')
        addDir('DivX Movies','structure_divx_movies',3,divxicon,'DivX Movies')
        addDir('Flash Movies','structure_flash_movies',6,flashicon,'Flash Movies')
        addDir('MicroHD Movies','structure_microhd_movies',33,icon,'MicroHD Movies')
        addDir('MKV/MP4 (H264)','structure_mkv',34,icon,'MKV/MP4 (H264)')
        addDir('Pre-Retail','structure_preretail',16,icon,'Pre-Retail')
        addDir('Foreign Movies','foreignmovies',19,icon,'Foreign Movies')
        addDir('Search','structure_search(url)',10,searchicon,'Search')
        addDir('TV Shows','tv_shows()',17,icon,'TV Shows')
        addSpecial('[COLOR yellow]Resolver Settings[/COLOR]','www.nonsense.com',69,'')
        #addDir('Resolver Test','test_resolve',15,'','Test_Resolver')
        setView('movies', 'default')
        #setView is setting the automatic view.....first is what section "movies"......second is what you called it in the settings xml

class TextBox:
    WINDOW = 10147
    CONTROL_LABEL = 1
    CONTROL_TEXTBOX = 5

    def __init__(self, *args, **kwargs):
        xbmc.executebuiltin( "ActivateWindow(%d)" % (self.WINDOW))
        self.win = xbmcgui.Window(self.WINDOW)
        self.setControls()


    def setControls( self ):
        link=OPEN_URL(url)
        title = re.findall('<title>(.+?) - IMDb</title>', link)
        rating = re.findall('title="(.+?) - click stars to rate"', link)
        description = re.findall('<div class="inline canwrap" itemprop="description">.+?<p>(.+?)<em class="nobr">', link, re.DOTALL)
        if not description:
            description = re.findall('<div class="inline canwrap" itemprop="description">.+?<p>(.+?)</p>', link, re.DOTALL)
        #trailer = re.findall('<a href="(.+?)" class="video-colorbox" data-context="imdb" data-video="vi1168877337" itemprop="trailer">', link)
        #if not trailer:
        #    trailer = ''
        text = title[0]+'\n\n'+rating[0]+'\n'+description[0]
        self.win.getControl(self.CONTROL_TEXTBOX).setText(text)

def test_resolve():
        keyboard = xbmc.Keyboard('http://180upload.com/zu245lp07707')
        keyboard.doModal()
        url = keyboard.getText()
        name = 'test'
        PLAY(name,url)
        
def imdb(url):
    popup = TextBox()
                
def nextdirectory(url):
        link=OPEN_URL(url)
        match=re.compile("<link rel='((?=(?:prev|first)).+?)' href='(.+?)'").findall(link) #prev/next page
        if match:
            for name, url in match:
                addDir('[B]'+name+'[/B]',url,1,'','')
        match=re.compile('href="((?!(?:.+imdb|.+facebook|.+imgur|.+postimage|.+nfomation|.+h264|.+microhd|.+no\-dvd\-rips\-here\-please\-read|.+pre\-retail\-mkv\-mp4\-h264\-topic\-guidelines)).+?)" title=\'(.+?) - started').findall(link)
        for url, name in match:
                addDir(name,url,2,'','')
        match=re.compile("<link rel='((?=(?:next|last)).+?)' href='(.+?)'").findall(link) #prev/next page
        if match:
            for name, url in match:
                addDir('[B]'+name+'[/B]',url,1,'','')

def nextdirectorytv(url):
        link=OPEN_URL(url)
        match=re.compile("<link rel='((?=(?:prev|first)).+?)' href='(.+?)'").findall(link) #prev/next page
        if match:
            for name, url in match:
                addDir('[B]'+name+'[/B]',url,14,'','')
        match=re.compile('href="((?!(?:.+imdb|.+facebook|.+imgur|.+postimage|.+nfomation)).+?)" title=\'((?!(?:Please Read Before Posting Any New Topics or Posts in the TV Forums)).+?) - started').findall(link)
        for url, name in match:
                addDir(name,url,12,'','')
        match=re.compile("<link rel='((?=(?:next|last)).+?)' href='(.+?)'").findall(link) #prev/next page
        if match:
            for name, url in match:
                addDir('[B]'+name+'[/B]',url,14,'','')

   
def nextdirectory_nextdirectory(url): #links
        link=OPEN_URL(url)
        match=re.compile("<link rel='((?=(?:prev|first)).+?)' href='(.+?)'").findall(link) #prev/next page
        if match:
            for name, url in match:
                addDir('[B]'+name+'[/B]',url,2,'','')
        cover=re.compile("img src='(.+?)' alt='Posted Image' class='bbc_img'>").findall(link)
        if not cover:
            cover=re.compile("img class='bbc_img' src=(?:\"|\')(.+?)(?:\"|\') alt=(?:\"|\').+?(?:\"|\')").findall(link)
            if not cover:
                cover = ['']
        imdbz=re.compile("a href='(http://www.imdb.com/.+?)' class='bbc_url'").findall(link)
        if imdbz:
            imdbz = imdbz[0].replace('/reference', '')
            addClick('[COLOR yellow]IMDB Info[/COLOR]',imdbz,18,imdbicon,'')
        match=re.compile('''<a href='((?:(?!imdb|facebook|imgur|postimage|filestube|nfomation|leetleech|paste2|wikipedia|fromMemberID|nfomation|dailyflix.net/|imageshack).)+?)' class='bbc_url' title='External link' rel='external'>''').findall(link)
        match.reverse()
        for url in match:
            name = re.findall('http://w?w?w?\.?(.+?)\..+?', url)
            for name in name:
                addDir(name,url,5,cover[0],'')
        match=re.compile("<link rel='((?=(?:next|last)).+?)' href='(.+?)'").findall(link) #prev/next page
        if match:
            for name, url in match:
                addDir('[B]'+name+'[/B]',url,2,'','')

def structure_searchTC(name):
        url = OPEN_URL('http://board.dailyflix.net/index.php')
        go = 'search'
        name = name.replace(' ','%20')
        source = 'http://board.dailyflix.net/index.php?app=core&module=search&do=search&search_term='+name
        linkz=OPEN_URL(source)
        match=re.compile("<link rel='((?=(?:prev|first)).+?)' href='(.+?)'").findall(linkz) #prev/next page
        if match:
            for name, url in match:
                addDir(''+name+'',url,11,'','')
        results = re.compile("data-tooltip=\".+?\">((?!(?:mHD))\b|Flash|HD|DivX|DivX TV|HD TV|Flash TV|\b)</a>.+?<h4><a href='(.+?)' title='View result'>(.+?)</a></h4>", re.DOTALL).findall(linkz)
        for name, url, description in results:
            if "TV" in name:
                addDir(description+' '+name,url,12,searchicon,'')
            else:
                addDir(description+' '+name,url,2,searchicon,'')
        match=re.compile("<link rel='((?=(?:next|last)).+?)' href='(.+?)'").findall(linkz) #prev/next page
        if match:
            for name, url in match:
                addDir(''+name+'',url,11,'','')

            else:
                print 'FAILED SEARCH'

def structure_search(url):
        url = OPEN_URL('http://board.dailyflix.net/index.php')
        go = 'search'
        keyboard = xbmc.Keyboard('')
        keyboard.doModal()
        if keyboard.isConfirmed():
            search = keyboard.getText()
            search = search.replace(' ','%20')
            source = 'http://board.dailyflix.net/index.php?app=core&module=search&do=search&search_term='+search
            linkz=OPEN_URL(source)
            match=re.compile("<link rel='((?=(?:prev|first)).+?)' href='(.+?)'").findall(linkz) #prev/next page
            if match:
                for name, url in match:
                    addDir('[B]'+name+'[/B]',url,11,'','')
            results = re.compile("data-tooltip=\".+?\">((?!(?:mHD))\b|Flash|HD|DivX|DivX TV|HD TV|Flash TV|\b)</a>.+?<h4><a href='(.+?)' title='View result'>(.+?)</a></h4>", re.DOTALL).findall(linkz)
            for name, url, description in results:
                if "TV" in name:
                    addDir(description+' '+name,url,12,searchicon,'')
                else:
                    addDir(description+' '+name,url,2,searchicon,'')
            match=re.compile("<link rel='((?=(?:next|last)).+?)' href='(.+?)'").findall(linkz) #prev/next page
            if match:
                for name, url in match:
                    addDir('[B]'+name+'[/B]',url,11,'','')

        else:
            print 'FAILED SEARCH'

def structure_searchpages(url):
        url = url.replace('amp;','')
        link=OPEN_URL(url)
        match=re.compile("<link rel='((?=(?:prev|first)).+?)' href='(.+?)'").findall(link) #prev/next page
        if match:
            for name, url in match:
                addDir('[B]'+name+'[/B]',url,11,'','')
        results = re.compile("data-tooltip=\".+?\">((?!(?:mHD))\b|Flash|HD|DivX|DivX TV|HD TV|Flash TV|\b)</a>.+?<h4><a href='(.+?)' title='View result'>(.+?)</a></h4>", re.DOTALL).findall(link)
        for name, url, description in results:
                if "TV" in name:
                    addDir(description+' '+name,url,12,searchicon,'')
                else:
                    addDir(description+' '+name,url,2,searchicon,'')
        match=re.compile("<link rel='((?=(?:next|last)).+?)' href='(.+?)'").findall(link) #prev/next page
        if match:
            for name, url in match:
                addDir('[B]'+name+'[/B]',url,11,'','')

def structure_seasons(url):
        link=OPEN_URL(url)
        match=re.compile("<link rel='((?=(?:prev|first)).+?)' href='(.+?)'").findall(link) #prev/next page
        if match:
            for name, urlz in match:
                addDir('[B]'+name+'[/B]',urlz,12,'','')
        imdbz=re.compile("a href='(http://www.imdb.com/.+?)' class='bbc_url'").findall(link)
        if imdbz:
            imdbz = imdbz[0].replace('/reference', '')
            addClick('[COLOR yellow]IMDB Info[/COLOR]',imdbz,18,imdbicon,'')
        seasonone=re.compile('\.([sS]01|1)([eE][0-9][0-9])\.(...............)').findall(link)
        seasontwo=re.compile('\.([sS]02|2)([eE][0-9][0-9])\.(...............)').findall(link)
        seasonthree=re.compile('\.([sS]03|3)([eE][0-9][0-9])\.(...............)').findall(link)
        seasonfour=re.compile('\.([sS]04|4)([eE][0-9][0-9])\.(...............)').findall(link)
        seasonfive=re.compile('\.([sS]05|5)([eE][0-9][0-9])\.(...............)').findall(link)
        seasonsix=re.compile('\.([sS]06|6)([eE][0-9][0-9])\.(...............)').findall(link)
        seasonseven=re.compile('\.([sS]07|7)([eE][0-9][0-9])\.(...............)').findall(link)
        seasoneight=re.compile('\.([sS]08|8)([eE][0-9][0-9])\.(...............)').findall(link)
        seasonnine=re.compile('\.([sS]09|9)([eE][0-9][0-9])\.(...............)').findall(link)
        seasonten=re.compile('\.([sS]10)([eE][0-9][0-9])\.(...............)').findall(link)
        seasoneleven=re.compile('\.([sS]11)([eE][0-9][0-9])\.(...............)').findall(link)
        seasontwelve=re.compile('\.([sS]12)([eE][0-9][0-9])\.(...............)').findall(link)
        seasonthirteen=re.compile('\.([sS]13)([eE][0-9][0-9])\.(...............)').findall(link)
        seasonfourteen=re.compile('\.([sS]14)([eE][0-9][0-9])\.(...............)').findall(link)
        seasonfifteen=re.compile('\.([sS]15)([eE][0-9][0-9])\.(...............)').findall(link)
        seasonsixteen=re.compile('\.([sS]16)([eE][0-9][0-9])\.(...............)').findall(link)
        seasonseventeen=re.compile('\.([sS]17)([eE][0-9][0-9])\.(...............)').findall(link)
        seasoneighteen=re.compile('\.([sS]18)([eE][0-9][0-9])\.(...............)').findall(link)
        seasonnineteen=re.compile('\.([sS]19)([eE][0-9][0-9])\.(...............)').findall(link)
        seasontwenty=re.compile('\.([sS]20)([eE][0-9][0-9])\.(...............)').findall(link)
        seasontwentyone=re.compile('\.([sS]21)([eE][0-9][0-9])\.(...............)').findall(link)
        seasontwentytwo=re.compile('\.([sS]22)([eE][0-9][0-9])\.(...............)').findall(link)
        seasontwentythree=re.compile('\.([sS]23)([eE][0-9][0-9])\.(...............)').findall(link)
        seasontwentyfour=re.compile('\.([sS]24)([eE][0-9][0-9])\.(...............)').findall(link)
        cover=re.compile("img src='(.+?)' alt='Posted Image' class='bbc_img'>").findall(link)
        if not cover:
            cover=re.compile("img class='bbc_img' src=(?:\"|\')(.+?)(?:\"|\') alt=(?:\"|\').+?(?:\"|\')").findall(link)
            if not cover:
                cover = ['']
        pic=cover[0]
        
        if seasonone:
                seasonone.sort()
                for season, episode, tail in seasonone:
                    addDir(season+' '+episode,url,13,pic,season+episode+'.'+tail)

        if seasontwo:
                seasontwo.sort()
                for season, episode, tail in seasontwo:
                    addDir(season+' '+episode,url,13,pic,season+episode+'.'+tail)

        if seasonthree:
                seasonthree.sort()
                for season, episode, tail in seasonthree:
                    addDir(season+' '+episode,url,13,pic,season+episode+'.'+tail)

        if seasonfour:
                seasonfour.sort()
                for season, episode, tail in seasonfour:
                    addDir(season+' '+episode,url,13,pic,season+episode+'.'+tail)

        if seasonfive:
                seasonfive.sort()
                for season, episode, tail in seasonfive:
                    addDir(season+' '+episode,url,13,pic,season+episode+'.'+tail)

        if seasonsix:
                seasonsix.sort()
                for season, episode, tail in seasonsix:
                    addDir(season+' '+episode,url,13,pic,season+episode+'.'+tail)

        if seasonseven:
                seasonseven.sort()
                for season, episode, tail in seasonseven:
                    addDir(season+' '+episode,url,13,pic,season+episode+'.'+tail)

        if seasoneight:
                seasoneight.sort()
                for season, episode, tail in seasoneight:
                    addDir(season+' '+episode,url,13,pic,season+episode+'.'+tail)

        if seasonnine:
                seasonnine.sort()
                for season, episode, tail in seasoneight:
                    addDir(season+' '+episode,url,13,pic,season+episode+'.'+tail)

        if seasonten:
                seasonten.sort()
                for season, episode, tail in seasoneight:
                    addDir(season+' '+episode,url,13,pic,season+episode+'.'+tail)

        if seasoneleven:
                seasoneleven.sort()
                for season, episode, tail in seasoneight:
                    addDir(season+' '+episode,url,13,pic,season+episode+'.'+tail)

        if seasontwelve:
                seasontwelve.sort()
                for season, episode, tail in seasoneight:
                    addDir(season+' '+episode,url,13,pic,season+episode+'.'+tail)

        if seasonthirteen:
                seasonthirteen.sort()
                for season, episode, tail in seasoneight:
                    addDir(season+' '+episode,url,13,pic,season+episode+'.'+tail)

        if seasonfourteen:
                seasonfourteen.sort()
                for season, episode, tail in seasoneight:
                    addDir(season+' '+episode,url,13,pic,season+episode+'.'+tail)

        if seasonfifteen:
                seasonfifteen.sort()
                for season, episode, tail in seasoneight:
                    addDir(season+' '+episode,url,13,pic,season+episode+'.'+tail)

        if seasonsixteen:
                seasonsixteen.sort()
                for season, episode, tail in seasoneight:
                    addDir(season+' '+episode,url,13,pic,season+episode+'.'+tail)

        if seasonseventeen:
                seasonseventeen.sort()
                for season, episode, tail in seasoneight:
                    addDir(season+' '+episode,url,13,pic,season+episode+'.'+tail)

        if seasoneighteen:
                seasoneighteen.sort()
                for season, episode, tail in seasoneight:
                    addDir(season+' '+episode,url,13,pic,season+episode+'.'+tail)

        if seasonnineteen:
                seasonnineteen.sort()
                for season, episode, tail in seasoneight:
                    addDir(season+' '+episode,url,13,pic,season+episode+'.'+tail)

        if seasontwenty:
                seasontwenty.sort()
                for season, episode, tail in seasoneight:
                    addDir(season+' '+episode,url,13,pic,season+episode+'.'+tail)

        if seasontwentyone:
                seasontwentyone.sort()
                for season, episode, tail in seasoneight:
                    addDir(season+' '+episode,url,13,pic,season+episode+'.'+tail)

        if seasontwentytwo:
                seasontwentytwo.sort()
                for season, episode, tail in seasoneight:
                    addDir(season+' '+episode,url,13,pic,season+episode+'.'+tail)

        if seasontwentythree:
                seasontwentythree.sort()
                for season, episode, tail in seasoneight:
                    addDir(season+' '+episode,url,13,pic,season+episode+'.'+tail)

        if seasontwentyfour:
                seasontwentyfour.sort()
                for season, episode, tail in seasoneight:
                    addDir(season+' '+episode,url,13,pic,season+episode+'.'+tail)

        match=re.compile("<link rel='((?=(?:next|last)).+?)' href='(.+?)'").findall(link) #prev/next page
        if match:
            for name, urlz in match:
                addDir('[B]'+name+'[/B]',urlz,12,'','')

def structure_episodesone(url):
        link=OPEN_URL(url)
        episodes=re.compile(description+"(.+?)((</div>|</a><br />.<br />))",re.DOTALL).findall(link)
        links=re.compile("<a href='((?:(?!imdb|facebook|imgur|postimage|filestube|nfomation|leetleech|paste2|wikipedia|fromMemberID|nfomation|dailyflix.net/|imageshack).)+?)' class='bbc_url' title='External link' rel='external'>").findall(str(episodes))
        links.reverse()
        for url in links:
            name = re.findall('http://w?w?w?\.?(.+?)\..+?', url)
            for name in name:
                addDir(name,url,5,'','')
        

def structure_divx_movies():
        addDir('Movies 2014-2015        A-Z','http://board.dailyflix.net/index.php?/forum/422-divx-2014-2015/?sort_key=title&sort_by=A-Z',1,icon,'DivX Movies 2014 - A-Z')
        addDir('Movies 2012-2013        A-Z','http://board.dailyflix.net/index.php?/forum/49-divx-2012-2013/?sort_key=title&sort_by=A-Z',1,icon,'DivX Movies 2012-2013 - A-Z')
        addDir('Movies 2006-2011        A-Z','http://board.dailyflix.net/index.php?/forum/50-divx-2006-2011/?sort_key=title&sort_by=A-Z',1,icon,'DivX Movies 2006-2011 - A-Z')
        addDir('Movies 2000-2005        A-Z','http://board.dailyflix.net/index.php?/forum/52-divx-2000-2005/?sort_key=title&sort_by=A-Z',1,icon,'DivX Movies 2000-2005 - A-Z')
        addDir('Movies 1990-1999        A-Z','http://board.dailyflix.net/index.php?/forum/55-divx-1990-1999/?sort_key=title&sort_by=A-Z',1,icon,'DivX Movies 1990-1999 - A-Z')
        addDir('Movies 1980-1989        A-Z','http://board.dailyflix.net/index.php?/forum/56-divx-1980-1989/?sort_key=title&sort_by=A-Z',1,icon,'DivX Movies 1980-1999 - A-Z')
        addDir('Movies Pre 1979             A-Z','http://board.dailyflix.net/index.php?/forum/57-divx-1979-earlier/?sort_key=title&sort_by=A-Z',1,icon,'DivX Movies Pre 1979  - A-Z')
        addDir('Movies 2014-2015        Recently Added','http://board.dailyflix.net/index.php?/forum/422-divx-2014-2015/?sort_key=last_post&sort_by=Z-A',1,icon,'DivX Movies 2014 - Recently Added')
        addDir('Movies 2012-2013        Recently Added','http://board.dailyflix.net/index.php?/forum/49-divx-2012-2013/?sort_key=last_post&sort_by=Z-A',1,icon,'DivX Movies 2012-2013 - Recently Added')
        addDir('Movies 2006-2011        Recently Added','http://board.dailyflix.net/index.php?/forum/50-divx-2006-2011/?sort_key=last_post&sort_by=Z-A',1,icon,'DivX Movies 2006-2011 - Recently Added')
        addDir('Movies 2000-2005        Recently Added','http://board.dailyflix.net/index.php?/forum/52-divx-2000-2005/?sort_key=last_post&sort_by=Z-A',1,icon,'DivX Movies 2000-2005 - Recently Added')
        addDir('Movies 1990-1999        Recently Added','http://board.dailyflix.net/index.php?/forum/55-divx-1990-1999/?sort_key=last_post&sort_by=Z-A',1,icon,'DivX Movies 1990-1999 - Recently Added')
        addDir('Movies 1980-1989        Recently Added','http://board.dailyflix.net/index.php?/forum/56-divx-1980-1989/?sort_key=last_post&sort_by=Z-A',1,icon,'DivX Movies 1980-1999 - Recently Added')
        addDir('Movies Pre 1979             Recently Added','http://board.dailyflix.net/index.php?/forum/57-divx-1979-earlier/?sort_key=last_post&sort_by=Z-A',1,icon,'DivX Movies Pre 1979  - Recently Added')        

def structure_mkv():
        addDir('Movies 2014-2015        A-Z','http://board.dailyflix.net/index.php?/forum/425-mkv-mp4-h264-2014-2015/?sort_key=title&sort_by=A-Z',1,icon,'MKV/MP4 (H264) Movies 2014 - A-Z')
        addDir('Movies 2012-2013        A-Z','http://board.dailyflix.net/index.php?/forum/270-mkv-mp4-h264-2012-2013/?sort_key=title&sort_by=A-Z',1,icon,'MKV/MP4 (H264) Movies 2012-2013 - A-Z')
        addDir('Movies 2006-2011        A-Z','http://board.dailyflix.net/index.php?/forum/271-mkv-mp4-h264-2006-2011/?sort_key=title&sort_by=A-Z',1,icon,'MKV/MP4 (H264) Movies 2006-2011 - A-Z')
        addDir('Movies 2000-2005        A-Z','http://board.dailyflix.net/index.php?/forum/272-mkv-mp4-h264-2000-2005/?sort_key=title&sort_by=A-Z',1,icon,'MKV/MP4 (H264) Movies 2000-2005 - A-Z')
        addDir('Movies 1990-1999        A-Z','http://board.dailyflix.net/index.php?/forum/273-mkv-mp4-h264-1990-1999/?sort_key=title&sort_by=A-Z',1,icon,'MKV/MP4 (H264) Movies 1990-1999 - A-Z')
        addDir('Movies 1980-1989        A-Z','http://board.dailyflix.net/index.php?/forum/274-mkv-mp4-h264-1980-1989/?sort_key=title&sort_by=A-Z',1,icon,'MKV/MP4 (H264) Movies 1980-1999 - A-Z')
        addDir('Movies Pre 1979             A-Z','http://board.dailyflix.net/index.php?/forum/275-mkv-mp4-h264-1979-earlier/?sort_key=title&sort_by=A-Z',1,icon,'MKV/MP4 (H264) Movies Pre 1979  - A-Z')
        addDir('Movies 2014-2015        Recently Added','http://board.dailyflix.net/index.php?/forum/425-mkv-mp4-h264-2014-2015/?sort_key=last_post&sort_by=Z-A',1,icon,'MKV/MP4 (H264) Movies 2014 - Recently Added')
        addDir('Movies 2012-2013        Recently Added','http://board.dailyflix.net/index.php?/forum/270-mkv-mp4-h264-2012-2013/?sort_key=last_post&sort_by=Z-A',1,icon,'MKV/MP4 (H264) Movies 2012-2013 - Recently Added')
        addDir('Movies 2006-2011        Recently Added','http://board.dailyflix.net/index.php?/forum/271-mkv-mp4-h264-2006-2011/?sort_key=last_post&sort_by=Z-A',1,icon,'MKV/MP4 (H264) Movies 2006-2011 - Recently Added')
        addDir('Movies 2000-2005        Recently Added','http://board.dailyflix.net/index.php?/forum/272-mkv-mp4-h264-2000-2005/?sort_key=last_post&sort_by=Z-A',1,icon,'MKV/MP4 (H264) Movies 2000-2005 - Recently Added')
        addDir('Movies 1990-1999        Recently Added','http://board.dailyflix.net/index.php?/forum/273-mkv-mp4-h264-1990-1999/?sort_key=last_post&sort_by=Z-A',1,icon,'MKV/MP4 (H264) Movies 1990-1999 - Recently Added')
        addDir('Movies 1980-1989        Recently Added','http://board.dailyflix.net/index.php?/forum/274-mkv-mp4-h264-1980-1989/?sort_key=last_post&sort_by=Z-A',1,icon,'MKV/MP4 (H264) Movies 1980-1999 - Recently Added')
        addDir('Movies Pre 1979             Recently Added','http://board.dailyflix.net/index.php?/forum/275-mkv-mp4-h264-1979-earlier/?sort_key=last_post&sort_by=Z-A',1,icon,'MKV/MP4 (H264) Movies Pre 1979  - Recently Added')        

def structure_HD_movies():
        addDir('Movies 2014-2015        A-Z','http://board.dailyflix.net/index.php?/forum/423-hd-movies-2014-2015/?sort_key=title&sort_by=A-Z',1,icon,'HD Movies 2014 - A-Z')
        addDir('Movies 2012-2013        A-Z','http://board.dailyflix.net/index.php?/forum/196-hd-movies-2012-2013/?sort_key=title&sort_by=A-Z',1,icon,'HD Movies 2012-2013 - A-Z')
        addDir('Movies 2006-2011        A-Z','http://board.dailyflix.net/index.php?/forum/197-hd-movies-2006-2011/?sort_key=title&sort_by=A-Z',1,icon,'HD Movies 2006-2011 - A-Z')
        addDir('Movies 2000-2005        A-Z','http://board.dailyflix.net/index.php?/forum/199-hd-movies-2000-2005/?sort_key=title&sort_by=A-Z',1,icon,'HD Movies 2000-2005 - A-Z')
        addDir('Movies 1990-1999        A-Z','http://board.dailyflix.net/index.php?/forum/202-hd-movies-1990-1999/?sort_key=title&sort_by=A-Z',1,icon,'HD Movies 1990-1999 - A-Z')
        addDir('Movies Pre 1989             A-Z','http://board.dailyflix.net/index.php?/forum/203-hd-movies-1989-earlier/?sort_key=title&sort_by=A-Z',1,icon,'HD Movies Pre 1989  - A-Z')
        addDir('Movies 2014-2015        Recently Added','http://board.dailyflix.net/index.php?/forum/423-hd-movies-2014-2015/?sort_key=last_post&sort_by=Z-A',1,icon,'HD Movies 2014 - Recently Added')
        addDir('Movies 2012-2013        Recently Added','http://board.dailyflix.net/index.php?/forum/196-hd-movies-2012-2013/?sort_key=last_post&sort_by=Z-A',1,icon,'HD Movies 2012-2013 - Recently Added')
        addDir('Movies 2006-2011        Recently Added','http://board.dailyflix.net/index.php?/forum/197-hd-movies-2006-2011/?sort_key=last_post&sort_by=Z-A',1,icon,'HD Movies 2006-2011 - Recently Added')
        addDir('Movies 2000-2005        Recently Added','http://board.dailyflix.net/index.php?/forum/199-hd-movies-2000-2005/?sort_key=last_post&sort_by=Z-A',1,icon,'HD Movies 2000-2005 - Recently Added')
        addDir('Movies 1990-1999        Recently Added','http://board.dailyflix.net/index.php?/forum/202-hd-movies-1990-1999/?sort_key=last_post&sort_by=Z-A',1,icon,'HD Movies 1990-1999 - Recently Added')
        addDir('Movies Pre 1989             Recently Added','http://board.dailyflix.net/index.php?/forum/203-hd-movies-1989-earlier/?sort_key=last_post&sort_by=Z-A',1,icon,'HD Movies Pre 1989  - Recently Added')        

def structure_flash_movies():
        addDir('Movies 2014-2015        A-Z','http://board.dailyflix.net/index.php?/forum/424-flash-2014-2015/?sort_key=title&sort_by=A-Z',1,icon,'Flash Movies 2014 - A-Z')
        addDir('Movies 2012-2013        A-Z','http://board.dailyflix.net/index.php?/forum/64-flash-2012-2013/?sort_key=title&sort_by=A-Z',1,icon,'Flash Movies 2012-2013 - A-Z')
        addDir('Movies 2006-2011        A-Z','http://board.dailyflix.net/index.php?/forum/65-flash-2006-2011/?sort_key=title&sort_by=A-Z',1,icon,'Flash Movies 2006-2011 - A-Z')
        addDir('Movies 2000-2005        A-Z','http://board.dailyflix.net/index.php?/forum/66-flash-2000-2005/?sort_key=title&sort_by=A-Z',1,icon,'Flash Movies 2000-2005 - A-Z')
        addDir('Movies 1990-1999        A-Z','http://board.dailyflix.net/index.php?/forum/67-flash-1990-1999/?sort_key=title&sort_by=A-Z',1,icon,'Flash Movies 1990-1999 - A-Z')
        addDir('Movies 1980-1989        A-Z','http://board.dailyflix.net/index.php?/forum/210-flash-1980-1989/?sort_key=title&sort_by=A-Z',1,icon,'Flash Movies 1980-1999 - A-Z')
        addDir('Movies Pre 1979             A-Z','http://board.dailyflix.net/index.php?/forum/68-flash-1979-earlier/?sort_key=title&sort_by=A-Z',1,icon,'Flash Movies Pre 1979  - A-Z')
        addDir('Movies 2014-2015        Recently Added','http://board.dailyflix.net/index.php?/forum/424-flash-2014-2015/?sort_key=last_post&sort_by=Z-A',1,icon,'Flash Movies 2014 - Recently Added')
        addDir('Movies 2012-2013        Recently Added','http://board.dailyflix.net/index.php?/forum/64-flash-2012-2013/?sort_key=last_post&sort_by=Z-A',1,icon,'Flash Movies 2012-2013 - Recently Added')
        addDir('Movies 2006-2011        Recently Added','http://board.dailyflix.net/index.php?/forum/65-flash-2006-2011/?sort_key=last_post&sort_by=Z-A',1,icon,'Flash Movies 2006-2011 - Recently Added')
        addDir('Movies 2000-2005        Recently Added','http://board.dailyflix.net/index.php?/forum/66-flash-2000-2005/?sort_key=last_post&sort_by=Z-A',1,icon,'Flash Movies 2000-2005 - Recently Added')
        addDir('Movies 1990-1999        Recently Added','http://board.dailyflix.net/index.php?/forum/67-flash-1990-1999/?sort_key=last_post&sort_by=Z-A',1,icon,'Flash Movies 1990-1999 - Recently Added')
        addDir('Movies 1980-1989        Recently Added','http://board.dailyflix.net/index.php?/forum/210-flash-1980-1989/?sort_key=last_post&sort_by=Z-A',1,icon,'Flash Movies 1980-1999 - Recently Added')
        addDir('Movies Pre 1979             Recently Added','http://board.dailyflix.net/index.php?/forum/68-flash-1979-earlier/?sort_key=last_post&sort_by=Z-A',1,icon,'Flash Movies Pre 1979  - Recently Added')        

def structure_preretail():
        addDir('Pre-Retail - DivX                   A-Z','http://board.dailyflix.net/index.php?/forum/217-preretail-flix-divx/?sort_key=title&sort_by=A-Z',1,icon,'Pre-Retail - DivX - A-Z')
        addDir('Pre-Retail - Flash                  A-Z','http://board.dailyflix.net/index.php?/forum/218-preretail-flix-flash/?sort_key=title&sort_by=A-Z',1,icon,'Pre-Retail - Flash - A-Z')
        addDir('Pre-Retail - MKV/MP4        A-Z','http://board.dailyflix.net/index.php?/forum/326-preretail-flix-mkv-mp4-h264/?sort_key=title&sort_by=A-Z',1,icon,'Pre-Retail - MKV/MP4 - A-Z')
        addDir('Pre-Retail - DivX                   Recently Added','http://board.dailyflix.net/index.php?/forum/217-preretail-flix-divx/?sort_key=last_post&sort_by=Z-A',1,icon,'Pre-Retail - DivX - Recently Added')
        addDir('Pre-Retail - Flash                  Recently Added','http://board.dailyflix.net/index.php?/forum/218-preretail-flix-flash/?sort_key=last_post&sort_by=Z-A',1,icon,'Pre-Retail - Flash - Recently Added')
        addDir('Pre-Retail - MKV/MP4        Recently Added','http://board.dailyflix.net/index.php?/forum/326-preretail-flix-mkv-mp4-h264/?sort_key=last_post&sort_by=Z-A',1,icon,'Pre-Retail - MKV/MP4 - Recently Added')
        
def tv_shows():
        addDir('General TV                                       A-Z','http://board.dailyflix.net/index.php?/forum/35-general-tv/?sort_key=title&sort_by=A-Z',14,icon,'General TV - A-Z')
        addDir('Reality/Talk Shows/Awards       A-Z','http://board.dailyflix.net/index.php?/forum/29-reality-tv-talk-shows-and-award-shows/?sort_key=title&sort_by=A-Z',14,icon,'Reality/Talk Shows/Awards - A-Z')
        addDir('Comedy                                            A-Z','http://board.dailyflix.net/index.php?/forum/30-comedy/?sort_key=title&sort_by=A-Z',14,icon,'Comedy - A-Z')
        addDir('Sci-Fi/Fantasy/Horror                  A-Z','http://board.dailyflix.net/index.php?/forum/31-sci-fi-fantasy-horror/?sort_key=title&sort_by=A-Z',14,icon,'Sci-Fi/Fantasy/Horror - A-Z')
        addDir('Teen Cartoons                                A-Z','http://board.dailyflix.net/index.php?/forum/32-teen-oriented-cartoons/?sort_key=title&sort_by=A-Z',14,icon,'Teen Cartoons - A-Z')
        addDir('Kids TV and Cartoons                   A-Z','http://board.dailyflix.net/index.php?/forum/33-kids-tv-shows-and-cartoons/?sort_key=title&sort_by=A-Z',14,icon,'Kids TV and Cartoons - A-Z')

        addDir('General TV                                       Recently Added','http://board.dailyflix.net/index.php?/forum/35-general-tv/?sort_key=last_post&sort_by=Z-A',14,icon,'General TV - Recently Added')
        addDir('Reality/Talk Shows/Awards       Recently Added','http://board.dailyflix.net/index.php?/forum/29-reality-tv-talk-shows-and-award-shows/?sort_key=last_post&sort_by=Z-A',14,icon,'Reality/Talk Shows/Awards - Recently Added')
        addDir('Comedy                                            Recently Added','http://board.dailyflix.net/index.php?/forum/30-comedy/?sort_key=last_post&sort_by=Z-A',14,icon,'Comedy - Recently Added')
        addDir('Sci-Fi/Fantasy/Horror                  Recently Added','http://board.dailyflix.net/index.php?/forum/31-sci-fi-fantasy-horror/?sort_key=last_post&sort_by=Z-A',14,icon,'Sci-Fi/Fantasy/Horror - Recently Added')
        addDir('Teen Cartoons                                Recently Added','http://board.dailyflix.net/index.php?/forum/32-teen-oriented-cartoons/?sort_key=last_post&sort_by=Z-A',14,icon,'Teen Cartoons - Recently Added')
        addDir('Kids TV and Cartoons                   Recently Added','http://board.dailyflix.net/index.php?/forum/33-kids-tv-shows-and-cartoons/?sort_key=last_post&sort_by=Z-A',14,icon,'Kids TV and Cartoons - Recently Added')

def foreignmovies():
        addDir('Chinese','chinese',20,icon,'Chinese')
        addDir('Dutch/Flemish','dutch',21,icon,'Dutch/Flemish')
        addDir('French','french',22,icon,'French')
        addDir('German','german',23,icon,'German')
        addDir('Italian','italian',24,icon,'Italian')
        addDir('Japanese','japanese',25,icon,'Japanese')
        addDir('Korean','korean',26,icon,'Korean')
        addDir('Russian','russian',27,icon,'Russian')
        addDir('Scandinavian','scandinavian',28,icon,'Scandinavian')
        addDir('Spanish','spanish',29,icon,'Spanish')
        addDir('Thai','thai',30,icon,'Thai')
        addDir('Other','other',31,icon,'Other')

def chinese():
        addDir('English Subbed/Dubbed                    A-Z','http://board.dailyflix.net/index.php?/forum/158-english-subbeddubbed/?sort_key=title&sort_by=A-Z',1,icon,'English Subbed/Dubbed')
        addDir('English Subbed/Dubbed                    Recently Added','http://board.dailyflix.net/index.php?/forum/158-english-subbeddubbed/?sort_key=last_post&sort_by=Z-A',1,icon,'English Subbed/Dubbed')
        addDir('Non English Subbed/Dubbed           A-Z','http://board.dailyflix.net/index.php?/forum/159-non-english-subbeddubbed/?sort_key=title&sort_by=A-Z',1,icon,'Non English Subbed/Dubbed')
        addDir('Non English Subbed/Dubbed           Recently Added','http://board.dailyflix.net/index.php?/forum/159-non-english-subbeddubbed/?sort_key=last_post&sort_by=Z-A',1,icon,'Non English Subbed/Dubbed')

def dutch():
        addDir('English Subbed/Dubbed                    A-Z','http://board.dailyflix.net/index.php?/forum/160-english-subbeddubbed/?sort_key=title&sort_by=A-Z',1,icon,'English Subbed/Dubbed')
        addDir('English Subbed/Dubbed                    Recently Added','http://board.dailyflix.net/index.php?/forum/160-english-subbeddubbed/?sort_key=last_post&sort_by=Z-A',1,icon,'English Subbed/Dubbed')
        addDir('Non English Subbed/Dubbed           A-Z','http://board.dailyflix.net/index.php?/forum/161-non-english-subbeddubbed/?sort_key=title&sort_by=A-Z',1,icon,'Non English Subbed/Dubbed')
        addDir('Non English Subbed/Dubbed           Recently Added','http://board.dailyflix.net/index.php?/forum/161-non-english-subbeddubbed/?sort_key=last_post&sort_by=Z-A',1,icon,'Non English Subbed/Dubbed')

def french():
        addDir('English Subbed/Dubbed                    A-Z','http://board.dailyflix.net/index.php?/forum/164-english-subbeddubbed/?sort_key=title&sort_by=A-Z',1,icon,'English Subbed/Dubbed')
        addDir('English Subbed/Dubbed                    Recently Added','http://board.dailyflix.net/index.php?/forum/164-english-subbeddubbed/?sort_key=last_post&sort_by=Z-A',1,icon,'English Subbed/Dubbed')
        addDir('Non English Subbed/Dubbed           A-Z','http://board.dailyflix.net/index.php?/forum/163-non-english-subbeddubbed/?sort_key=title&sort_by=A-Z',1,icon,'Non English Subbed/Dubbed')
        addDir('Non English Subbed/Dubbed           Recently Added','http://board.dailyflix.net/index.php?/forum/163-non-english-subbeddubbed/?sort_key=last_post&sort_by=Z-A',1,icon,'Non English Subbed/Dubbed')

def german():
        addDir('English Subbed/Dubbed                    A-Z','http://board.dailyflix.net/index.php?/forum/165-english-subbeddubbed/?sort_key=title&sort_by=A-Z',1,icon,'English Subbed/Dubbed')
        addDir('English Subbed/Dubbed                    Recently Added','http://board.dailyflix.net/index.php?/forum/165-english-subbeddubbed/?sort_key=last_post&sort_by=Z-A',1,icon,'English Subbed/Dubbed')
        addDir('Non English Subbed/Dubbed           A-Z','http://board.dailyflix.net/index.php?/forum/166-non-english-subbeddubbed/?sort_key=title&sort_by=A-Z',1,icon,'Non English Subbed/Dubbed')
        addDir('Non English Subbed/Dubbed           Recently Added','http://board.dailyflix.net/index.php?/forum/166-non-english-subbeddubbed/?sort_key=last_post&sort_by=Z-A',1,icon,'Non English Subbed/Dubbed')

def italian():
        addDir('English Subbed/Dubbed                    A-Z','http://board.dailyflix.net/index.php?/forum/167-english-subbeddubbed/?sort_key=title&sort_by=A-Z',1,icon,'English Subbed/Dubbed')
        addDir('English Subbed/Dubbed                    Recently Added','http://board.dailyflix.net/index.php?/forum/167-english-subbeddubbed/?sort_key=last_post&sort_by=Z-A',1,icon,'English Subbed/Dubbed')
        addDir('Non English Subbed/Dubbed           A-Z','http://board.dailyflix.net/index.php?/forum/168-non-english-subbeddubbed/?sort_key=title&sort_by=A-Z',1,icon,'Non English Subbed/Dubbed')
        addDir('Non English Subbed/Dubbed           Recently Added','http://board.dailyflix.net/index.php?/forum/168-non-english-subbeddubbed/?sort_key=last_post&sort_by=Z-A',1,icon,'Non English Subbed/Dubbed')

def japanese():
        addDir('English Subbed/Dubbed                    A-Z','http://board.dailyflix.net/index.php?/forum/169-english-subbeddubbed/?sort_key=title&sort_by=A-Z',1,icon,'English Subbed/Dubbed')
        addDir('English Subbed/Dubbed                    Recently Added','http://board.dailyflix.net/index.php?/forum/169-english-subbeddubbed/?sort_key=last_post&sort_by=Z-A',1,icon,'English Subbed/Dubbed')
        addDir('Non English Subbed/Dubbed           A-Z','http://board.dailyflix.net/index.php?/forum/170-non-english-subbeddubbed/?sort_key=title&sort_by=A-Z',1,icon,'Non English Subbed/Dubbed')
        addDir('Non English Subbed/Dubbed           Recently Added','http://board.dailyflix.net/index.php?/forum/170-non-english-subbeddubbed/?sort_key=last_post&sort_by=Z-A',1,icon,'Non English Subbed/Dubbed')

def korean():
        addDir('English Subbed/Dubbed                    A-Z','http://board.dailyflix.net/index.php?/forum/171-english-subbeddubbed/?sort_key=title&sort_by=A-Z',1,icon,'English Subbed/Dubbed')
        addDir('English Subbed/Dubbed                    Recently Added','http://board.dailyflix.net/index.php?/forum/171-english-subbeddubbed/?sort_key=last_post&sort_by=Z-A',1,icon,'English Subbed/Dubbed')
        addDir('Non English Subbed/Dubbed           A-Z','http://board.dailyflix.net/index.php?/forum/172-non-english-subbeddubbed/?sort_key=title&sort_by=A-Z',1,icon,'Non English Subbed/Dubbed')
        addDir('Non English Subbed/Dubbed           Recently Added','http://board.dailyflix.net/index.php?/forum/172-non-english-subbeddubbed/?sort_key=last_post&sort_by=Z-A',1,icon,'Non English Subbed/Dubbed')

def russian():
        addDir('English Subbed/Dubbed                    A-Z','http://board.dailyflix.net/index.php?/forum/173-english-subbeddubbed/?sort_key=title&sort_by=A-Z',1,icon,'English Subbed/Dubbed')
        addDir('English Subbed/Dubbed                    Recently Added','http://board.dailyflix.net/index.php?/forum/173-english-subbeddubbed/?sort_key=last_post&sort_by=Z-A',1,icon,'English Subbed/Dubbed')
        addDir('Non English Subbed/Dubbed           A-Z','http://board.dailyflix.net/index.php?/forum/174-non-english-subbeddubbed/?sort_key=title&sort_by=A-Z',1,icon,'Non English Subbed/Dubbed')
        addDir('Non English Subbed/Dubbed           Recently Added','http://board.dailyflix.net/index.php?/forum/174-non-english-subbeddubbed/?sort_key=last_post&sort_by=Z-A',1,icon,'Non English Subbed/Dubbed')

def scandinavian():
        addDir('English Subbed/Dubbed                    A-Z','http://board.dailyflix.net/index.php?/forum/175-english-subbeddubbed/?sort_key=title&sort_by=A-Z',1,icon,'English Subbed/Dubbed')
        addDir('English Subbed/Dubbed                    Recently Added','http://board.dailyflix.net/index.php?/forum/175-english-subbeddubbed/?sort_key=last_post&sort_by=Z-A',1,icon,'English Subbed/Dubbed')
        addDir('Non English Subbed/Dubbed           A-Z','http://board.dailyflix.net/index.php?/forum/176-non-english-subbeddubbed/?sort_key=title&sort_by=A-Z',1,icon,'Non English Subbed/Dubbed')
        addDir('Non English Subbed/Dubbed           Recently Added','http://board.dailyflix.net/index.php?/forum/176-non-english-subbeddubbed/?sort_key=last_post&sort_by=Z-A',1,icon,'Non English Subbed/Dubbed')

def spanish():
        addDir('English Subbed/Dubbed                    A-Z','http://board.dailyflix.net/index.php?/forum/177-english-subbeddubbed/?sort_key=title&sort_by=A-Z',1,icon,'English Subbed/Dubbed')
        addDir('English Subbed/Dubbed                    Recently Added','http://board.dailyflix.net/index.php?/forum/177-english-subbeddubbed/?sort_key=last_post&sort_by=Z-A',1,icon,'English Subbed/Dubbed')
        addDir('Non English Subbed/Dubbed           A-Z','http://board.dailyflix.net/index.php?/forum/178-non-english-subbeddubbed/?sort_key=title&sort_by=A-Z',1,icon,'Non English Subbed/Dubbed')
        addDir('Non English Subbed/Dubbed           Recently Added','http://board.dailyflix.net/index.php?/forum/178-non-english-subbeddubbed/?sort_key=last_post&sort_by=Z-A',1,icon,'Non English Subbed/Dubbed')

def thai():
        addDir('English Subbed/Dubbed                    A-Z','http://board.dailyflix.net/index.php?/forum/308-english-subbeddubbed/?sort_key=title&sort_by=A-Z',1,icon,'English Subbed/Dubbed')
        addDir('English Subbed/Dubbed                    Recently Added','http://board.dailyflix.net/index.php?/forum/308-english-subbeddubbed/?sort_key=last_post&sort_by=Z-A',1,icon,'English Subbed/Dubbed')
        addDir('Non English Subbed/Dubbed           A-Z','http://board.dailyflix.net/index.php?/forum/309-non-english-subbeddubbed/?sort_key=title&sort_by=A-Z',1,icon,'Non English Subbed/Dubbed')
        addDir('Non English Subbed/Dubbed           Recently Added','http://board.dailyflix.net/index.php?/forum/309-non-english-subbeddubbed/?sort_key=last_post&sort_by=Z-A',1,icon,'Non English Subbed/Dubbed')

def other():
        addDir('English Subbed/Dubbed                    A-Z','http://board.dailyflix.net/index.php?/forum/179-english-subbeddubbed/?sort_key=title&sort_by=A-Z',1,icon,'English Subbed/Dubbed')
        addDir('English Subbed/Dubbed                    Recently Added','http://board.dailyflix.net/index.php?/forum/179-english-subbeddubbed/?sort_key=last_post&sort_by=Z-A',1,icon,'English Subbed/Dubbed')
        addDir('Non English Subbed/Dubbed           A-Z','http://board.dailyflix.net/index.php?/forum/180-non-english-subbeddubbed/?sort_key=title&sort_by=A-Z',1,icon,'Non English Subbed/Dubbed')
        addDir('Non English Subbed/Dubbed           Recently Added','http://board.dailyflix.net/index.php?/forum/180-non-english-subbeddubbed/?sort_key=last_post&sort_by=Z-A',1,icon,'Non English Subbed/Dubbed')

def structure_microhd_movies():
        addDir('MicroHD                                 A-Z','http://board.dailyflix.net/index.php?/forum/310-microhd-movies/?sort_key=title&sort_by=A-Z',1,icon,'MicroHD - A-Z')
        addDir('MicroHD                                 Recently Added','http://board.dailyflix.net/index.php?/forum/310-microhd-movies/?sort_key=last_post&sort_by=Z-A',1,icon,'MicroHD - A-Z')
        
def PLAY(name,url):
        playlist = xbmc.PlayList(xbmc.PLAYLIST_VIDEO)
        playlist.clear()
        listitem = xbmcgui.ListItem(name, iconImage="DefaultVideo.png")
        listitem.setInfo("Video", infoLabels={ "Title": name})
        listitem.setProperty('mimetype', 'video/x-msvideo')
        listitem.setProperty('IsPlayable', 'true')
        xbmc.executebuiltin("XBMC.Notification(Please Wait!,Resolving Link,3000)")
        stream_url = urlresolver.HostedMediaFile(url).resolve()
        if not stream_url:
                xbmc.executebuiltin("XBMC.Notification(Sorry!,Link Cannot Be Resolved,5000)")
                return
        playlist.add(stream_url,listitem)
        xbmcPlayer = xbmc.Player()
        xbmcPlayer.play(playlist)
        addDir('','','','','')
     
def OPEN_URL(url):
    req = urllib2.Request(url)
    req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
    response = urllib2.urlopen(req)
    link=response.read()
    response.close()
    link = str(link)
    return link
     
     
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
     
# this is the listing of the items
     
def addDir(name,url,mode,iconimage,description):
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&iconimage="+urllib.quote_plus(iconimage)+"&description="+urllib.quote_plus(description)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "PlotOutline": description} )
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
        return ok
#same as above but this is addlink this is where you pass your playable content so you dont use addDir you use addLink "url" is always the playable content        
def addLink(name,url,iconimage,description):
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name, "Plot": description } )
        liz.setProperty("IsPlayable","true")
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=url,listitem=liz,isFolder=False)
        return ok
def addClick(name,url,mode,iconimage,description):
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&iconimage="+urllib.quote_plus(iconimage)+"&description="+urllib.quote_plus(description)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "PlotOutline": description} )
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=False)
        return ok
def addSpecial(name,url,mode,image):
        liz=xbmcgui.ListItem(label = '[B]%s[/B]'%name,iconImage="",thumbnailImage = image)
        liz.setProperty('fanart_image', '')
        xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=sys.argv[0]+"?url=%s&mode=%s&name=%s"%(url,mode,name),isFolder=False,listitem=liz)
     
           
#below tells plugin about the views                
def setView(content, viewType):
        # set content type so library shows more views and info
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
send=None

     

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
        print "nextdirectory "+url
        nextdirectory(url)
           
elif mode==2:
        print "nextdirectory_nextdirectory "+url
        nextdirectory_nextdirectory(url)

elif mode==3:
        print "structure_divx_movies "
        structure_divx_movies()

elif mode==4:
        print "structure_HD_movies "
        structure_HD_movies()
        
elif mode==5:
        print "PLAY "+url
        PLAY(name,url)

elif mode==6:
        print "structure_flash_movies "
        structure_flash_movies()

elif mode==7:
        print ""+url
        structure_HD_TV()

elif mode==8:
        print ""+url
        structure_divx_TV()

elif mode==9:
        print ""+url
        structure_flash_TV()

elif mode==10:
        print "structure_search "+url
        structure_search(url)

elif mode==11:
        print "structure_searchpages "+url
        structure_searchpages(url)

elif mode==12:
        print "structure_seasons "+url
        structure_seasons(url)

elif mode==13:
        print "structure_episodes "
        structure_episodesone(url)

elif mode==14:
        print "next directory tv"+url
        nextdirectorytv(url)
     
elif mode == 'play':
    stream_url = urlresolver.HostedMediaFile(url).resolve()
    if stream_url:
        xbmc.Player(xbmc.PLAYER_CORE_DVDPLAYER).play(stream_url)
        addon.add_directory({'mode': 'play', 'url': url}, {'title': 'Play Again'})

elif mode==15:
        print "test_resolve"
        test_resolve()

elif mode==16:
        print "structure_preretail"
        structure_preretail()

elif mode==17:
        print "TV_shows"
        tv_shows()

elif mode==18:
        print "IMDB "+url
        imdb(url)

elif mode==19:
        print 'Foreign Movies'
        foreignmovies()

elif mode==20:
        print 'Chinese'
        chinese()

elif mode==21:
        print 'Dutch'
        dutch()

elif mode==22:
        print 'French'
        french()

elif mode==23:
        print 'German'
        german()

elif mode==24:
        print 'Italian'
        italian()

elif mode==25:
        print 'Japanese'
        japanese()

elif mode==26:
        print 'Korean'
        korean()

elif mode==27:
        print 'Russian'
        russian()

elif mode==28:
        print 'Scandinavian'
        scandinavian()

elif mode==29:
        print 'Spanish'
        spanish()

elif mode==30:
        print 'Thai'
        thai()

elif mode==31:
        print 'Other'
        other()

elif mode==32:
        print "structure_searchTC "+name
        structure_searchTC(name)

elif mode==33:
        print 'structure_microhd_movies'
        structure_microhd_movies()

elif mode==34:
        print 'MKV/MP4'
        structure_mkv()

elif mode==69:
    urlresolver.display_settings()
     
           
xbmcplugin.endOfDirectory(int(sys.argv[1]))
