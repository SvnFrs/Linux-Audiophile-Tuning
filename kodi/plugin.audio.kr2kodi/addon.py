
import sys, xbmcgui, xbmcplugin
import urllib, urllib2, re

addon_handle = int(sys.argv[1])

xbmcplugin.setContent(addon_handle, 'audio')

def url_func(url):
    WebSock = urllib.urlopen(url)
    WebHTML = WebSock.read()
    WebSock.close()
    return WebHTML

def kbs_func(code):
    Base_URL = 'http://onair.kbs.co.kr/index.html?sname=onair&stype=live&ch_code=' + code
    WebHTML = url_func(Base_URL)
    Temp_Web_URL = re.compile('http://.*_lsu_sa_=[0-9a-z]*').findall(WebHTML)
    url = Temp_Web_URL[0].split('\\', 1)[0]
    ### Double query
    #url_root = url.rsplit('/', 1)[0]
    #M3U = url_func(url)
    #M3U = re.compile('.*m3u.*').findall(M3U)[0]
    #url = url_root + '/' + M3U
    ###
    return url

def mbc_func(code):
    Base_URL = 'http://miniplay.imbc.com/AACLiveURL.ashx?channel=' + code + '&agent=android&protocol=M3U8'
    url = url_func(Base_URL)
    ### Double query
    #url_root = url.rsplit('/', 1)[0]
    #M3U = url_func(url)
    #M3U = re.compile('.*m3u.*').findall(M3U)[0]
    #url = url_root + '/' + M3U
    ###
    return url

def sbs_func(code1, code2):

    Base_URL = 'http://api.sbs.co.kr/vod/_v1/Onair_Media_Auth_Security.jsp?channelPath=' + code1 + '&streamName=' + code2 + '.stream&playerType=mobile'
    data = url_func(Base_URL)

    import base64, Crypto.Cipher.DES

    key = b'7d1ff4ea8925c225'
    ciphertext = base64.b64decode(data)
    cipher = Crypto.Cipher.DES.new(key[:8], mode=Crypto.Cipher.DES.MODE_ECB)
    text = cipher.decrypt(ciphertext)
    url = text.decode('utf8')

    ### Double query
    #print(url)
    #M3U = url_func(url)
    #url = re.compile('.*m3u.*').findall(M3U)[0]
    ###
    return url

def ch_func(ch):
    if   ch == 'KBS 1FM':
        url = kbs_func('24')
    elif ch == 'KBS 2FM':
        url = kbs_func('25')
    elif ch == 'KBS 1R':
        url = kbs_func('21')
    elif ch == 'KBS 2R':
        url = kbs_func('22')
    elif ch == 'KBS 3R':
        url = kbs_func('23')
    elif ch == 'KBS SCR':
        url = kbs_func('I26')
    elif ch == 'KBS RKI':
        url = kbs_func('I92')
    elif ch == 'MBC Channel M':
        url = mbc_func('chm')
    elif ch == 'MBC FM4U':
        url = mbc_func('mfm')
    elif ch == 'MBC FM':
        url = mbc_func('sfm')
    elif ch == 'SBS Power FM':
        url = sbs_func('powerpc',  'powerfm')
    elif ch == 'SBS Love FM':
        url = sbs_func('lovepc',   'lovefm')
    else:
        print 'Argument(s) is missing or invalid!'
        quit()
    return url

def add_func(ch, url):
    url = url
    li = xbmcgui.ListItem(ch, iconImage='DefaultAudio.png')
    xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li)

chs = ["KBS 1FM", "KBS 2FM", "MBC Channel M", "MBC FM4U", "MBC FM", "SBS Power FM", "SBS Love FM"]
for ch in chs:
    ch = ch
    url = ch_func(ch)
    add_func(ch, url)

add_func('CBS Music FM', 'http://aac.cbs.co.kr/cbs939/cbs939.stream/playlist.m3u8')
add_func('tbs FM',       'http://tbs.hscdn.com/tbsradio/fm/playlist.m3u8')
add_func('Gukak FM',     'http://mgugaklive.nowcdn.co.kr/gugakradio/gugakradio.stream/playlist.m3u8')
add_func('EBS FM',       'http://ebsonair.ebs.co.kr/fmradiofamilypc/familypc1m/playlist.m3u8')

xbmcplugin.endOfDirectory(addon_handle)