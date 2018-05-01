from __future__ import print_function

# Imports to access nugget methods
import argparse
import hashlib
import sys
from getpass import getpass
from Cryptodome.Cipher import AES
from crankycoin import *

# Import for the GUI
import Tkinter as tk
import random
import requests
import socket 
# from config import *
# from node import NodeMixin
# from transaction import *


LARGE_FONT = ("Verdona", 12)
SMALL_FONT = ("Verdona", 8)
# ip = config['user']['ip']
# ip = socket.gethostbyname(socket.gethostname())
ip = '10.0.2.15'
# print(ip)
public_key = config['user']['public_key']
fullnode = FullNode(ip, public_key)



class BlockGold(tk.Tk):
    # Code in this class baseline code to start basic gui
    def __init__(self, *args, **kwargs):
        
        tk.Tk.__init__(self, *args, **kwargs)
  
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)

        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        for F in (StartPage, LoginPage, NewUserPage, WalletPage, SendPage):

            frame = F(container, self)

            self.frames[F] = frame

            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(StartPage)

    def show_frame(self, cont):

        frame = self.frames[cont]
        frame.tkraise()
        frame.configure(background="#000000", borderwidth="2", width="506")

class StartPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="N U G G E T S", background="#000000", font='Helvetica 24 bold', foreground="#ffff00")
        label.pack(pady=10, padx=10)

        label = tk.Label(self, text="Passphrase", background="#000000", font='Helvetica 12 bold', foreground="#ffff00")
        label.pack()

        passphrase = tk.Entry(self)
    #EE  passphrase.place(relx=0.38, rely=0.39, height=30, relwidth=0.46)
        passphrase.pack()

        loginbutton = tk.Button(self, text="Login", font=LARGE_FONT, command=lambda: login(self, passphrase, controller))
        loginbutton.configure(background="#ffff00", borderwidth="5", highlightcolor="white", pady="0")
        loginbutton.pack(padx=5, pady=10)

        newuserbutton = tk.Button(self, text="New User", font=SMALL_FONT, command=lambda:
        controller.show_frame(NewUserPage))
        newuserbutton.configure(background="#ffff00", borderwidth="5", highlightcolor="black", pady="0")
        newuserbutton.pack(padx=5, pady=10)


def login(self, passphrase, controller):
    encrypted = config['user']['encrypted_private_key']
    encrypted = encrypted.decode('hex')
    nonce = encrypted[0:16]
    tag = encrypted[16:32]
    ciphertext = encrypted[32:]
    hashedpass = hashlib.sha256(passphrase.get()).digest()
    cipher = AES.new(hashedpass, AES.MODE_EAX, nonce)
    global client
    try:
        private_key = cipher.decrypt_and_verify(ciphertext, tag)
        client = Client(private_key)
        passphrase.delete(0, "end")
        controller.show_frame(WalletPage)
    except ValueError as ve:
        errmessage = tk.Label(self, text="*** PASSPHRASES DO NOT MATCH ***")
        errmessage.grid(row="2", columnspan="2")


class LoginPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label1 = tk.Label(self, text="Passphrase", font=LARGE_FONT)
        label1.grid(row=0, column=0)
        passphrase = tk.Entry(self, bd=5)
        passphrase.grid(row=0, column=1)

        loginbutton1 = tk.Button(self, text="Login", font=LARGE_FONT, command=lambda: login(self, passphrase, controller))
        loginbutton1.grid(row=1, columnspan=2)

        backbutton = tk.Button(self, text="Back", font=SMALL_FONT, command=lambda: controller.show_frame(StartPage))
        backbutton.grid(row=3, columnspan=2)


def update():
    userdata = "config/config.yaml"
    with open(userdata, "w") as f:
        yaml.dump(config, f)


def encrypt(passphrase, confirm, self, controller):
    if passphrase.get() != confirm.get() or passphrase.get() == None:
        errmessage1 = tk.Label(self, text="*** PASSPHRASEES DO NOT MATCH ***")
        errmessage1.grid(row="3", columnspan="2")
    else:
        #secret = coincurve.utils.get_valid_secret()
        secret = "32"

        hashedpass = hashlib.sha256(passphrase.get()).digest()
        cipher = AES.new(hashedpass, AES.MODE_EAX)
        ciphertext, tag = cipher.encrypt_and_digest(secret)

        combined = "{}{}{}".format(cipher.nonce, tag, ciphertext)

        global client
        client = Client()

        passphrase.delete(0, "end");
        confirm.delete(0, "end");

        config['user']['encrypted_private_key'] = combined.encode('hex')
        config['user']['public_key'] = client.get_public_key()
        update()

        controller.show_frame(WalletPage)


class NewUserPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        label2 = tk.Label(self, text="Passphrase", background="#000000", font='Helvetica 12 bold', foreground="#ffff00")
        label2.grid(row=0, column=0)
        label3 = tk.Label(self, text="Re-Enter Passphrase", background="#000000", font='Helvetica 12 bold', foreground="#ffff00")
        label3.grid(row=1, column=0)

        newpassphrase = tk.Entry(self, bd=5)
        newpassphrase.grid(row=0, column=1)
        confirm = tk.Entry(self, bd=5)
        confirm.grid(row=1, column=1)
        enterbutton = tk.Button(self, text="Enter", font=LARGE_FONT,
                                command=lambda: encrypt(newpassphrase, confirm, self, controller))
        enterbutton.configure(background="#ffff00", borderwidth="5", highlightcolor="white", pady="0")
        enterbutton.grid(row=2, columnspan=2)
        backbutton1 = tk.Button(self, text="Back", font=SMALL_FONT, command=lambda: controller.show_frame(StartPage))
        backbutton1.configure(background="#ffff00", borderwidth="5", highlightcolor="white", pady="0")
        backbutton1.grid(row=4, columnspan=2)


def callback(self, balance):
    # host = '10.0.2.15'
    # port = 5000 

    # s=socket.socket()
    # s.connect((host, port))

    # trans = s.recv(1024)
    
    # config[user][block_path].append(trans)
    # update()

    # print('Received updated Transaction')
    # s.close()
    amount = client.get_balance()
    if amount is None:
        amount = 0
    balance = tk.Label(self, text=str(amount)+" Nugget(s)", font=LARGE_FONT)
    balance.grid(row=0, rowspan = 2, column=0)




def callback1(self, priK):
    priK = tk.Label(self, text=config['user']['encrypted_private_key'], font=LARGE_FONT)
    priK.grid(row=0, column=1, columnspan=3)

def viewPeers(self, pri):
    pri = tk.Label(self, text=fullnode.full_nodes, font=LARGE_FONT)
    pri.grid(row=8, column=0, columnspan=3)
    config['network']['seed_nodes'] = fullnode.full_nodes
    update();

def addMe(self):
    ip = '10.0.2.15'
    host = '137.198.12.80'
    port = 5000

    s = socket.socket()
    s.connect((host, port))
    # fullnode.add_node('10.0.2.16')
    data = s.recv(1024)
    fullnode.add_node(data)
    # config['network']['seed_nodes'].append(host)
    # update();
    # c = s.accept()
    s.send(ip)
    # print(fullnode.add_node(host))
    # print(fullnode.full_nodes)
    # message = raw_input("-> ")
    # if message == 'a ':
            # fullnode.add_node('10.0.2.16')
            # print("node sucesfuly added" + str(fullnode.full_nodes))
    #         s.close()
    # while message != 'q ':
    #         s.send(message)
    #         data = s.recv(1024)
    #         print ('Received from server' + str(data))
    #         message = raw_input("->")
    print("node sucesfuly added")
    s.close()


def callback2(self, pubK):
    pubK = tk.Label(self, text=config['user']['public_key'], font=LARGE_FONT)
    pubK.grid(row=1, column=1, columnspan=3)

def sendPageBack(self):
    # controller.show_frame(WalletPage)
    self.destroy()

def refresh():
    window.destroy()
    execfile("blockGold.py",globals())

class WalletPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        # construction = tk.Label(self, text="/// UNDER CONSTRUCTION ///")
        # construction.grid(row=0, columnspan=3)
        #cmd = raw_input("{} ({}) wallet > ".format(config['network']['name'], config['network']['ticker_symbol']))
        #cmd_split = cmd.split()
        #
        balance = tk.Button(self, text="Balance", command=lambda: callback(self, balance))
        balance.configure(background="#ffff00", borderwidth="5", highlightcolor="white", pady="0")
        balance.grid(row = 0, rowspan=2, column=0)

        networkConnect =tk.Button(self, text = "Connect To BlockGold Network: ", command=lambda: addMe(self))
        networkConnect.configure(background="#ffff00", borderwidth="5", highlightcolor="white", pady="0")
        networkConnect.grid(row=2, column=0)
        sendcurrency = tk.Button(self, text="Send Nuggets: ", font=SMALL_FONT, command =lambda: controller.show_frame(SendPage))
        sendcurrency.configure(background="#ffff00", borderwidth="5", highlightcolor="white", pady="0")
        sendcurrency.grid(row=2, column=1)
        viewprivatekey = tk.Button(self, text="View my Private Key ", command=lambda: callback1(self, viewprivatekey))
        viewprivatekey.configure(background="#ffff00", borderwidth="5", highlightcolor="white", pady="0")
        viewprivatekey.grid(row=0, column=1)
        viewpublickey = tk.Button(self, text="View my Public Key ", command=lambda: callback2(self, viewpublickey))
        viewpublickey.configure(background="#ffff00", borderwidth="5", highlightcolor="white", pady="0")
        viewpublickey.grid(row=1, column=1)
        logout = tk.Button(self, text="logout", font=LARGE_FONT, command=lambda: controller.show_frame(StartPage))
        logout.configure(background="#ffff00", borderwidth="5", highlightcolor="white", pady="0")
        logout.grid(row=4, columnspan=3)

        fresh = tk.Button(self, text="Refresh", font=LARGE_FONT, command=lambda: refresh())
        fresh.configure(background="#ffff00", borderwidth="5", highlightcolor="white", pady="0")
        fresh.grid(row=5, columnspan=3)


def sendNuggets(self, to, amount):
    client.create_transaction(to, amount)
    ip = '10.0.2.15'
    host = '137.198.12.80'
    port = 5000

    s = socket.socket()
    s.connect((host, port))
    # fullnode.add_node('10.0.2.16')
    #data = s.recv(1024)
    # fullnode.add_node(data)
    # config['network']['seed_nodes'].append(host)
    # update();
    # c = s.accept()
    s.send(client.create_transaction(to, amount))
    # print(fullnode.add_node(host))
    # print(fullnode.full_nodes)
    # message = raw_input("-> ")
    # if message == 'a ':
            # fullnode.add_node('10.0.2.16')
            # print("node sucesfuly added" + str(fullnode.full_nodes))
    #         s.close()
    # while message != 'q ':
    #         s.send(message)
    #         data = s.recv(1024)
    #         print ('Received from server' + str(data))
    #         message = raw_input("->")
    print("Transaction Updated")
    s.close()

def get_transaction_history(self):
    text = tk.StringVar()
    text_widget = tk.Label(self, textvariable = text)
    text_widget.grid(row = 0, column = 2, rowspan = 4)
    empty = True

    transactions = config['network']['block_path']
    for i in range(0, len(transactions)):
        pointer = '{}'.format(transactions[i])
        for j in range(0,len(bcinfo[pointer]['transactions'])):
            if bcinfo[pointer]['transactions']['{}'.format(j)]['destination'] == config['user']['public_key']:
                s = text.get()
                s = (str)("Recieved " + (str)(bcinfo[pointer]['transactions']['{}'.format(j)]['amount']) + " nugget(s) from " + bcinfo[pointer]['transactions']['{}'.format(j)]['source'] + "\n")
                text.set(s)
                empty = False
            elif bcinfo[pointer]['transactions']['{}'.format(j)]['source'] == config['user']['public_key']:
                s = text.get()
                s = (str)("Sent " + (str)(bcinfo[pointer]['transactions']['{}'.format(j)]['amount']) + " nugget(s) from " + bcinfo[pointer]['transactions']['{}'.format(j)]['destination'] + "\n")
                text.set(s)
                empty = False

        if empty is True:
            s = text.get()
            s = ("No Transaction History")
            text.set(s)

class SendPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent,)

        SendTo = tk.Label(self, background="#000000", font='Helvetica 12 bold', foreground="#ffff00", text="Send Nuggets To This Public Key: ")
        SendTo.grid(row=0, column=0)

        SendTo1 = tk.Entry(self, bd=5)
        SendTo1.grid(row=0, column=1)

        AmmountTo = tk.Label(self, background="#000000", font='Helvetica 12 bold', foreground="#ffff00",text="Enter Nuggets Amount to send: ")
        AmmountTo.grid(row=2, column=0)

        AmmountTo1 = tk.Entry(self, bd=5)
        AmmountTo1.grid(row=2, column=1)

        backbutton1 = tk.Button(self, text="Back", font=SMALL_FONT, command=lambda: controller.show_frame(WalletPage) )
        backbutton1.configure(background="#ffff00", borderwidth="5", highlightcolor="white", pady="0")
        backbutton1.grid(row=5, columnspan=2)

        SendButton = tk.Button(self, text="Send", font =SMALL_FONT, command=lambda: sendNuggets(self, SendTo1.get(), (int)(AmmountTo1.get())))
        SendButton.configure(background="#ffff00", borderwidth="5", highlightcolor="white", pady="0")
        SendButton.grid(row=4, columnspan=2)

        TransactionHistory = tk.Button(self, text = "Transaction History", font =SMALL_FONT, command =lambda: get_transaction_history(self))
        TransactionHistory.configure(background="#ffff00", borderwidth="5", highlightcolor="white", pady="0")
        TransactionHistory.grid(row = 5, column = 2)
        viewP = tk.Button(self, text="View Peers on the network ", command=lambda: viewPeers(self, viewP))
        viewP.configure(background="#ffff00", borderwidth="5", highlightcolor="white", pady="0")
        viewP.grid(row=6, column=0, columnspan=3)





app = BlockGold()
app.title("BlockGold")
app.mainloop()
