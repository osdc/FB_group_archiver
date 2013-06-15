FB_group_archiver
==================
Example <a href="https://www.facebook.com/groups/jiitlug/" target ='_blank'>Jiit osdc group</a>
<a href="https://kippt.com/Osdc_JIIT" target ='_blank'> Archive </a>  

It is a utility to archive post from Facebook open group 

and parse out the link and store them to kippt list

based on hashtag associated with post

Also if post has no hashtag then some group member can comment just the hashtag and link will be stored in kippt list based on that hashtag 


Init_archive.py
=====
Run Init.py with configuration file as argument for the first time
It archives all post since beginning.
Basically it calls sync_fb with json data

cron_tab.py
=======
Should run every few minutes to get updated post from group

config folder
======
change the settings here

db
====
import database.sql file in your db

 
Issues
======
 use request packages insead of urllib2 

 see the date issue
 
 Currently not storing the cooment links, can be done easily

 Currently not storing comments  

 Removing duplicate links By comparing lists 
 
