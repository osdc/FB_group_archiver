import urllib2
import time
import urllib
import re
import ConfigParser
import json
import MySQLdb
import logging
import traceback
from datetime import datetime
import iso8601
a=1

# To be done-- Date issue db is storing the current timestamp instead of fb post date !
# to use REquest instead of urllib2
class Archiver:

    def __init__(self, init_config_filename):
        self.init_config = ConfigParser.ConfigParser()
                
        try:
            self.init_config.read(init_config_filename)
        except:
            print  str(init_config_filename)+' : Read Error'
            return
        init_config = self.init_config
        self.db = MySQLdb.connect(user=init_config.get('db','user'), passwd=init_config.get('db','password'), db=init_config.get('db','name'))
        self.cursor = self.db.cursor()
        # store the error and info log
        logging.basicConfig(filename=init_config.get('logging','infolog'), level=logging.INFO)

    def process_data(self):
        controlchar_regex = re.compile(r'[\n\r\t]')
        cursor = self.cursor
        init_config = self.init_config
        fb_url = init_config.get('group','url')
        jsdata = urllib2.urlopen(fb_url).read()
        jsondata = json.loads(jsdata)
        for i,post in enumerate(jsondata['data']):
            try:
                post_id = post.get('id').rsplit('_',1)[1]
                message = post.get('message')
	        created_on_d = iso8601.parse_date(post.get('created_time'))
		created_on = created_on_d.strftime('%Y-%m-%d %H:%M:%S')
                updated_on_d = iso8601.parse_date(post.get('updated_time'))
                updated_on = created_on_d.strftime('%Y-%m-%d %H:%M:%S')
		author_name = post.get('from').get('name').encode('ascii','ignore').replace('"','')
                author_id = post.get('from').get('id')
                if(message != None):
                    message = message.encode('ascii','ignore').replace('"','')
                    comments_count = None
                    likes_count = None
                    title = ''
                    if(post.get('comments') != None):
                        comments_count = post.get('comments').get('count')
                    if(post.get('likes') != None):
                        likes_count = post.get('likes').get('count')
                    
                   
                    cursor.execute("""SELECT InsertPost(%s, %s, %s, %s, %s, %s, %s, %s)""", (author_name, author_id, message, likes_count, comments_count, created_on, updated_on, post_id))
                    code = cursor.fetchone()
                    # code[0] indicates the number of affected rows, if its 1 -> successful insert, if not the post already exists in thr Db
                    if(code[0] == 1 and post.get('link') !=  None):
                        link = post.get('link').encode('ascii','ignore')
                        if(post.get('name') != None):
                            title = controlchar_regex.sub(' ',post.get('name').encode('ascii','ignore').replace('"',''))
                        if(post.get('description') != None):
                            description = post.get('description').encode('ascii','ignore').replace('"','')
                            description = controlchar_regex.sub(' ',description) + ' - ' + author_name
                        else:
                            description = controlchar_regex.sub(' ',message) + ' - ' + author_name
                
                        # Build the JSON !! Don't change Anything here
                        values = '{"url": "'+link+'" , "list":"'+init_config.get('kippt','listuri')+'", "title":"'+title+'", "notes":"'+description+ '"}'
                        r = self.kippt_post(values)
                        self.link_store(r, post_id)

                    elif(code[0] == 1):
                       
                      # regex can be improved 
                       try:
                           description = post.get('message').encode('ascii','ignore').replace('"','')
                           description = controlchar_regex.sub(' ',description)
                           urls =  re.findall("(?P<url>https?://[^\s]+)", description)
                           for url in urls:
                               description = description.replace(url, '')
                           description = description  + ' - ' + author_name

                           for url in urls:
                               # Build the JSON !! Don't change anythig here !! 
                               values = '{"url": "'+url+'" , "list": "'+init_config.get('kippt','listuri')+'", "notes":"'+description+'"}' 
                               r = self.kippt_post(values)
                               self.link_store(r, post_id)
                       except Exception, err:
                           logging.error(str(datetime.now())+" "+str(err))
                           traceback.print_exc(file = open(init_config.get('logging','errorlog'),'a'))
            except Exception, err:
                print 'Some error'
                logging.error(str(datetime.now())+" "+str(err))
                traceback.print_exc(file = open(init_config.get('logging','errorlog'),'a'))
        print "Archiving Complete!"
        logging.info(str(datetime.now())+' Archiving Complete for page: '+fb_url)


    def link_store(self, response, post_id):
        cursor = self.cursor
        resp_jsdata = json.loads(response)
        resp_url=resp_jsdata.get('url').encode('ascii','ignore').replace('"','')
        resp_title=resp_jsdata.get('title').encode('ascii','ignore').replace('"','')
        resp_notes=resp_jsdata.get('notes').encode('ascii','ignore').replace('"','') 
        cursor.execute("""SELECT InsertLink(%s, %s, %s, %s) """,(resp_url, resp_title, resp_notes, post_id ))
 

    def kippt_post(self, values):

        init_config = self.init_config
        req = urllib2.Request(init_config.get('kippt','url'),values)
        req.add_header('X-Kippt-Username', init_config.get('kippt','username'))
        req.add_header('X-Kippt-API-Token', init_config.get('kippt','apitoken'))
        r= urllib2.urlopen(req)
        return r.read()                                                                   

    
