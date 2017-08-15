import os

print ">>Cache Cleaner running..."
os.system("sudo python CCleaner.py")
print ">>Web Interface running..."
#os.system("sudo python index.py")
os.system("gunicorn -w 4 -b 192.168.81.218:80 index:app")