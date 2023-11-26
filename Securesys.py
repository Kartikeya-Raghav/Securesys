a=3
'''Securesys v1.0
A python script for basic security implementations
on files and browser.For personal use only.Usage of
this script for commercial use is prohibitted.
For more info check my github repostery

Created by Kartikeya
'''
import os #to pipe os
from plyer import notification #for sending notification
import urllib #for accessing browser
import tkinter #gui
from selenium import webdriver #web drivers
from cryptography.fernet import Fernet #Fernet binary key for encryption
import threading #for creating threads
import subprocess #for accessing shell
from threading import Thread #for creating Thread
from multiprocessing import Process,active_children #for creating Process
class MainActivity: #Display Class
    global password
    global warning
    def __init__(self):
        global password
        global warning
        password=''
        self.key='86rDoqIPIkMgKmMcnj2rIzyikwH5wdXfrncQs5FUBmc=' #encryption key
        self.mainlayout=tkinter.Tk() #main window
        self.mainlayout.config(background='black')
        self.mainlabel=tkinter.Label(self.mainlayout,\
                                     text='Securesys v1.0',\
                                     background='black',\
                                     foreground='red',\
                                     width=50,height=5)
        self.username=os.getlogin()
        if os.path.isfile(os.getcwd()+'\\password.txt'): #finding password file
            try:
                self.FileSecurity=FileSecurity()
                self.Decryptor=FileSecurity.Decrypt
                password=self.Decryptor(self,file='password.txt',\
                                        key=self.key)
                self.FileSecurity.Encrypt(file='password.txt',\
                                          key=self.key)
                LockEdit(text='password.txt')
            except Exception as t:
                print(t)
                ok='ok'
        else:
            #Creating new password
            password=self.InputText('Enter your new password',\
                                    self.passwordWrite)
        #UI widgets   
        self.mainlabel.pack()
        self.FileSecurityButton=tkinter.Button(self.mainlayout,\
                                               text='File Security',\
                                               command=lambda:\
                                               self.InputText('Enter files to lock',\
                                                              LockEdit),\
                                               background='green',\
                                               foreground='red',\
                                               width=50,height=5).pack()
        self.FileUnlockButton=tkinter.Button(self.mainlayout,\
                                             text='File Unlock',\
                                             command=lambda:\
                                             self.InputText(text='Enter password',\
                                                            command=\
                                                            FileSecurity.UnlockEdit),\
                                             background='green',\
                                             foreground='red',\
                                             width=50,height=5).pack()
        self.BrowserSecurityButton=tkinter.Button(self.mainlayout,\
                                                  text='Open Secured browser',\
                                                  command=lambda:\
                                                  BrowserSecurity(),\
                                                  background='green',\
                                                  foreground='red',\
                                                  width=50,height=5).pack()
        self.TerminalButton=tkinter.Button(self.mainlayout,\
                                           text='Open Terminal',\
                                           command=lambda:\
                                           TerminalRun(),\
                                           background='green',\
                                           foreground='red',\
                                           width=50,height=5).pack()

    def WarningText(self,text): #Display Warning
        global warning
        self.warnWindow=tkinter.Tk()
        self.warnWindow.config(background='black')
        self.warnShowText=tkinter.Label(self.warnWindow,\
                                        text=text,\
                                        background='black',\
                                        foreground='red',\
                                        width=50,height=5)
        self.warnShowText.after(5000,self.warnWindow.destroy)
        self.warnShowText.pack()
    def InputText(self,text='Enter',command=''): #Input Text
        self.textWindow=tkinter.Tk()
        self.textWindow.config(background='black')
        self.textInput=tkinter.StringVar(self.textWindow)
        self.DisplayText=tkinter.Label(self.textWindow,\
                                       text=text,\
                                       background='black',\
                                       foreground='red',\
                                       width=50,height=5)
        self.Input=tkinter.Entry(self.textWindow,\
                                 textvariable=self.textInput,\
                                 background='white',\
                                 foreground='red',\
                                 font=('Arial',25))
        self.SendButton=tkinter.Button(self.textWindow,\
                                       text='Send',\
                                       command=lambda:\
                                       [self.textWindow.destroy(),\
                                        command(self.textInput.get())],\
                                       background='green',\
                                       foreground='red',\
                                       width=50,height=5)
        self.DisplayText.pack()
        self.Input.pack()
        self.SendButton.pack()
    def passwordWrite(self,text): #For writing password
        key='86rDoqIPIkMgKmMcnj2rIzyikwH5wdXfrncQs5FUBmc=' #Encryption key
        passwordFile=open('password.txt','w')
        print(text)
        passwordFile.write(text)
        passwordFile.close()
        FileSecurity().Encrypt(file='password.txt',key=key)
class TerminalRun: #Terminal class
    def __init__(self):
        #Displaying Username
        MainActivity.WarningText(self,\
                                 text='Terminal:'+os.getlogin())
        self.CommandRun()
    def CommandRun(self): #Terminal Window
        self.TerminalWindow=tkinter.Tk() #Terminal command window
        self.TerminalWindow.config(background='black')
        self.text=tkinter.StringVar(self.TerminalWindow)
        self.TextShowLabel=tkinter.Label(self.TerminalWindow,\
                                         text='Enter command to run',\
                                         background='black',\
                                         foreground='red',\
                                         width=50,height=5).pack()
        self.TerminalText=tkinter.Entry(self.TerminalWindow,\
                                        textvariable=self.text,\
                                        foreground='red',\
                                        font=('Arial',25)).pack()
        self.TerminalButton=tkinter.Button(self.TerminalWindow,\
                                           text='Run',\
                                           command=lambda:\
                                           self.CommandCheck(self.text.get()),\
                                           background='green',\
                                           foreground='red',\
                                           width=50,height=5).pack()
    def CommandCheck(self,text):#To pipe commands to terminal
        try:
            self.commandrun=subprocess.check_output(text,shell=False)
        except Exception as t:
            self.commandrun=t
        self.CommandWindow=tkinter.Tk()
        self.CommandWindow.config(background='black')
        self.commandtext=tkinter.Label(self.CommandWindow,\
                                       text=self.commandrun,\
                                       background='black',\
                                       foreground='red',\
                                       width=50,height=5).pack()
class BrowserSecurity: #Browser class
    global warning
    def __init__(self):
        #Accessing drivers
        self.driver = webdriver.Edge('edgedriver.exe')
        #Creating thread for Monitoring url
        t=Thread(target=self.MonitorUrl)
        t.start()
        t.join()
    def MonitorUrl(self): #To Monitor Url
        self.last=''   
        while True:
            self.url=self.driver.current_url #Capturing url
            self.url=str(self.url)
            if self.url==self.last:
                ok='ok'
            else:
                try:
                    self.last=self.url
                    text=urllib.request.urlopen(self.url) #Scrapping url
                    text=str(text.read())
                    self.wrongwordsfile=open('wrongwordsall.txt','r')
                    self.wrongwordsall=self.wrongwordsfile.read()
                    self.wrongwordsfile.close()
                    self.wrongwordsall=self.wrongwordsall.split('\n')
                    print(text)
                    for j in self.wrongwordsall: #Checking for wrong words
                        if j in text.split():
                            print(4)
                            #Sending notification
                            notification.notify(title='Wrong Word',\
                                                message=j,timeout=5)
                except Exception as t:
                    print(t)
class FileSecurity: #File Security class
    global password
    def __init__(self):
        self.key='86rDoqIPIkMgKmMcnj2rIzyikwH5wdXfrncQs5FUBmc=' #Encryption key
    def UnlockEdit(text): #For unlocking edit lock
        global password
        password=str(password)
        password=password.replace('b\'','')
        password=password.replace('\'','')
        if password==text:
            for j in active_children():
                j.terminate()
        else:
            MainActivity().WarningText(text=f'Incorrect Password {password}')
    def Encrypt(self,file,key): #For encrypting file
        try:
            print(file)
            print(key)
            self.fernet=Fernet(key) #Creating fernet object
            print('Key is correct')
            with open(file, 'rb') as self.file:
                self.original = self.file.read()
                self.encrypted = self.fernet.encrypt(self.original)
            with open(file, 'wb') as self.encrypted_file:
                self.encrypted_file.write(self.encrypted)
                print('Encrypted')
        except Exception as t:
            print(t)
    def Decrypt(self,file,key): #For decrypting file
        while True:
            try:
                fernet=Fernet(key)
                print('Key is correct')
                with open(file, 'rb') as enc_file:
                    encrypted = enc_file.read()
                    print('File opened')
                    decrypted = fernet.decrypt(encrypted)
                with open(file, 'wb') as dec_file:
                    dec_file.write(decrypted)
                    print('Decrypted')
            except Exception as t:
                print(t)
                return encrypted
def LockEdit(text): #To enable Edit lock
    #Outside of FileSecurity class as it was creating issues
    #with multiprocessing
        text=str(text)
        text=text.split(',')
        print(text)
        for j in text:
            print(j)
            LockEditProcess=Process(target=LockEditRuntime,args=[j])
            print(1)
            LockEditProcess.start()
            print(2)
def LockEditRuntime(text): #Lock Edit Process Runtime
        with open(text,'a') as file:
            print(3)
            while True:
                file.flush()
            print(4)
if __name__=='__main__':
    b=MainActivity()
    tkinter.mainloop()