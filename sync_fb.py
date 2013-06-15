import urllib2
import re
import ConfigParser
import json
import MySQLdb
import logging
import traceback
from datetime import datetime
import iso8601
from kippt_module import *
import time


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
		#Initialize DB configuration
        passwd = init_config.get('db','password')
        self.update = 0
        self.db = MySQLdb.connect(user=init_config.get('db','user'), passwd=init_config.get('db','password'), db=init_config.get('db','name'))
        self.cursor = self.db.cursor()
        # Initialize  the error and info log
        logging.basicConfig(filename=init_config.get('logging','infolog'), level=logging.INFO)

    def process_data(self,fb_url=None):
        cursor = self.cursor
        init_config = self.init_config
         
        if(fb_url == None):
         fb_url = init_config.get('group','url')
       
        desc_trim = re.compile(r'[\n\r\t]')  
        #default list_uri
        list_uri = init_config.get('kippt','listuri')
        hashtag = [] 
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
                c_update = 0
                 
                #if(message == None) "Post only had a link !"
                
                if(message != None):
                    message = message.encode('ascii','ignore').replace('"','')
                    message_copy = message 
                    comments_count = 0
                    likes_count = 0
                    title = ''
                                                           
                    if ('comments' in post and post.get('comments').get('data') != None):
                      for comment in post.get('comments').get('data'):
                          comments_count+=1 
                            
                    if(post.get('likes') != None):
                        likes_count = post.get('likes').get('count')
                    
	            cursor.execute("SELECT comments_count from posts where posts.id = (%s)  and comments_count > 0 ",post_id)
                    previous_comment = cursor.fetchone() 
                    
                    
                    cursor.execute("""SELECT InsertPost(%s, %s, %s, %s, %s, %s, %s, %s)""", (author_name, author_id, message, likes_count, comments_count, created_on, updated_on, post_id))
                    code = cursor.fetchone()
                    
                    #to check if the link in the old post has no hashtag and comment is updated with hashtag the link wil go in new\
                    #hashtag 
                    if(code[0] == 2):
                      cursor.execute("SELECT comments_count from posts where posts.id = (%s)  and comments_count > 0 ",post_id)
                      comment_update = cursor.fetchone()
                      if(comment_update !=None):
                       c_update = comment_update[0] - previous_comment[0]
                    #to get the list_uri of kippt list   
                    list_uri = self.process_hashtag(message,post,code[0],c_update)
                    # code[0] ==1 indicates no duplicate entry is posted in DB , instead Update the likes and comment count , see DB function structure
                    if(code[0] == 1 and post.get('link') !=  None):
                        link = post.get('link').encode('ascii','ignore')
                        if(post.get('name') != None):
                            title = desc_trim.sub(' ',post.get('name').encode('ascii','ignore').replace('"',''))
                        if(post.get('description') != None):
                            description = post.get('description').encode('ascii','ignore').replace('"','')

                            description = desc_trim.sub(' ',description) + ' - ' + author_name
                        else:
                            description = desc_trim.sub(' ',message) + ' - ' + author_name
                        
                        # Build the Kippt JSON !! Don't change Anything here
                        values = '{"url": "'+link+'" , "list":"'+list_uri+'", "title":"'+title+'", "notes":"'+description+ '"}'
                        # Get the permalink from Kippt link and then Store in Db    
                        js_dump = self.kippt_post(values)
                        self.link_store(js_dump, post_id)

                    elif(code[0] == 1):
                       
                       try:
                           description = post.get('message').encode('ascii','ignore').replace('"','')
                           description = desc_trim.sub(' ',description)
                           urls =  re.findall("(?P<url>https?://[^\s]+)", description)
                             
                           for url in urls:
                               description = description.replace(url, '')
                           description = description  + ' - ' + author_name

                           for url in urls:
                               # Build the JSON !! Don't change anythig here !! 
                               values = '{"url": "'+url+'" , "list": "'+list_uri+'", "notes":"'+description+'"}' 
                               #print url
                               js_dump = self.kippt_post(values) 
                               self.link_store(js_dump, post_id)
                           
                       except Exception, err:
                           logging.error(str(datetime.now())+" "+str(err))
                           traceback.print_exc(file = open(init_config.get('logging','errorlog'),'a'))

                    #if the post already exists in Db but comment hashtag is updated make a list coressponding to hashtag     
                    #in kippt  
                    if (self.update == 1 and post.get('link')!=None and self.hashtag[0]!='archive' and code[0] == 2):
                           try:
                               if(post.get('description') != None):
                                description = post.get('description').encode('ascii','ignore').replace('"','')

                                description = desc_trim.sub(' ',description) + ' - ' + author_name
                               else:
                                description = '- ' + author_name
  
                               values = '{"url": "'+post.get('link')+'" , "list": "'+list_uri+'", "notes":"'+description+'"}' 
                               #print self.hashtag 
                               js_dump = self.kippt_post(values) 
                               
                           except Exception, err:
                            print 'Some error'
                            logging.error(str(datetime.now())+" "+str(err))
                            traceback.print_exc(file = open(init_config.get('logging','errorlog'),'a')) 
             
            except Exception, err:
                print 'Some error'
                logging.error(str(datetime.now())+" "+str(err))
                traceback.print_exc(file = open(init_config.get('logging','errorlog'),'a'))
        print "Archiving Complete!"
        logging.info(str(datetime.now())+' Archiving Complete for page: '+fb_url)


   
   
    def process_hashtag(self,message,post,code,c_update):
                    init_config = self.init_config
                    ind = 0 
                    kippt_init = Kippt(username = init_config.get('kippt','username'), api_token = init_config.get('kippt','apitoken'))
                    self.hashtag = [i  for i in message.split() if i.startswith("#") ]
                    if not self.hashtag:
                      self.check_comment_hashtag(post,code,c_update) 
                      self.hashtag.append ('archive')
                    #Strip down the hashes ! 
                    else:
                     for i in self.hashtag:  
                       self.hashtag[ind] = re.sub(r'#','',i)   
                       self.hashtag[ind] = self.hashtag[ind].lower() 
                       ind+=1 
                    list_search = json.dumps(kippt_init.get_lists())
                    jsondata_kippt = json.loads(list_search)
                    
                    for i,post in enumerate (jsondata_kippt['objects']):
                      list_uri = post.get('resource_uri') 
                      slug  = post.get('slug').lower()
                      #kippt api is returning the deleted list id also that is why this check.. 
                      a = kippt_init.get_list(re.search('(\d+)',list_uri ).group(1))  
  
                      if(slug == self.hashtag[0] and 'message' not in a):
                          #print list_uri + "Already exists!"
                          return list_uri 
                   
                    a = kippt_init.create(self.hashtag[0])
                    list_uri = a['resource_uri']
                    #print list_uri + "created"
                    return list_uri

    def kippt_post(self, values):
        init_config = self.init_config     
        req = urllib2.Request(init_config.get('kippt','url'),values)
        req.add_header('X-Kippt-Username', init_config.get('kippt','username'))
        req.add_header('X-Kippt-API-Token', init_config.get('kippt','apitoken'))
        r= urllib2.urlopen(req)
        # print "posting " +self.hashtag[0] + url
        return r.read()                                                                   
 
    def link_store(self, response, post_id):
        cursor = self.cursor
        resp_jsdata = json.loads(response)
        resp_url=resp_jsdata.get('url').encode('ascii','ignore').replace('"','')
        resp_title=resp_jsdata.get('title').encode('ascii','ignore').replace('"','')
        resp_notes=resp_jsdata.get('notes').encode('ascii','ignore').replace('"','') 
        cursor.execute("""SELECT InsertLink(%s, %s, %s, %s) """,(resp_url, resp_title, resp_notes, post_id ))



    # try to build hashtag list from comments if post don't include hashtag 
    def check_comment_hashtag(self,post,code,c_update):
          ind =0
          desc_trim = re.compile(r'[\n\r\t]')  
          if ('comments' in post and post.get('comments').get('data') != None):
                      for comment in post.get('comments').get('data'):
                          mess = comment.get('message').encode('ascii','ignore').replace('"','')
                          mess = desc_trim.sub(' ',mess) 
                          hash_tag = [i  for i in mess.split() if i.startswith("#") ]
                          if (hash_tag):
                             self.hashtag = hash_tag
                             #strip down #
                             for i in self.hashtag:  
                                 self.hashtag[ind] = re.sub(r'#','',i)   
                                 self.hashtag[ind] = self.hashtag[ind].lower()
                                 ind+=1
                             
                             if (code == 2 and c_update >0):
                                #print "processed update" 
                                self.update =1    
                             return    
                                   
               
       

