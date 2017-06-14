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
PATH_SESSION_FILE = "./data/SESSION.session"
# out of date time, varible below defined the days that an analyzing result 
# will be expired( delete from the server)
VAR_RESULT_LIFE = 7 

#gernerate session id for better organised data
def generateSessionID():
    x = ''.join(random.sample(string.ascii_letters+string.digits, 32))
    x += ''.join(random.sample(string.ascii_letters+string.digits, 16))
    x += str(time.time()).replace('.','') #add time in case of the same id
    return  x

# this function is used to add a session to the 
# session list file for easy manage
def addSession(sessionid):
    f = open(PATH_SESSION_FILE,"a+")
    timestr = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    f.write(sessionid + "," + timestr + "\n")
    f.close()

# this function is used to delete sessions from the 
# session list file which usally happens when an session out of date 
def deleteSession(sessionids):
    f = open(PATH_SESSION_FILE,"a+")
    f.seek(0)
    sessiondata = f.read()
    # start delete
    for session in sessionids:
        print("process session:",session)
        if sessiondata.find(session) > -1:
            sessiondata =  sessiondata[:sessiondata.find(session)-1] + \
                             sessiondata[sessiondata.rfind("\n",sessiondata.rfind(session)):]
    f.seek(0)
    f.truncate()
    f.write(sessiondata)
    f.close()


# this function is used to get all sessions that out of date,
#  we can then delete them easilt later by calling deleteSession() looply
def getOutofDateSessionList():
    ntime = datetime.datetime.now()
    f = open(PATH_SESSION_FILE,"r")
    sessiondata = f.read()
    f.close()
    sessionlist = sessiondata.split("\n")
    OOD_list = []
    for session in sessionlist:
        # skip comment by check if line starting with #
        if session[0] != "#":
            session = session.split(",")
            if (ntime - datetime.datetime.strptime(session[1],"%Y-%m-%d %H:%M:%S")) > datetime.timedelta(VAR_RESULT_LIFE,0,0):
                OOD_list.append(session[0])
    return OOD_list    
    


# code below is used for unit test if this module works as expect
if __name__ == "__main__":
    print ">>>>>>>>>>unit test for SessionManager Module<<<<<<<<<<<"
    PATH_SESSION_FILE = "../data/SESSION.session"
    addSession("aslkjdjkassadj")
    print(getOutofDateSessionList())
    deleteSession(getOutofDateSessionList())
    print(getOutofDateSessionList())
    print ">>>>>>>>>>unit test done for SessionManager Module<<<<<<<<<<<"