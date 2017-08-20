#this script is used to clean cache in Cache module.
from apscheduler.schedulers.blocking import BlockingScheduler
from Utilities import SessionManager as SM
import os

CACHE_CLEAN_INTERVAL = 24*SM.VAR_RESULT_LIFE  # hours to clean cache

def cacheCleaner_Start():
    scheduler = BlockingScheduler()
    scheduler.add_job(cleanOODCache, 'interval', hours=CACHE_CLEAN_INTERVAL)
    scheduler.start()
    

def cleanOODCache():
    print ">>>start deleting cache..."
    OODList = SM.getOutofDateSessionList()
    SM.deleteSession(OODList)
    for session in OODList:
        os.system("sudo rm -rf ./Cache/"+session)
    print ">>>%d data deleted."%len(OODList)