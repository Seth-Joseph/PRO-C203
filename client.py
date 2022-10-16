import socket
from threading import Thread
from tkinter import *

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

ip_address = '127.0.0.1'
port = 8000

client.connect((ip_address, port))

print("Connected to the server successfully!")

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

    def goAhead(self, name):
        self.login.destroy()
        self.layout(name)
        rcv = Thread(target=self.receive)
        rcv.start()

    def layout(self, name):
        self.name = name
        self.window.deiconify()
        self.window.title("CHATROOM")
        self.window.resizable(width=False,height=False)
        self.window.configure(width=775,height=550,bg='#202121')

        self.labelHead = Label(self.window,text=self.name,bg='#202121',fg='#FFF',font='Helvetica 18 bold',pady=5)
        self.labelHead.place(relx=0.5,rely=0.02,anchor=CENTER)

        self.textCons = Text(self.window,width = 20,height = 2,bg = "#252525",fg = "#FFF",font = "Helvetica 14",padx = 5,pady = 5,bd=0,highlightthickness=2)
        self.textCons.place(relheight = 0.745,relwidth = 0.95,rely = 0.06,relx=0.025)
        self.textCons.config(cursor='arrow',highlightbackground = "black", highlightcolor= "black")

        self.labelBottom = Label(self.window,bg='#202121',height=80)
        self.labelBottom.place(relwidth = 1,rely = 0.82)

        self.a = Button(self.labelBottom,text="a",font='Helvetica 14 bold',width=30,bg='#00a985',fg='#FFF',bd=0,command=lambda : self.sendButton(msg='a'))
        self.a.place(relx=0.15,rely=0.02,relheight=0.04,relwidth=0.1)

        self.b = Button(self.labelBottom,text="b",font='Helvetica 14 bold',width=30,bg='#00a985',fg='#FFF',bd=0,command=lambda: self.sendButton(msg='b'))
        self.b.place(relx=0.35,rely=0.02,relheight=0.04,relwidth=0.1)

        self.c = Button(self.labelBottom,text="c",font='Helvetica 14 bold',width=30,bg='#00a985',fg='#FFF',bd=0,command=lambda: self.sendButton(msg='c'))
        self.c.place(relx=0.55,rely=0.02,relheight=0.04,relwidth=0.1)

        self.d = Button(self.labelBottom,text="d",font='Helvetica 14 bold',width=30,bg='#00a985',fg='#FFF',bd=0,command=lambda: self.sendButton(msg='d'))
        self.d.place(relx=0.75,rely=0.02,relheight=0.04,relwidth=0.1)

        scrollbar = Scrollbar(self.textCons)
        scrollbar.place(relheight=1,relx=0.974)
        scrollbar.config(command=self.textCons.yview)

        self.textCons.config(state=DISABLED)

    def sendButton(self,msg):
        self.textCons.config(state=DISABLED)

        if msg == 'a':
            self.msg = 'a'
        elif msg == 'b':
            self.msg = 'b'
        elif msg == 'c':
            self.msg = 'c'
        elif msg == 'd':
            self.msg = 'd'
        snd = Thread(target=self.write)
        snd.start()

    def show_message(self, message):
        self.textCons.config(state=NORMAL)
        self.textCons.insert(END, message+"\n\n")
        self.textCons.config(state=DISABLED)
        self.textCons.see(END)

    def receive(self):
        while True:
            try:
                message = client.recv(2048).decode('utf-8')
                if message == 'NICKNAME':
                    client.send(self.name.encode('utf-8'))
                else:
                    self.show_message(message)
            except:
                print("An error occured!")
                client.close()
                break

    def write(self):
        self.textCons.config(state=DISABLED)
        while True:
            message = (f"{self.name}: {self.msg}")
            client.send(message.encode('utf-8'))
            self.show_message(message)
            break

g = GUI()
