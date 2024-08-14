
import urllib.parse as p

from nwebclient import util
from nwebclient import nweb
from nwebclient import web as w

def nx_channel_emit(guid, message):
    key = nweb.nweb_cfg['V4_INNER_SECRET']
    url = nweb.nweb_cfg.get('NTS_URL', 'ws://localhost:3000/')
    util.wget(url + 'ws-nx-emit?key=' + key + '&guid=' + guid + '&message='+p.quote(message), verify=True)

def nx_channel_html_part(guid):
    res = w.script('/static/js/socket.io.js')
    res += w.js_ready("""
            const socket = io("wss://bsnx.net/", {
                transports:["websocket"], 
                query: "nx_guid=""" + guid + """"});
            socket.on("msg", function(msg) { 
                console.log(msg); 
                const $console = document.querySelector("#console");
                $console.append(msg,document.createElement("br"));
            }); 
        """)
    res += w.div('', id='console')
    return res
