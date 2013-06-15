import urllib
import urllib2
import json
import ConfigParser
import sys

from sync_fb import Archiver
#To be done-- To use Requests instead of urllib2

def main():
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
        Archiver(sys.argv[1]).process_data(fb_url)
        jsdata = urllib2.urlopen(fb_url).read()
        jsondata =  json.loads(jsdata)
        #paging attribute used to go to next page
        fb_url = jsondata.get('paging').get('next')
        print fb_url
   

if __name__ == "__main__":
    main()

