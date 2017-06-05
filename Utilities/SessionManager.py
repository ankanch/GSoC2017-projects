import random
import string
import time
import datetime

# NOTE: we are manage session in a text file which one line 
# in that file stands for one session. 
# Session format as below:
#                           session id , created date
# when a new session generated ,we will add it to the file
# if a session out of date ,we will have to delete them as well
# MAXIUM SESSION LIFTTIME: 7 days

# path of session list file
PATH_SESSION_FILE = "../data/SESSION.session"

#gernerate session id for better organised data
def generateSessionID():
    x = ''.join(random.sample(string.ascii_letters+string.digits, 32))
    x += ''.join(random.sample(string.ascii_letters+string.digits, 16))
    x += str(time.time()).replace('.','') #add time in case of the same id
    return  x

# this function is used to add a session to the 
# session list file for easy manage
def addSession(sessionid):
    f = open("SESSION.session","a+")
    f.write(sessionid + "," + datetime.datetime.strftime("YY-mm-dd HH:MM:ss") + "\r\n")
    f.close()

# this function is used to delete sessions from the 
# session list file which usally happens when an session out of date 
def deleteSession(sessionids):
    f = open("SESSION.session","w")
    sessiondata = f.read()
    # start delete
    for session in sessionids:
        if sessiondata.find(session) == True:
            sessiondata = sessiondata[:sessiondata.find(session)-1] + \
                            sessiondata[sessiondata.rfind("\r\n",sessiondata.rfind(session)):]
    print(sessiondata)
    f.seek(0)
    f.write(sessiondata)
    f.close()


# this function is used to get all sessions that out of date,
#  we can then delete them easilt later by calling deleteSession() looply
def getOutofDateSessionList():
    ntime = datetime.datetime.now()
    f = open("SESSION.session","r")
    sessiondata = f.read()
    f.close()
    delta = 7 * 3600 * 24
    sessionlist = sessiondata.split("\r\n")
    OOD_list = []
    for session in sessionlist:
        if ntime - datetime.datetime.strptime("YY-mm-dd HH:MM:ss") > delta:
            OOD_list.append(session[0])
    return OOD_list    
    


# code below is used for test if this module works as expect
if __name__ == "__main__":
    test_session_data = """x1,2016-5-6 15:42:30\r\nx2,2017-4-21 6:23:00\r\nx4,2017-6-1 5:42:06"""
    print(test_session_data)
    for session in ["x2"]:
        print(session)
        if test_session_data.find(session) >= 0 :
            print("1")
            test_session_data = test_session_data[:test_session_data.find(session)-1] + \
                                test_session_data[test_session_data.rfind("\n",test_session_data.rfind(session)):]
    print("================")
    print(test_session_data)