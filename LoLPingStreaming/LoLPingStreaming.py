from tkinter import *
import os
from dbfunc import Db as db
from subprocess import Popen
import threading
import sys
from getpass import getuser
from PIL import Image
import pystray
from pystray import MenuItem as item
from time import sleep
from datetime import datetime
from datetime import timedelta
import backendfunc as bf
from helperfunc import subhelp, help
os.environ["PBR_VERSION"] = "4.0.2"
from tendo import singleton
import webbrowser


class App:
    def __init__(self):
        self.today = datetime.today()
        self.names = {131: '  NA  ', 141: ' EUW ', 142: 'EUNE', 156: ' OCE ', 136: ' LAN ', 152: '  BR  ',
                      73: '  RU  ', 128: '  PH  ', 250: '  KR  ', 254: '  JP  ', 165: ' LAS ', 132: '  SG  ',
                      138: '  TW  ', 107: 'CN-T', 117: '  VN  ', 122: '  TH  ', 32: ' PBE ', 111: 'CN-N'}

    def threading(self):
        self.thread = threading.Thread(target=self.start, args=())
        self.thread.setDaemon(True)
        self.thread.start()

    def startthreading(self):
        self.checked = db.getsync()[0]
        self.nextcheck = db.getsync()[1]
        self.needsync = False
        if self.checked == '.' and self.nextcheck == '.':
            self.checked = str(self.today)[:10]
            self.nextcheck = str(self.today + timedelta(days=1))[:10]
            # self.nextcheck = str(self.today)[:10]
            db.updatesyncdate(self.checked, self.nextcheck)
        if self.today > datetime.strptime(self.nextcheck, '%Y-%m-%d'):
            self.needsync = True
        self.cloudthread = threading.Thread(target=self.startcloudconn, args=(self.needsync,))
        self.cloudthread.setDaemon(True)
        self.cloudthread.start()
        self.iconthread = threading.Thread(target=self.starticon, args=())
        self.iconthread.setDaemon(True)
        self.iconthread.start()
        self.threading()

    def startcloudconn(self, needsync):
        sleep(1)
        if needsync:
            # self.runcloud = Popen([r'connfirebase.exe'], **subhelp.subprocess_args(True)).wait()
            # print('finished')
            self.analizeversion()
        else:
            self.analizeversion()
        gui.close.bind('<Button-1>', gui.askclose)
        gui.close.bind('<Enter>', self.onclose)
        gui.close.bind('<Leave>', self.offclose)
        gui.close.config(cursor='hand2')
        gui.close.config(image=gui.closebutt)
        if gui.swin.winfo_exists():
            gui.upicon.bind('<Button-1>', gui.updateinfo)
            gui.upicon.config(cursor='hand2')
        gui.updateunlock = 1

    def analizeversion(self):
        versiontuple = db.getversionsync()
        self.current = versiontuple[0]
        self.lastversion = versiontuple[1]
        self.lastnote = versiontuple[2]
        if self.current != self.lastversion:
            gui.updatestatus = 1
            gui.noti = PhotoImage(file='media/infoicon.png')
            if gui.swin.winfo_exists():
                gui.upicon.config(image=gui.noti)
            gui.updatenotification()

    def onclose(self, event):
        gui.close.config(image=gui.closeon)
    def onsetting(self, event):
        gui.setting.config(image=gui.setton)
    def onhide(self, event):
        gui.hide.config(image=gui.hideon)
    def onminn(self, event):
        gui.minn.config(image=gui.minnon)
    def onunminn(self, event):
        gui.minn.config(image=gui.unminnon)
    def offclose(self, event):
        gui.close.config(image=gui.closebutt)
    def offsetting(self, event):
        gui.setting.config(image=gui.settbutt)
    def offhide(self, event):
        gui.hide.config(image=gui.hidebutt)
    def offminn(self, event):
        gui.minn.config(image=gui.minnbutt)
    def offunminn(self, event):
        gui.minn.config(image=gui.unminnbutt)

    def starticon(self):
        sleep(0.7)
        image = Image.open("media/icon.png")
        menu = pystray.Menu(item('show', gui.show, default=True, visible=False))
        self.icon = pystray.Icon("LoL Ping Streaming", image, "Click to show LoL Ping Streaming", menu)
        self.icon.run()

    def start(self):
        sleep(0.5)
        code = db.getcurrent()[0]
        self.ip = db.getip(code)[0]
        self.p = Popen(['ping', self.ip, '-t'], **subhelp.subprocess_args(True))
        gui.name.config(text=self.names[code])
        with self.p.stdout:
            ping = 0
            stdoutindex = 0
            for line in iter(self.p.stdout.readline, b''):
                print(line)
                stdoutindex += 1
                ping = bf.findping(line, stdoutindex, self.ip)
                self.customcolor(ping)
                gui.ping.config(text=ping)

    def customcolor(self, ping):
        ms = int(ping)
        if ms < 70:
            gui.ping.config(fg='light blue')
            gui.mstext.config(fg='light blue')
        elif ms < 150:
            gui.ping.config(fg='light green')
            gui.mstext.config(fg='light green')
        elif ms < 300:
            gui.ping.config(fg='yellow')
            gui.mstext.config(fg='yellow')
        else:
            gui.ping.config(fg='red')
            gui.mstext.config(fg='red')

    def toggle_startup(self, opt):
        old = db.getcurrent()[2]
        if opt > old:
            bf.startup(1)
        elif opt < old:
            bf.startup(0)
        else:
            pass

    def close(self, *args):
        gui.cwin.destroy()
        gui.cbg.destroy()
        self.p.terminate()
        self.thread.join()
        self.icon.stop()
        self.icon.visible = False
        x= gui.master.winfo_width()
        y= gui.master.winfo_height()
        if x > 100:
            self.animation('x', y, x, 1, gui.master, 5, 8, sys.exit)
        else:
            self.animation('y', x, y, 1, gui.master, 5, 8, sys.exit)

    def hardreset(self):
        self.resetthread = threading.Thread(target=self.resetting, args=())
        self.resetthread.setDaemon(True)
        self.resetthread.start()

    def resetting(self):
        self.p.terminate()
        self.toggle_startup(0)
        os.remove('testerdata.db')
        db.startup()
        gui.newsettings(1)
        app.p.terminate()
        app.threading()
        gui.rwin.destroy()
        gui.cbg.destroy()
        app.animation('y', 138, 399, 1, gui.swin, 28, 18, gui.settingsclose)


    def animation(self, axis, cons, start, end, window, shot, time, func=None):
        self.startframe = start
        if axis == 'x':
            if self.startframe < end:
                def xslideout():
                    self.startframe += shot
                    if self.startframe < end:
                        window.geometry('%sx%s' % (self.startframe, cons))
                        gui.master.after(time, xslideout)
                    else:
                        window.geometry('%sx%s' % (end, cons))
                        if func:
                            func()
                xslideout()
            else:
                def xslidein():
                    self.startframe -= shot
                    if self.startframe > end:
                        window.geometry('%sx%s' % (self.startframe, cons))
                        gui.master.after(time, xslidein)
                    else:
                        window.geometry('%sx%s' % (end, cons))
                        if func:
                            func()
                xslidein()
        elif axis == 'y':
            if self.startframe < end:
                def yslideout():
                    self.startframe += shot
                    if self.startframe < end:
                        window.geometry('%sx%s' % (cons, self.startframe))
                        gui.master.after(time, yslideout)
                    else:
                        window.geometry('%sx%s' % (cons, end))
                        if func:
                            func()
                yslideout()
            else:
                def yslidein():
                    self.startframe -= shot
                    if self.startframe > end:
                        window.geometry('%sx%s' % (cons, self.startframe))
                        gui.master.after(time, yslidein)
                    else:
                        window.geometry('%sx%s' % (cons, end))
                        if func:
                            func()
                yslidein()


    def minnani(self):
        self.mx = 138 ##to 39
        self.my = 52 ##to 118
        def ani():
            self.mx -= 11
            self.my += 7
            gui.master.geometry('%sx%s' %(self.mx,self.my))
            if self.mx-11 > 39:
                gui.master.after(15, ani)
            else:
                gui.master.geometry('39x118')
        ani()

    def unminnani(self):
        self.mx = 39
        self.my = 118
        def ani():
            self.mx += 11
            self.my -= 7
            gui.master.geometry('%sx%s' %(self.mx,self.my))
            if self.mx+11 < 138:
                gui.master.after(15, ani)
            else:
                gui.master.geometry('138x52')
        ani()

    def createframes(self):
        self.frames = []
        self.vframes = []
        stt = True
        index = 0
        while stt:
            try:
                self.frames.append(PhotoImage(file='media/flame.gif', format='gif -index ' + str(index)))
                self.vframes.append(PhotoImage(file='media/verticalflame.gif', format='gif -index ' + str(index)))
                index += 1
            except Exception:
                index = 0
                stt = False

    def openpatreon(self, event):
        url = "https://www.patreon.com/paaksing"
        webbrowser.open(url, new=0, autoraise=True)
        self.animation('y', 138, 399, 1, gui.swin, 28, 18, gui.settingsclose)


class Gui:
    def __init__(self, master):
        master.title('LoL Ping Streaming (vers. 1.0)')
        master.overrideredirect(1)

        master.geometry('+%s+%s' % db.getpos())
        master.resizable(False, False)
        master.attributes('-topmost', db.getcurrent()[1])

        self.updatestatus = 0
        self.updateunlock = 0
        self.minngoing = 0
        self.isminn = db.getminn()

        self.master = master
        self.swin = Toplevel(self.master, bg='#000912')
        self.swin.destroy()
        self.gwin = Toplevel(self.master, bg='#000912')
        self.gwin.destroy()
        self.cwin = Toplevel(self.master, bg='#000912')
        self.cwin.destroy()
        self.rwin = Toplevel(self.master, bg='#000912')
        self.rwin.destroy()
        self.uwin = Toplevel(self.master, bg='#000912')
        self.uwin.destroy()
        self.cbg = Toplevel(self.master, bg='#000912')
        self.cbg.destroy()

        self.master.bind('<Button-1>', self.show)

        self.line = Frame(master, bg='#785b28', height=2)
        self.line.pack(side='top', fill=X)

        self.top = Frame(master, bg='#000912')
        self.top.option_add('*Label.Background', '#000912')
        self.top.pack(side='top', fill=X)

        self.pinglabel = PhotoImage(file='media/ping.png')
        self.title = Label(self.top, image=self.pinglabel)
        self.title.pack(side='left', padx=(10, 0))
        self.title.bind("<ButtonPress-1>", self.StartMove)
        self.title.bind("<ButtonRelease-1>", self.StopMove)
        self.title.bind("<B1-Motion>", self.OnMotion)

        self.closebutt = PhotoImage(file='media/close.png')
        self.closeon = PhotoImage(file='media/lightclose.png')
        self.closeoff = PhotoImage(file='media/closeoff.png')
        self.close = Label(self.top, image=self.closeoff, cursor='watch', bd=0)
        self.close.pack(side='right', padx=(0, 2))

        self.settbutt = PhotoImage(file='media/settings.png')
        self.setton = PhotoImage(file='media/lightsettings.png')
        self.settoff = PhotoImage(file='media/settingsoff.png')
        self.setting = Label(self.top, image=self.settbutt, cursor='hand2', bd=0)
        self.setting.pack(side='right')
        self.setting.bind('<Button-1>', self.settings)
        self.setting.bind('<Enter>', app.onsetting)
        self.setting.bind('<Leave>', app.offsetting)

        self.hidebutt = PhotoImage(file='media/hidebutt.png')
        self.hideon = PhotoImage(file='media/lighthidebutt.png')
        self.hide = Label(self.top, image=self.hidebutt, cursor='hand2', bd=0)
        self.hide.pack(side='right')
        self.hide.bind('<Button-1>', self.hidewin)
        self.hide.bind('<Enter>', app.onhide)
        self.hide.bind('<Leave>', app.offhide)
        self.hideeventlock = 0

        self.minnbutt = PhotoImage(file='media/vertical.png')
        self.minnon = PhotoImage(file='media/lightvertical.png')
        self.unminnbutt = PhotoImage(file='media/unvertical.png')
        self.unminnon = PhotoImage(file='media/lightunvertical.png')
        self.minn = Label(self.top, image=self.minnbutt, cursor='hand2', bd=0)
        self.minn.pack(side='right')
        self.minn.bind('<Button-1>', self.minnwin)
        self.minn.bind('<Enter>', app.onminn)
        self.minn.bind('<Leave>', app.offminn)

        self.midline = Frame(master, bg='#1a212b', height=1.5)
        self.midline.pack(side='top', fill=X)

        self.line = Frame(self.master, bg='#785b28', height=1)
        self.line.pack(side='bottom', fill=X)

        self.bot = Frame(master, bg='#010102')
        self.bot.pack(side='bottom', fill=BOTH, expand=TRUE)

        self.xline = Frame(self.bot, bg='#1a212b', height=1.5)
        self.xline2 = Frame(self.top, bg='#1a212b', height=1.5)

        self.mstext = Label(self.bot, text='ms', font='Helvetica 12 bold', fg='white', bg='#010102')
        self.mstext.pack(side='right', padx=(0, 3))
        self.ping = Label(self.bot, text='0', font='Helvetica 12 bold', fg='white', bg='#010102')
        self.ping.pack(side='right', padx=(13, 0))

        self.name = Label(self.bot, text=' ----- ', fg='light blue', font='Helvetica 6 bold')
        self.name.pack(side='left', fill=Y, padx=(3,3))
        self.sep = Frame(self.bot, bg='#1a212b', width=2)
        self.sep.pack(side='left', fill=Y)

        self.noti = PhotoImage(file='media/offinfoicon.png')
        self.iconnoti = Label(self.bot, bd=0)
        self.iconnoti.place(x=50, y=3)
        self.iconnoti.lower()

        app.createframes()
        self.ani = Label(self.bot, image=app.frames[0])
        self.ani.photo = app.frames[0]
        self.ani.pack(side='right')

        self.vani = Label(self.bot, image=app.vframes[0], bd=0)
        self.vani.photo = app.vframes[0]

        index = 0
        def update(ind):
            if ind == len(app.frames) - 1:
                ind = 0
            frame = app.frames[ind]
            vframe = app.vframes[ind]
            ind += 1
            self.ani.config(image=frame)
            self.vani.config(image=vframe)
            self.master.after(35, update, ind)
        update(index)

        self.openx = 1
        def startani():
            self.openx += 10
            if self.openx < 138:
                master.geometry('%sx52'% self.openx)
                master.after(15, startani)
            else:
                master.geometry('138x52')
                if self.isminn:
                    db.updateminn(0)
                    self.minnwin()
        startani()

        app.startthreading()

    def hidewin(self, event):
        self.hideeventlock = 1
        self.master.withdraw()
        if self.swin.winfo_exists():
            self.swin.withdraw()

    def minnwin(self, *args):
        if not db.getminn():
            self.minngoing = 1
            db.updateminn(1)
            self.title.pack_forget()
            self.close.pack_forget()
            self.setting.pack_forget()
            self.hide.pack_forget()
            self.minn.pack_forget()
            self.name.pack_forget()
            self.sep.pack_forget()
            self.ani.pack_forget()
            self.ping.pack_forget()
            self.mstext.pack_forget()
            self.iconnoti.place_forget()

            if self.swin.winfo_exists():
                app.animation('y', 138, 399, 1, self.swin, 28, 18, self.settingsclose)
            else:
                app.minnani()

            self.title.pack(side='top', pady=(3,0), padx=(2,0))
            self.xline2.pack(side='top', fill=X)
            self.close.pack(side='left')
            self.minn.config(image=self.unminnbutt)
            self.minn.unbind('<Enter>')
            self.minn.unbind('<Leave>')
            self.minn.bind('<Enter>', app.onunminn)
            self.minn.bind('<Leave>', app.offunminn)
            self.minn.pack(side='left')
            self.name.pack(side='top', fill=X, pady=(2,2))
            self.xline.pack(side='top', fill=X)
            self.ping.pack(side='bottom', pady=(3,0))
            self.vani.pack(side='bottom')
            self.iconnoti.place(x=10, y=28)
        else:
            self.minngoing = 0
            db.updateminn(0)
            self.title.pack_forget()
            self.hide.pack_forget()
            self.minn.pack_forget()
            self.name.pack_forget()
            self.xline2.pack_forget()
            self.xline.pack_forget()
            self.ping.pack_forget()
            self.vani.pack_forget()
            self.iconnoti.place_forget()

            app.unminnani()
            self.title.pack(side='left', padx=(10, 0))
            self.close.pack(side='right', padx=(0, 2))
            self.setting.pack(side='right')
            self.hide.pack(side='right')
            self.minn.config(image=self.minnbutt)
            self.minn.unbind('<Enter>')
            self.minn.unbind('<Leave>')
            self.minn.bind('<Enter>', app.onminn)
            self.minn.bind('<Leave>', app.offminn)
            self.minn.pack(side='right')
            self.mstext.pack(side='right', padx=(0, 3))
            self.ping.pack(side='right', padx=(13, 0))
            self.name.pack(side='left', fill=Y, padx=(3,3))
            self.sep.pack(side='left', fill=Y)
            self.ani.pack(side='left')
            self.iconnoti.place(x=50, y=3)

    def show(self, *args):
        if db.getcurrent()[1] == 0:
            self.master.attributes('-topmost', 1)
            self.master.attributes('-topmost', 0)
            if self.swin.winfo_exists():
                self.swin.attributes('-topmost', 1)
                self.swin.attributes('-topmost', 0)
            if self.cbg.winfo_exists():
                self.cbg.attributes('-topmost', 1)
                self.cbg.attributes('-topmost', 0)
            if self.gwin.winfo_exists():
                self.gwin.attributes('-topmost', 1)
                self.gwin.attributes('-topmost', 0)
            if self.uwin.winfo_exists():
                self.uwin.attributes('-topmost', 1)
                self.uwin.attributes('-topmost', 0)
            if self.cwin.winfo_exists():
                self.cwin.attributes('-topmost', 1)
                self.cwin.attributes('-topmost', 0)
            if self.rwin.winfo_exists():
                self.rwin.attributes('-topmost', 1)
                self.rwin.attributes('-topmost', 0)
        else:
            if self.cbg.winfo_exists():
                self.cbg.attributes('-topmost', 1)
            if self.gwin.winfo_exists():
                self.gwin.attributes('-topmost', 1)
            if self.uwin.winfo_exists():
                self.uwin.attributes('-topmost', 1)
            if self.cwin.winfo_exists():
                self.cwin.attributes('-topmost', 1)
            if self.rwin.winfo_exists():
                self.rwin.attributes('-topmost', 1)
        if not self.master.winfo_viewable() and self.hideeventlock == 0:
            self.master.deiconify()
            if self.swin.winfo_exists():
                self.swin.deiconify()
        self.hideeventlock = 0

    def StartMove(self, event):
        self.x = event.x
        self.y = event.y

    def StopMove(self, event):
        self.x = None
        self.y = None
        db.updatepos(self.master.winfo_x(), self.master.winfo_y())

    def OnMotion(self, event):
        deltax = event.x - self.x
        deltay = event.y - self.y
        x = self.master.winfo_x() + deltax
        y = self.master.winfo_y() + deltay
        self.master.geometry("+%s+%s" % (x, y))
        if self.swin.winfo_exists():
            self.swin.geometry("+%s+%s" % (x, y + 52))
        if self.gwin.winfo_exists():
            self.gwin.geometry("+%s+%s" % (x + 10, y + 52))
        if self.cbg.winfo_exists():
            self.cbg.geometry("+%s+%s" % (x, y))
        if self.cwin.winfo_exists():
            self.cwin.geometry("+%s+%s" % (x + 9, y + 15))
        if self.rwin.winfo_exists():
            self.rwin.geometry("+%s+%s" % (x + 15, y + 197))
        if self.uwin.winfo_exists():
            if self.updatestatus:
                self.uwin.geometry("+%s+%s" % (x + 10, y + 50))
            else:
                self.uwin.geometry("+%s+%s" % (x + 10, y + 120))

    def blackout(self):
        self.cbg = Toplevel(self.master, bg='black')
        self.cbg.overrideredirect(1)
        self.cbg.resizable(False, False)
        self.cbg.bind('<Button-1>', self.show)
        if self.swin.winfo_exists():
            self.cbg.geometry('138x451')
            self.whiteblock = Frame(self.cbg, bg='white', bd=0, width=39, height=23)
            self.whiteblock.pack(side='top', anchor='w', padx=(10, 0))
        elif self.master.winfo_width() > 100:
            self.cbg.geometry('138x52')
            self.whiteblock = Frame(self.cbg, bg='white', bd=0, width=39, height=23)
            self.whiteblock.pack(side='top', anchor='w', padx=(10, 0))
        else:
            self.cbg.geometry('39x118')
            self.whiteblock = Frame(self.cbg, bg='white', bd=0, width=39, height=20)
            self.whiteblock.pack(side='top', anchor='w')
        self.cbg.geometry('+%s+%s' % (self.master.winfo_x(), self.master.winfo_y()))
        self.cbg.attributes('-alpha', 0.7)
        self.cbg.attributes('-transparentcolor', 'white')
        self.cbg.attributes('-topmost', db.getcurrent()[1])

    def askclose(self, *args):
        self.cwin = Toplevel(self.master, bg='#000912')
        self.cwin.overrideredirect(1)
        self.cwin.resizable(False, False)
        self.cwin.attributes('-topmost', db.getcurrent()[1])
        self.cwin.bind('<Button-1>', self.show)

        self.cline = Frame(self.cwin, bg='#785b28', height=1)
        self.cline.pack(side='top', fill=X)

        self.askframe = Frame(self.cwin, bg='#000912')
        self.askframe.pack(side='top')
        self.exitlabel = Label(self.askframe, text='Exit?', fg='light gray', bg='#000912', font='Helvetica 8 bold',
                               bd=0)

        self.yes = PhotoImage(file='media/closeyes.png')
        self.no = PhotoImage(file='media/closeno.png')
        self.exityes = Label(self.askframe, image=self.yes, bd=0, cursor='hand2')
        self.exityes.bind('<Button-1>', app.close)
        self.exitno = Label(self.askframe, image=self.no, bd=0, cursor='hand2')
        self.exitno.bind('<Button-1>', self.returnmain)

        self.cline2 = Frame(self.cwin, bg='#785b28', height=2)
        self.cline2.pack(side='bottom', fill=X)

        if self.master.winfo_width() > 100:
            app.animation('x', 33, 1, 88, self.cwin, 10, 10)
            self.cwin.geometry('+%s+%s' % (self.master.winfo_x() + 25, self.master.winfo_y() + 12))
            self.exitlabel.pack(side='left', padx=(5, 0), pady=(5, 5))
            self.exityes.pack(side='left', padx=(5, 2), pady=(5, 5))
            self.exitno.pack(side='left', padx=(0, 5), pady=(5, 5))
        else:
            app.animation('y', 30, 1, 88, self.cwin, 10, 10)
            self.cwin.geometry('+%s+%s' % (self.master.winfo_x() + 5, self.master.winfo_y() + 15))
            self.exitlabel.pack(side='top', anchor='center', pady=(8, 0))
            self.exityes.pack(side='top', anchor='center', pady=(8, 1))
            self.exitno.pack(side='top', anchor='center', pady=(1, 5))

        if self.swin.winfo_exists():
            app.animation('y', 138, 399, 1, self.swin, 28, 18, self.settingsclose)
        else:
            self.blackout()

    def settingsclose(self):
        self.swin.destroy()
        self.setting.bind('<Button-1>', self.settings)
        self.setting.config(cursor='hand2')
        self.setting.config(image=self.settbutt)
        self.setting.bind('<Enter>', app.onsetting)
        self.setting.bind('<Leave>', app.offsetting)
        if self.minngoing:
            self.minngoing = 0
            app.minnani()
        if self.cwin.winfo_exists():
            self.blackout()
            self.cwin.lift(aboveThis=self.cbg)

    def returnmain(self, event):
        if self.rwin.winfo_exists():
            app.animation('y', 108, 80, 1, self.rwin, 10, 15, self.closerwin)
        elif self.uwin.winfo_exists():
            if self.updatestatus:
                app.animation('y', 120, 399, 1, self.uwin, 15, 8, self.uwinexit)
            else:
                app.animation('y', 120, 210, 1, self.uwin, 15, 8, self.uwinexit)
        elif self.gwin.winfo_exists():
            self.guideexit.unbind('<Button-1>')
            app.animation('y', 120, 399, 1, self.gwin, 15, 8, self.gwinexit)
        elif self.cwin.winfo_exists():
            if self.master.winfo_width() > 100:
                app.animation('x', 33, 88, 1, self.cwin, 10, 15, self.closecwin)
            else:
                app.animation('y', 30, 88, 1, self.cwin, 10, 15, self.closecwin)

    def closerwin(self):
        self.rwin.destroy()
        self.cbg.destroy()

    def closecwin(self):
        self.cwin.destroy()
        self.cbg.destroy()

    def gwinexit(self):
        self.gwin.destroy()
        self.cbg.destroy()

    def uwinexit(self):
        self.uwin.destroy()
        self.cbg.destroy()

    def settings(self, *args):
        self.setting.unbind('<Button-1>')
        self.setting.unbind('<Enter>')
        self.setting.unbind('<Leave>')
        self.setting.config(cursor='arrow')
        self.setting.config(image=self.settoff)
        self.swin = Toplevel(self.master, bg='#000912')
        self.swin.overrideredirect(1)
        self.swin.resizable(False, False)
        self.swin.geometry('139x1')
        self.swin.geometry('+%s+%s' % (self.master.winfo_x(), self.master.winfo_y() + 52))

        app.animation('y', 138, 1, 399, self.swin, 28, 18)

        self.swin.attributes('-topmost', db.getcurrent()[1])
        self.swin.bind('<Button-1>', self.show)

        self.stitle = Label(self.swin, text='Servers:', font='Helvetica 8 bold', bd=1, fg='light green')
        self.stitle.pack(side='top', anchor='w', padx=(6, 0), pady=(5, 0))

        self.server = Frame(self.swin, bg='#000912')
        self.server.pack(side='top', fill=X, padx=(8, 5))
        self.server.grid_columnconfigure(0, weight=1)
        self.server.grid_columnconfigure(1, weight=1)
        self.server.grid_columnconfigure(2, weight=1)
        self.server.grid_rowconfigure(0, weight=1)
        self.server.grid_rowconfigure(1, weight=1)
        self.server.grid_rowconfigure(2, weight=1)
        self.server.grid_rowconfigure(3, weight=1)
        self.server.grid_rowconfigure(4, weight=1)
        self.server.grid_rowconfigure(5, weight=1)
        self.server.grid_rowconfigure(6, weight=1)
        self.server.grid_rowconfigure(7, weight=1)
        self.server.grid_rowconfigure(8, weight=1)
        self.server.grid_rowconfigure(9, weight=1)
        self.server.grid_rowconfigure(9, weight=1)
        self.server.option_add('*Radiobutton.Background', '#000912')
        self.server.option_add('*Radiobutton.Foreground', 'light gray')

        self.code = IntVar()

        self.official = Label(self.server, text='-League Direct:', font='Helvetica 7 bold', bg='#000912',
                              fg='sky blue')
        self.official.grid(row=0, columnspan=3, sticky='w')
        self.na = Radiobutton(self.server, text='NA', variable=self.code, font='Helvetica 6 bold', value=131, bd=0,
                              activebackground='#000912')
        self.na.grid(row=1, column=0, sticky='w')
        self.lan = Radiobutton(self.server, text='LAN', variable=self.code, font='Helvetica 6 bold', value=136, bd=0,
                               activebackground='#000912')
        self.lan.grid(row=1, column=1, sticky='w')
        self.ph = Radiobutton(self.server, text='PH', variable=self.code, font='Helvetica 6 bold', value=128, bd=0,
                              activebackground='#000912')
        self.ph.grid(row=1, column=2, sticky='w')
        self.euw = Radiobutton(self.server, text='EUW', variable=self.code, font='Helvetica 6 bold', value=141, bd=0,
                               activebackground='#000912')
        self.euw.grid(row=2, column=0, sticky='w')
        self.eune = Radiobutton(self.server, text='EUNE', variable=self.code, font='Helvetica 6 bold', value=142, bd=0,
                                activebackground='#000912')
        self.eune.grid(row=2, column=1, sticky='w')
        self.br = Radiobutton(self.server, text='BR', variable=self.code, font='Helvetica 6 bold', value=152, bd=0,
                              activebackground='#000912')
        self.br.grid(row=2, column=2, sticky='w')
        self.ru = Radiobutton(self.server, text='RU', variable=self.code, font='Helvetica 6 bold', value=73, bd=0,
                              activebackground='#000912')
        self.ru.grid(row=3, column=0, sticky='w')
        self.oce = Radiobutton(self.server, text='OCE', variable=self.code, font='Helvetica 6 bold', value=156, bd=0,
                               activebackground='#000912')
        self.oce.grid(row=3, column=1, sticky='w')
        self.vn = Radiobutton(self.server, text='VN', variable=self.code, font='Helvetica 6 bold', value=117, bd=0,
                              activebackground='#000912')
        self.vn.grid(row=3, column=2, sticky='w')

        self.unofficial = Label(self.server, text='-Regional Average:', font='Helvetica 7 bold', bg='#000912',
                                fg='sky blue')
        self.unofficial.grid(row=4, columnspan=3, sticky='w')
        self.las = Radiobutton(self.server, text='LAS', variable=self.code, font='Helvetica 6 bold', value=165, bd=0,
                               activebackground='#000912')
        self.las.grid(row=5, column=0, sticky='w')
        self.kr = Radiobutton(self.server, text='KR', variable=self.code, font='Helvetica 6 bold', value=250, bd=0,
                              activebackground='#000912')
        self.kr.grid(row=5, column=1, sticky='w')
        self.jp = Radiobutton(self.server, text='JP', variable=self.code, font='Helvetica 6 bold', value=254, bd=0,
                              activebackground='#000912')
        self.jp.grid(row=5, column=2, sticky='w')
        self.tw = Radiobutton(self.server, text='TW', variable=self.code, font='Helvetica 6 bold', value=138, bd=0,
                              activebackground='#000912')
        self.tw.grid(row=6, column=0, sticky='w')
        self.sg = Radiobutton(self.server, text='SG', variable=self.code, font='Helvetica 6 bold', value=132, bd=0,
                              activebackground='#000912')
        self.sg.grid(row=6, column=1, sticky='w')
        self.th = Radiobutton(self.server, text='TH', variable=self.code, font='Helvetica 6 bold', value=122, bd=0,
                              activebackground='#000912')
        self.th.grid(row=6, column=2, sticky='w')
        self.pbe = Radiobutton(self.server, text='PBE', variable=self.code, font='Helvetica 6 bold', value=32, bd=0,
                               activebackground='#000912')
        self.pbe.grid(row=7, column=0, sticky='w')

        self.china = Label(self.server, text='-China Network:', font='Helvetica 7 bold', bg='#000912', fg='sky blue')
        self.china.grid(row=8, columnspan=3, sticky='w')
        self.cn1 = Radiobutton(self.server, text='TELECOM CN (CN-T)', variable=self.code, font='Helvetica 6 bold',
                               value=107, bd=0, activebackground='#000912')
        self.cn1.grid(row=9, columnspan=3, sticky='w')
        self.cn2 = Radiobutton(self.server, text='NETCOM CN (CN-N)', variable=self.code, font='Helvetica 6 bold',
                               value=111, bd=0, activebackground='#000912')
        self.cn2.grid(row=10, columnspan=3, sticky='w')

        self.code.set(db.getcurrent()[0])

        self.title2 = Label(self.swin, text='Options:',bd=1, font='Helvetica 8 bold', fg='light green')
        self.title2.pack(side='top', anchor='w', padx=(6, 5))

        self.options = Frame(self.swin, bg='#000912')
        self.options.pack(side='top', fill=X, padx=(8, 8), pady=(5, 1))
        self.options.option_add('*Checkbutton.Background', '#000912')
        self.options.option_add('*Checkbutton.Foreground', 'light gray')

        self.topmost = IntVar()
        self.topmostcheck = Checkbutton(self.options, text="Force on top", variable=self.topmost,
                                        font='Helvetica 7 bold', bd=0, activebackground='#000912')
        self.topmostcheck.pack(side='top', anchor='w')
        self.topmost.set(db.getcurrent()[1])

        self.startup = IntVar()
        self.startupcheck = Checkbutton(self.options, text="Run at Startup", justify='left', variable=self.startup,
                                        font='Helvetica 7 bold', bd=0, activebackground='#000912', )
        self.startupcheck.pack(side='top', anchor='w')
        self.startup.set(db.getcurrent()[2])

        self.title3 = Label(self.swin, text='Help:', bd=1, font='Helvetica 8 bold', fg='light green')
        self.title3.pack(side='top', anchor='w', padx=(6, 5))

        self.guide = Frame(self.swin, bg='#000912')
        self.guide.pack(side='top', fill=X, padx=(10, 5))
        self.guideimg = PhotoImage(file='media/guideicon.png')
        self.guideicon = Label(self.guide, image=self.guideimg, bg='#000912', cursor='question_arrow', bd=0)
        self.guideicon.pack(side='left', pady=(2, 0))
        self.guidetext = Label(self.guide, text="About App", font='Helvetica 7 bold', fg='light gray',
                               bg='#000912')
        self.guidetext.pack(side='left', pady=(3, 0))
        self.guideicon.bind('<Button-1>', self.showguide)

        self.resetf = Frame(self.swin, bg='#000912')
        self.resetf.pack(side='top', fill=X, padx=(10, 5))
        self.resetimg = PhotoImage(file='media/reseticon.png')
        self.reseticon = Label(self.resetf, image=self.resetimg, bg='#000912', cursor='hand2', bd=0)
        self.reseticon.pack(side='left', pady=(2, 0))
        self.resetcheck = Label(self.resetf, text="Reset program", font='Helvetica 7 bold', fg='light gray',
                                bg='#000912')
        self.resetcheck.pack(side='left', pady=(3, 0))
        self.reseticon.bind('<Button-1>', self.askreset)

        self.upf = Frame(self.swin, bg='#000912')
        self.upf.pack(side='top', fill=X, padx=(10, 5))
        self.upicon = Label(self.upf, image=self.noti, bg='#000912', cursor='watch', bd=0)
        self.upicon.pack(side='left', pady=(2, 0))
        self.upcheck = Label(self.upf, text="Update check", font='Helvetica 7 bold', fg='light gray', bg='#000912')
        self.upcheck.pack(side='left', pady=(3, 0))
        if self.updateunlock:
            self.upicon.config(cursor='hand2')
            self.upicon.bind('<Button-1>', self.updateinfo)

        self.suppf = Frame(self.swin, bg='#000912')
        self.suppf.pack(side='top', fill=X, padx=(10, 5))
        self.suppimg = PhotoImage(file='media/supporticon.png')
        self.suppicon = Label(self.suppf, image=self.suppimg, bg='#000912', cursor='hand2', bd=0)
        self.suppicon.pack(side='left', pady=(2, 0))
        self.suppcheck = Label(self.suppf, text="Support creator\n on Patreon", bd=0, font='Helvetica 7 bold', fg='light gray',
                                bg='#000912', justify='left')
        self.suppcheck.pack(side='left', pady=(3, 0))
        self.suppicon.bind('<Button-1>', app.openpatreon)

        self.endline = Frame(self.swin, bg='#785b28', height=2)
        self.endline.pack(side='bottom', fill=X)

        self.done = PhotoImage(file='media/DONE.png')
        self.apply = Label(self.swin, image=self.done, cursor='hand2', bd=0)
        self.apply.pack(side='bottom')
        self.apply.bind('<Button-1>', self.applysettings)

    def applysettings(self, event):
        code = self.code.get()
        topmost = self.topmost.get()
        startup = self.startup.get()
        app.toggle_startup(startup)
        db.updatecurrent(code, topmost, startup)
        self.newsettings(topmost)
        app.animation('y', 138, 399, 1, self.swin, 28, 18, self.settingsclose)
        app.p.terminate()
        self.ping.config(text='10')
        self.ping.config(fg='light blue')
        self.name.config(text=' ---- ')
        app.threading()

    def newsettings(self, topmost):
        if topmost == 1:
            self.master.attributes('-topmost', True)
        else:
            self.master.attributes('-topmost', False)

    def updatenotification(self):
        self.iconnoti.config(image=self.noti)
        self.iconnoti.config(cursor='hand2')
        self.iconnoti.lift()
        self.iconnoti.bind('<Button-1>', self.shortcuttouwin)

    def shortcuttouwin(self, event):
        if self.master.winfo_width() > 100:
            if not self.swin.winfo_exists():
                self.settings()
            self.updateinfo()
            self.swin.lift()
        else:
            self.minnwin()
            def go():
                self.settings()
                self.updateinfo()
                self.swin.lift()
            self.master.after(138, go)

    def updateinfo(self, *args):
        self.uwin = Toplevel(self.master, bg='#000912')
        self.uwin.overrideredirect(1)
        self.uwin.resizable(False, False)
        self.uwin.attributes('-topmost', db.getcurrent()[1])
        self.uwin.bind('<Button-1>', self.show)
        self.uchecked = db.getsync()[0]
        self.unextcheck = db.getsync()[1]
        if self.updatestatus:
            app.animation('y', 120, 1, 399, self.uwin, 15, 5)
            self.uwin.geometry('+%s+%s' % (self.master.winfo_x() + 10, self.master.winfo_y() + 50))

            self.uline = Frame(self.uwin, bg='#785b28', height=1)
            self.uline.pack(side='top', fill=X)

            self.ulabel = Label(self.uwin, text='Update\nAvailable', font='Helvetica 10 bold', fg='light green',
                                bg='#000912', justify='left')
            self.ulabel.pack(side='top', pady=(5, 5), padx=(5, 5), anchor='w')

            self.current = Label(self.uwin, text='Current version:\n' + app.current, font='Helvetica 7 bold',
                                 fg='light gray', bg='#000912', bd=0, justify='left')
            self.current.pack(side='top', padx=(8, 8), anchor='w')
            self.last = Label(self.uwin, text='Last version:\n' + app.lastversion, font='Helvetica 7 bold',
                              fg='light gray', bg='#000912', bd=0, justify='left')
            self.last.pack(side='top', padx=(8, 8), anchor='w')
            self.lastcheck = Label(self.uwin, text='Checked at:\n' + self.uchecked, font='Helvetica 7 bold',
                                   fg='light gray', bg='#000912', bd=0, justify='left')
            self.lastcheck.pack(side='top', padx=(8, 8), anchor='w')

            self.utitle = Label(self.uwin, text='Version note:', font='Helvetica 10 bold', fg='light green',
                                bg='#000912', justify='left')
            self.utitle.pack(side='top', pady=(5, 5), padx=(5, 5), anchor='w')

            self.newnote = Text(self.uwin, bg='#01070d', bd=2, relief=FLAT, font='Helvetica 7 bold', fg='light gray',
                                wrap=WORD, height=12, highlightthickness=1, highlightbackground='#1a212b')
            self.newnote.pack(side='top', padx=(8, 8), anchor='w')
            self.newnote.insert(INSERT, app.lastnote)
        else:
            app.animation('y', 120, 1, 210, self.uwin, 15, 5)
            self.uwin.geometry('+%s+%s' % (self.master.winfo_x() + 10, self.master.winfo_y() + 120))

            self.uline = Frame(self.uwin, bg='#785b28', height=1)
            self.uline.pack(side='top', fill=X)
            self.ulabel = Label(self.uwin, text='Version\nup to date:', font='Helvetica 10 bold', fg='light green',
                                bg='#000912', justify='left')
            self.ulabel.pack(side='top', pady=(5, 5), padx=(5, 5), anchor='w')
            self.current = Label(self.uwin, text='Current version:\n' + app.current, font='Helvetica 7 bold',
                                 fg='light gray', bg='#000912', bd=0, justify='left')
            self.current.pack(side='top', padx=(8, 8), anchor='w')
            self.last = Label(self.uwin, text='Last version:\n' + app.lastversion, font='Helvetica 7 bold',
                              fg='light gray', bg='#000912', bd=0, justify='left')
            self.last.pack(side='top', padx=(8, 8), anchor='w')
            self.lastcheck = Label(self.uwin, text='Checked at:\n' + self.uchecked, font='Helvetica 7 bold',
                                   fg='light gray', bg='#000912', bd=0, justify='left')
            self.lastcheck.pack(side='top', padx=(8, 8), anchor='w')
            self.nextcheck = Label(self.uwin, text='Next check:\n' + self.unextcheck, font='Helvetica 7 bold',
                                   fg='light gray', bg='#000912', bd=0, justify='left')
            self.nextcheck.pack(side='top', padx=(8, 8), anchor='w')

        self.uline2 = Frame(self.uwin, bg='#785b28', height=2)
        self.uline2.pack(side='bottom', fill=X)
        self.done1 = PhotoImage(file='media/DONE.png')
        self.closeupdate = Label(self.uwin, image=self.done1, cursor='hand2', bd=0)
        self.closeupdate.pack(side='bottom')
        self.closeupdate.bind('<Button-1>', self.returnmain)
        self.uinfo2 = Label(self.uwin, text='*You can check updates\nfrom patreon posts', font='Helvetica 7',
                            bg='#000912', fg='gray')
        self.uinfo2.pack(side='bottom', pady=(5, 10), padx=(5, 5))
        self.uinfo = Label(self.uwin, text='*The program will check\nfor update every 7 days.', font='Helvetica 7',
                           bg='#000912', fg='gray')
        self.uinfo.pack(side='bottom', pady=(5, 0), padx=(5, 5))
        self.blackout()

    def startreset(self, event):
        self.master.after(128, app.hardreset)
        self.resetyes.pack_forget()
        self.resetno.pack_forget()
        self.rlabel.config(text='Resetting...\nPlease wait')
        self.rlabel.pack_forget()
        self.rlabel.pack(side='top', pady=(5, 5))
        self.ping.config(text='10')
        self.ping.config(fg='light blue')
        self.name.config(text=' ------ ')

    def askreset(self, *args):
        self.rwin = Toplevel(self.master, bg='#000912')
        self.rwin.overrideredirect(1)
        self.rwin.resizable(False, False)
        app.animation('y', 108, 1, 80, self.rwin, 10, 15)
        self.rwin.geometry('+%s+%s' % (self.master.winfo_x() + 15, self.master.winfo_y() + 197))
        self.rwin.attributes('-topmost', db.getcurrent()[1])
        self.rwin.bind('<Button-1>', self.show)

        self.rline = Frame(self.rwin, bg='#785b28', height=1)
        self.rline.pack(side='top', fill=X)

        self.rlabel = Label(self.rwin, text='Are you sure\nto reset program to\ndefault values?', fg='light gray',
                            bg='#000912', font='Helvetica 7 bold', bd=0)
        self.rlabel.pack(side='top', pady=(5, 5))

        self.askresetframe = Frame(self.rwin, bg='#000912')
        self.askresetframe.pack(side='top')
        self.ryes = PhotoImage(file='media/yes.png')
        self.rno = PhotoImage(file='media/no.png')
        self.resetyes = Label(self.askresetframe, image=self.ryes, bd=0, cursor='hand2')
        self.resetyes.pack(side='left', pady=(5, 5), padx=(0, 2))
        self.resetyes.bind('<Button-1>', self.startreset)
        self.resetno = Label(self.askresetframe, image=self.rno, bd=0, cursor='hand2')
        self.resetno.pack(side='left', pady=(5, 5))
        self.resetno.bind('<Button-1>', self.returnmain)

        self.rline2 = Frame(self.rwin, bg='#785b28', height=2)
        self.rline2.pack(side='bottom', fill=X)
        self.blackout()

    def showguide(self, event):
        self.gwin = Toplevel(self.master, bg='#000912')
        self.gwin.overrideredirect(1)
        self.gwin.resizable(False, False)
        app.animation('y', 120, 1, 399, self.gwin, 15, 8)
        self.gwin.geometry('+%s+%s' % (self.master.winfo_x() + 10, self.master.winfo_y() + 52))
        self.gwin.attributes('-topmost', db.getcurrent()[1])
        self.gwin.bind('<Button-1>', self.show)

        self.gline = Frame(self.gwin, bg='#785b28', height=1)
        self.gline.pack(side='top', fill=X)
        self.gtop = Frame(self.gwin, bg='#000912')
        self.gtop.pack(side='top', fill=X, padx=(10, 0))
        self.titleguide = Label(self.gtop, text='About:', font='Helvetica 8 bold', fg='light green')
        self.titleguide.pack(side='left', anchor='w', pady=(5, 0))
        self.guideexit = Label(self.gtop, image=self.closebutt, bg='#000912', cursor='hand2', bd=0)
        self.guideexit.pack(side='right')
        self.guideexit.bind('<Button-1>', self.returnmain)

        guidetext = help.guideinfo()
        servertext = help.serverinfo()
        self.guide = Message(self.gwin, text=guidetext + '\n\n' + servertext, bg='#000912', fg='light blue',
                             font='Helvetica 7 bold', aspect=40)
        self.guide.pack(side='top', padx=(5, 5))

        self.ginfo = Label(self.gwin, text='*This program shows\na close but not exact\nPing on League servers.',
                           font='Helvetica 7', bg='#000912', fg='gray')
        self.ginfo.pack(side='top', pady=(5, 0), padx=(5, 5))

        self.gendline2 = Frame(self.gwin, bg='#785b28', height=2)
        self.gendline2.pack(side='bottom', fill=X)
        self.blackout()


class LaunchError:
    def __init__(self, root):
        root.geometry('1x1')
        self.root= root
        root.overrideredirect(1)
        root.geometry('+%s+%s' % (int(root.winfo_screenwidth() / 2 - 100), int(root.winfo_screenheight() / 2 - 90)))
        root.attributes('-topmost', 1)

        self.master = Frame(root, bg='#000912')
        self.master.pack(fill=BOTH, expand=True)

        self.line1 = Frame(self.master, bg='#785b28', height=2)
        self.line1.pack(side='top', fill=X)

        self.top = Frame(self.master, bg='#000912')
        self.top.pack(side='top', fill=X)

        self.pinglabel = PhotoImage(file='media/ping.png')
        self.title = Label(self.top, image=self.pinglabel, bg='#000912')
        self.title.pack(side='left', padx=(5, 0), anchor='w', pady=(5,0))
        self.butt = PhotoImage(file='media/closeno.png')
        self.close = Label(self.top, image=self.butt, bd=0, cursor='hand2', bg='#000912')
        self.close.pack(side='right', pady=(5, 0), padx=(0,5))
        self.close.bind('<Button-1>', self.exitapp)

        self.wlabel = Label(self.master, text='Software is running.', fg='light blue', bg='#000912', font='Helvetica 7 bold', bd=0)
        self.wlabel.pack(side='top', pady=(5, 0))

        self.icon = PhotoImage(file='media/trayexample.png')
        self.example = Label(self.master, image=self.icon, bd=0)
        self.example.pack(side='top', pady=(7, 1))
        self.wlabel = Label(self.master,
                       text='Click on the icon in\nSystem Tray to raise.',
                       fg='light blue', bg='#000912', font='Helvetica 7 bold', bd=0)
        self.wlabel.pack(side='top', pady=(5, 0))

        self.line2 = Frame(self.master, bg='#785b28', height=1)
        self.line2.pack(side='bottom', fill=X)

        root.after(88, self.enterani)

    def exitapp(self, event):
        app.animation('y', 138, 128, 1, self.root, 15, 8, sys.exit)

    def enterani(self):
        app.animation('y', 138, 1, 128, self.root, 15, 18)


##################################################################################################################################################

if __name__ == '__main__':
    try:
        me = singleton.SingleInstance()
        root1 = Tk()
        app = App()
        gui = Gui(root1)
        root1.mainloop()
    except singleton.SingleInstanceException:
        print('El proceso esta siendo utilizado.')
        root2 = Tk()
        app = App()
        gui = LaunchError(root2)
        root2.mainloop()
