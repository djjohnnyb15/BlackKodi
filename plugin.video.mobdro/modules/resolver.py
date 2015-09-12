import plugintools
import json
import xbmcaddon

__settings__ = xbmcaddon.Addon(id='plugin.video.mobdro')

supported_sites = ["url", "youtube", "biggestplayer", "relayer", "veetle", "vaughnlive", "rtmpdump", "filmon", "ustream", "livestream", "twitch", "iliveto"]

for site in supported_sites:
    exec "from resolvers import " + site

def display(result):
    for site in supported_sites:
        try:
            if result[site] and (not __settings__.getSetting("HOST_" + site.upper()) or __settings__.getSetting("HOST_" + site.upper()) == "true"):
                title = result.get("name").encode("utf-8").decode("string_escape").upper()
                if site == "rtmpdump" and not result[site]["rtmp"]:
                    continue
                thumbnail = result.get("img").encode("utf-8").decode("string_escape")
                plot = result.get("description").encode("utf-8").decode("string_escape")
                
                item_data = {
                             "type":site,
                             "data":result[site]
                }
                
                if __settings__.getSetting("DEBUG") == "true":
                    title = title + "( " + site + ")"
                
                plugintools.add_item( action="play" , title=title, plot=plot, url=json.dumps(item_data), folder=False )
                return 1
        except KeyError:
            pass
   
def resolve(params):
    type = params["type"]
    data = params["data"]
    #try:
    resolved_url = eval(type + ".parse_" + type + "(data)")
    return resolved_url
    #except:
    #    return ""