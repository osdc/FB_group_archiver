import sys

from sync_fb import Archiver

try:
    Archiver(sys.argv[1]).process_data()
except Exception, e:
    print sys.argv[0]
    print 'Correct use: cron_tab <path to default properties file'
    print sys.argv[1]
    print e
