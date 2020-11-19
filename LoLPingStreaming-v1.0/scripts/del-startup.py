import os
import sys
from getpass import getuser
from tkinter import *
from dbfunc import Db as db
from time import sleep


class App:
    def __init__(self):
        self.USER_NAME = getuser()
        self.startup_path = r'C:\Users\%s\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup' % self.USER_NAME

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


    def main(self):
        self.isset = db.getcurrent()[2]
        def one():
            gui.label.config(text='Startup is set, Searching for startup file in System folder...')
        def two():
            try:
                os.chdir(self.startup_path)
                os.remove('LoLPingStreaming.vbs')
                gui.wlabel.config(text="Found file 'LoLPingStreaming.vbs', deleting...")
                root.after(688*3, three)
                root.after(688*6, exit)
            except Exception:
                gui.label.config(text="An error occured during cleanup of startup file 'LoLPingStreaming.vbs':")
                gui.wlabel.config(text="Please manually delete it at your startup folder (Press Windowskey + R, and type 'shell:startup').")
                gui.close.pack(side='right', pady=(5, 0), padx=(0,5))
        def three():
            gui.wlabel.config(text='File deleted, Uninstall will begins now...')
        def three2():
            gui.wlabel.config(text='Startup is not set, Uninstall will begins now...')
        def exit():
            gui.exitapp()

        if self.isset:
            root.after(688, one)
            root.after(688*3, two)
        else:
            root.after(688, three2)
            root.after(688*3, exit)


class Del:
    def __init__(self, root):
        root.geometry('1x1')
        self.root= root
        root.overrideredirect(1)
        root.geometry('+%s+%s' % (int(root.winfo_screenwidth() / 2 - 268), int(root.winfo_screenheight() / 2 - 90)))
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
        # self.close.pack(side='right', pady=(5, 0), padx=(0,5))
        self.close.bind('<Button-1>', self.exitapp)

        self.label = Label(self.master, text='Checking if startup is set...', fg='light blue', bg='#000912', font='Helvetica 7 bold', bd=0)
        self.label.pack(side='top', pady=(5, 0), anchor='w', padx=(15,0))

        self.wlabel = Label(self.master, text='', fg='light blue', bg='#000912', font='Helvetica 7 bold', bd=0)
        self.wlabel.pack(side='top', anchor='w', padx=(15,0))

        self.line2 = Frame(self.master, bg='#785b28', height=1)
        self.line2.pack(side='bottom', fill=X)

        root.after(88, self.enterani)
        root.after(1268, app.main)

    def exitapp(self, *args):
        app.animation('x', 68, 528, 1, self.root, 28, 8, sys.exit)

    def enterani(self):
        app.animation('x', 68, 1, 528, self.root, 28, 8)


root = Tk()
app = App()
gui = Del(root)
root.mainloop()
