import urllib
import urllib2
import json
import ConfigParser
import sys

from sync_fb import Archiver
#To be done-- To use Requests instead of urllib2

def main():
 url_fb = []

 try:
    if (len(sys.argv)>1):     
        init_config = ConfigParser.ConfigParser() 
        init_config.read(sys.argv[1])
        fb_url = init_config.get('group','url')
    else:
        print 'Correct usage: Init_archive <path to default properties file>'
        return
    jsdata = urllib2.urlopen(fb_url).read()
    jsondata = json.loads(jsdata)
    while(fb_url is not None):
        jsdata = urllib2.urlopen(fb_url).read()
        jsondata =  json.loads(jsdata)
        #paging attribute used to go to next page
        fb_url = jsondata.get('paging').get('next')
        url_fb.append(fb_url)
 except Exception , err:
    print str(len(url_fb)) + " :Length of json pages of group! Sit back and relax its gonna take some time an hour or so " 
    
# Archive post in reverse order so the new link post to db and kipppt first
 fb_url = url_fb.pop()
 jsdata = urllib2.urlopen(fb_url).read()
 jsondata = json.loads(jsdata)
 while(fb_url is not None):
   Archiver(sys.argv[1]).process_data(fb_url)
   jsdata = urllib2.urlopen(fb_url).read()
   jsondata =  json.loads(jsdata)
   fb_url = url_fb.pop()


if __name__ == "__main__":
    main()

