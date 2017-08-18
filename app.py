import os
from threading import Thread
from Utilities import CCleaner

WORKDS_COUNT = 6

print ">>Cache Cleaner running..."
tn = Thread(target= CCleaner.cacheCleaner_Start)
tn.setDaemon(True)
tn.start()
print ">>Web Interface running..."
if "mode.server" in os.listdir("./"):
    # when a specific file in current dir,bind IP below  
    # running on beta.baderlab.org
    print ">>>Running as server mode,use http://beta.baderlab.org to visit."
    os.system("gunicorn -w %d -b 192.168.81.218:80 index:app"%WORKDS_COUNT)
elif "mode.debug" in os.listdir("../"):
    # used for debug, only run on a single thread
    os.system("python index.py")
else:
    # local machine for test
    print ">>>Running on local machine."
    os.system("gunicorn -w %d -b 127.0.0.1:5000 index:app"%WORKDS_COUNT)