from email import message
from os import stat
import socket
from threading import Thread
from tkinter import *

client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
ip_address = '127.0.0.1'
port =8000
client.connect((ip_address,port))
print('Client connected.')

class GUI:
    def __init__(self):
        self.window = Tk()
        self.window.withdraw()
        
        self.login = Toplevel()
        self.login.title('Login')
        self.login.resizable(width=False,height=False)
        self.login.configure(width=775,height=550,bg='#202121')

        self.heading = Label(self.login,text='Login',font='Helvetica 24 bold',justify=CENTER,bg='#202121',fg='#FFF')
        self.heading.place(relx=0.5, rely=0.3,anchor=CENTER )

        self.labelName = Label(self.login,text='Nickname: ',font='Helvetica 12 bold',justify=CENTER,bg='#202121',fg='#727479')
        self.labelName.place(anchor=CENTER,relx=0.4,rely=0.45)

        self.entryName = Entry(self.login,font='Helvetica 14 bold',bg='#252425',fg='#FFF',bd=0,width=27,insertbackground='#00a985')
        self.entryName.place(anchor=CENTER,relx=0.53,rely=0.5,height=35)
        self.entryName.focus()

        self.loginBtn = Button(self.login,text="Login",font='Helvetica 14 bold',bg='#00a985',fg='#000',justify=CENTER,width=24,bd=0,command=lambda: self.goAhead(self.entryName.get()))
        self.loginBtn.place(anchor=CENTER,relx=0.53,rely=0.6)
        self.window.mainloop()

    def goAhead(self,name):
        self.login.destroy()
        # self.name = name
        self.layout(name)
        rcv = Thread(target=self.recieve)
        rcv.start()
    
    
    def layout(self,name):
        self.name = name
        self.window.deiconify()
        self.window.title('Chat room')
        self.window.resizable(width=False,height=False)
        self.window.configure(width=775,height=550,bg='#202121')

        self.labelHead = Label(text=self.name,bg='#202121',fg='#FFF',font='Helvetica 18 bold',pady=5)
        self.labelHead.place(relx=0.5,rely=0.02,anchor=CENTER)

        # self.line = Label(self.window,width=776,bg='#00a985')
        # self.line.place(relwidth=1,relheight=0.01,rely=0.05)

        self.textCons = Text(self.window,width = 20,height = 2,bg = "#252525",fg = "#EAECEE",font = "Helvetica 14",padx = 5,pady = 5,bd=0,highlightthickness=2)
        self.textCons.place(relheight = 0.745,relwidth = 0.95,rely = 0.06,relx=0.025)
        self.textCons.config(cursor='arrow',highlightbackground = "black", highlightcolor= "black")

        self.scrollBar = Scrollbar(self.textCons)
        self.scrollBar.place(relx=0.98,relheight=1)
        self.scrollBar.config(command=self.textCons.yview)


        self.labelBottom = Label(self.window,bg='#202121',height=80)
        self.labelBottom.place(relwidth = 1,rely = 0.82)

        self.entryMsg = Entry(self.labelBottom,font='Helvetica 14',bg='#252525',fg='#FFF',bd=0,insertbackground='#00a985',highlightthickness=2)
        self.entryMsg.config(highlightbackground = "black", highlightcolor= "black")
        self.entryMsg.place(relx=0.045,rely=0.02,relheight=0.04,relwidth=0.8)
        self.entryMsg.focus()

        self.sendBtn = Button(self.labelBottom,text="Send",font='Helvetica 14 bold',width=30,bg='#00a985',fg='#FFF',bd=0,command=lambda: self.sendButton(self.entryMsg.get()))
        self.sendBtn.place(relx=0.855,rely=0.02,relheight=0.04,relwidth=0.1)

    def sendButton(self, msg):
        self.textCons.config(state = DISABLED)
        self.msg=msg
        self.entryMsg.delete(0, END)
        snd= Thread(target = self.write)
        snd.start()

    def show_message(self,message):
        self.textCons.config(state=NORMAL)
        self.textCons.insert(END,message+"\n\n")
        self.textCons.config(state=DISABLED)
        self.textCons.see(END)

    def recieve(self):
        while True:
            try:
                msg = client.recv(2048).decode('utf-8')
                if msg == 'NICKNAME':
                    client.send(self.name.encode('utf-8'))
                else:
                    self.show_message(message)

                    # print('failed')
                    # pass
            except:
                print('Connection error.')
                client.close()
                break


    def write(self):
        self.textCons.config(state=DISABLED)
        while True:
            message = (f"{self.name}: {self.msg}")
            client.send(message.encode('utf-8'))
            self.show_message(message)
            break

g1 = GUI()