# -*- coding: utf-8 -*-
#Библиотеки, които използват python и Kodi в тази приставка
import re
import sys
import os
import urllib
import urllib2
import xbmc, xbmcplugin,xbmcgui,xbmcaddon
import base64
import cookielib
import xbmcvfs
import mechanize
import codecs


#Място за дефиниране на константи, които ще се използват няколкократно из отделните модули
__addon_id__= 'plugin.video.rntv'
__Addon = xbmcaddon.Addon(__addon_id__)
__settings__ = xbmcaddon.Addon(id=__addon_id__)
__addondir__    = xbmc.translatePath( __Addon.getAddonInfo('profile') ) 
baseurl = xbmcaddon.Addon().getSetting('baseurl')
username = xbmcaddon.Addon().getSetting('settings_username')
password = xbmcaddon.Addon().getSetting('settings_password')
channels = xbmcaddon.Addon().getSetting('channels')
thumburl = xbmcaddon.Addon().getSetting('chlogos')
UA = 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:40.0) Gecko/20100101 Firefox/58.0' #За симулиране на заявка от  компютърен браузър

#инициализация
if not username or not password or not __settings__:
        xbmcaddon.Addon().openSettings()

br = mechanize.Browser()
cj = cookielib.LWPCookieJar()
br.set_cookiejar(cj)
br.set_handle_equiv(True)
br.set_handle_redirect(True)
br.set_handle_referer(True)
br.set_handle_robots(False)
br.addheaders = [('User-agent', UA)]
br.set_handle_refresh(mechanize._http.HTTPRefreshProcessor(), max_time=1)
base = base64.b64decode(baseurl)
print base
r= br.open(base)
br.select_form(nr=0)
br.form['UserName'] = username
br.form['Password'] = password
br.form['RememberMe'] = ['true']
br.submit()

#Меню с директории в приставката
def CATEGORIES():
        chnames = channels.decode('hex')
        names = base64.b64decode(chnames)
        match = re.compile('"(.+?)"').findall(names)
        match.sort()
        for channel in match:      
         url = base64.b64decode('aHR0cDovL3BsYXkucm4tdHYuY29tLzc0NzkvcGxheS8=') + channel
         thumbnail = base64.b64decode(thumburl) + channel + base64.b64decode('LnBuZw==')
         if thumbnail is '':
          thumbnail = 'DefaultFolder.png'
         addLink(channel,url,2,thumbnail)
         


#Разлистване видеата на първата подадена страница
def INDEXPAGES(url):
        ""

#Зареждане на видео
def PLAY(url):
        f = br.open(url)
        html = f.read()
        li = xbmcgui.ListItem(iconImage=iconimage, thumbnailImage=iconimage, path=html+'|X-Forwarded-For='+baseurl+'&User-Agent='+urllib.quote_plus(UA))
        li.setInfo('video', { 'title': name })
        try:
            xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, li)
        except:
            xbmc.executebuiltin("Notification('Грешка','Видеото липсва на сървъра!')")




#Модул за добавяне на отделно заглавие и неговите атрибути към съдържанието на показваната в Kodi директория - НЯМА НУЖДА ДА ПРОМЕНЯТЕ НИЩО ТУК
def addLink(name,url,mode,iconimage):
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage=iconimage, thumbnailImage=iconimage)
        liz.setArt({ 'thumb': iconimage,'poster': iconimage, 'banner' : iconimage, 'fanart': iconimage })
        liz.setInfo( type="Video", infoLabels={ "Title": name } )
        liz.setProperty("IsPlayable" , "true")
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=False)
        return ok



#Модул за добавяне на отделна директория и нейните атрибути към съдържанието на показваната в Kodi директория - НЯМА НУЖДА ДА ПРОМЕНЯТЕ НИЩО ТУК
def addDir(name,url,mode,iconimage):
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage=iconimage, thumbnailImage=iconimage)
        liz.setArt({ 'thumb': iconimage,'poster': iconimage, 'banner' : iconimage, 'fanart': iconimage })
        liz.setInfo( type="Video", infoLabels={ "Title": name } )
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
        return ok


#НЯМА НУЖДА ДА ПРОМЕНЯТЕ НИЩО ТУК
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







params=get_params()
url=None
name=None
iconimage=None
mode=None

try:
        url=urllib.unquote_plus(params["url"])
except:
        pass
try:
        name=urllib.unquote_plus(params["name"])
except:
        pass
try:
        name=urllib.unquote_plus(params["iconimage"])
except:
        pass
try:
        mode=int(params["mode"])
except:
        pass


#Списък на отделните подпрограми/модули в тази приставка - трябва напълно да отговаря на кода отгоре
if mode==None or url==None or len(url)<1:
        print ""
        CATEGORIES()
    
elif mode==1:
        print ""+url
        INDEXPAGES(url)

elif mode==2:
        print ""+url
        PLAY(url)

xbmcplugin.endOfDirectory(int(sys.argv[1]))
