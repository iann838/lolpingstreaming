
import os
import sys
from getpass import getuser


def createcmdfile():
    file_path = os.path.dirname(os.path.realpath(__file__))
    # t = r'cd "'+ file_path + '"'
    # s = r'start LoLPingStreaming.exe'
    # with open("startup.bat", "w+") as bat_file:
    #     bat_file.write('@echo off\n')
    #     bat_file.write(t)
    #     bat_file.write('\n')
    #     bat_file.write(s)


def startup(option):
    USER_NAME = getuser()
    file_path = os.path.dirname(os.path.realpath(__file__))
    startup_path = r'C:\Users\%s\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup' % USER_NAME
    createcmdfile()
    # if option:
    #     thirdline = "strArgs = \"\"\"" + file_path + "\\startup.bat\"\"\"\n"
    #     with open(startup_path + r'\LoLPingStreaming.vbs', 'w+') as vbs_file:
    #         vbs_file.write('Set oShell = CreateObject ("Wscript.Shell")\n')
    #         vbs_file.write('Dim strArgs\n')
    #         vbs_file.write(thirdline)
    #         vbs_file.write('oShell.Run strArgs, 0, false')
    # else:
    #     os.chdir(startup_path)
    #     try:
    #         os.remove('LoLPingStreaming.vbs')
    #     except:
    #         pass
    #     os.chdir(file_path)

def findping(out, ind, ip):
    out = str(out)
    on = out.find(ip)
    ping = '10'
    if on == -1:
        ping = '998'
    elif ind >= 3:
        pingindex = out.find('ms', 25)
        ping = out[pingindex - 2:pingindex] if out[pingindex - 3] == '=' else out[pingindex - 3:pingindex]
    return ping



if __name__ == '__main__':
    startup(1)
