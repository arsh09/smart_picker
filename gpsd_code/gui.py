

# import threading
from tkinter import *
import tkinter as tk


class GUI:
    def __init__(self, on_green, on_blue, on_red):
        self.main_w = None
        self.main_root = None
        self.green_callback = on_green
        self.blue_callback = on_blue
        self.red_callback = on_red

    def waitForLogin(self):
        root = Tk()
        root.title("User Login")
        root.focus_force()
        root.geometry("300x250")
        login_w = LoginPage(root)
        root.mainloop()

        return login_w.user

    def setupMainWindow(self):
        self.main_root = Tk()
        self.main_root.title("Call a Robot")
        self.main_root.focus_force()
        self.main_root.geometry("800x430")
        self.main_root.configure(bg='white')
        self.main_w = MainWindow(self.main_root, self.green_callback, self.blue_callback, self.red_callback)

    def loopMainWindow(self):
        self.main_root.mainloop()

    def setGreenButton(self, value):
        if self.main_w is not None:
            if value:
                self.main_w.gbutton.configure(bg = "green")
            else:
                self.main_w.gbutton.configure(bg = "white")

    def setRedButton(self, value):
        if self.main_w is not None:
            if value:
                self.main_w.rbutton.configure(bg = "red")
            else:
                self.main_w.rbutton.configure(bg = "white")

    def setBlueButton(self, value):
        if self.main_w is not None:
            if value:
                self.main_w.bbutton.configure(bg = "blue")
            else:
                self.main_w.bbutton.configure(bg = "white")

    def setDescription(self, string):
        self.main_w.label_text.set(string)

    def getDescription(self):
        self.main_w.label_text.get()
        
    def setUser(self, string):
        self.main_w.user_text.set(string)


class MainWindow():
    def __init__(self, root, green_callback, blue_callback, red_callback):
        self.root = root

        # initialize tkinter
        self.label_text = StringVar()

        self.user_text = StringVar()

        # set window title
        self.root.wm_title("Call A Robot")

        self.text = Label(self.root, text="Welcome to Call A Robot.",background="white", foreground="#2B394A", font = ('gomono', 24, "bold"), textvariable = self.label_text)
        self.text.place(relx = 0.5, rely = 0.1, anchor = CENTER)

        self.userText = Label(self.root, text="", foreground="#9B9A94",background="white", font = "arial 12 normal", textvariable = self.user_text)
        self.userText.place(relx = 0.5, rely = 0.2, anchor = CENTER)

        self.gbutton = Button(self.root, text="Call", bg="white", height=10, width=20, command=lambda : green_callback(None))
        self.gbutton.place(relx = 0.1, rely = 0.5, anchor = 'w') 
        self.gbutton.config(highlightbackground="green")

        self.rbutton = Button(self.root, text="Cancel", bg="white", height=10, width=20, command=lambda : red_callback(None))
        self.rbutton.place(relx = 0.5, rely = 0.5, anchor = CENTER) 
        self.rbutton.config(highlightbackground="red")

        self.bbutton = Button(self.root, text="Load", bg="white", height=10, width=20, command=lambda : blue_callback(None))
        self.bbutton.place(relx = 0.9, rely = 0.5, anchor = 'e') 
        self.bbutton.config(highlightbackground="blue")


class LoginPage():
    def __init__(self, master=None):
        self.master = master

        #self.login_screen.attributes("-fullscreen", True)  
        self.loginText = Label(self.master, text="Please enter login details", font = "arial 12 bold", foreground="red")
        self.loginText.place(relx = 0.5, rely = 0.1, anchor = CENTER)
        self.usernameText = Label(self.master, text="Username:")
        self.usernameText.place(relx = 0.2, rely = 0.3, anchor = CENTER)
        self.username_login_entry = Entry(self.master)
        self.username_login_entry.place(relx = 0.5, rely = 0.4, anchor = CENTER, width = 270)
        self.subButton = Button(self.master, text="Login", width=30, height=1, command =self.submit, bg = "green")
        self.subButton.place(relx = 0.5, rely = 0.6, anchor = CENTER)
        self.user = "not set"
    
    def submit(self):
        self.user = self.username_login_entry.get()
        print("The user is : " + self.user)
        self.master.destroy()



if __name__ == "__main__":
    # tests

    gui = GUI()

    user = gui.waitForLogin()

    print("user logged {}".format(user))

    gui.setupMainWindow()

    gui.greenButtonPressed()

    gui.loopMainWindow()

    # gui.redBut    tonPressed()
