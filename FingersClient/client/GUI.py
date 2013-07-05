'''
Created on Jul 5, 2013

@author: SanjaK
'''


from Tkinter import Tk, Frame, Label, BOTH, Button, StringVar, Entry, Text, LEFT, RIGHT, BOTTOM, E, N,CENTER,NW,W, S, END
import tkMessageBox
import tkFont

class Template(Frame):
    '''
    Template for all gui classes
    '''
    def __init__(self, parent):
        Frame.__init__(self, parent)   
         
        self.parent = parent        
        self.parent.title("Fingers game")  
        self.pack(fill=BOTH, expand=1)

class ChatWellcameForm(Template):
    '''
    Class for graphic presentation of chat client.
    Wellcome form with two buttons.
    '''
  
    def __init__(self, parent):
        Template.__init__(self, parent) 
        self.parent = parent        
        self.initUI()
        
    def initUI(self):
        '''
        Initialize all gui components
        '''
        
        self.welcometext = Label(self, text="Hello, world!")
        self.welcometext.pack(pady=20)
        self.localButton = Button(self,text="Game against computer", width=30)
        self.localButton.pack(pady=5)
        self.netButton = Button(self, text="Network game", width=30, command=self.openNetworkForm)
        self.netButton.pack(pady=5)
       
    
    def openNetworkForm(self):
        '''
        Opens form for network game
        '''
        self.parent.destroy()
        root = Tk()
        ex = ChatNetworkForm(root)
        root.geometry("300x250+300+300")
        root.mainloop() 
        
class ChatNetworkForm(Template):
    '''
    Class for graphic presentation of chat client. 
    ChatNetworkForm form with two text boxes and one button.
    '''
  
    def __init__(self, parent):
        Template.__init__(self, parent)  
       
        self.parent = parent        
        self.initUI()
        
    def initUI(self):
        '''
        Initialize all gui components
        '''
       
        self.nameText = Label(self, text="Enter name")
        self.nameText.pack(pady=5)
        self.name = StringVar()
        self.nameText =Entry(self, textvariable=self.name)
        self.nameText.pack(pady=5)
        self.nameButton = Button(self, text="Continue", width=30, command=self.open_game_form)
        self.nameButton.pack(pady=5)
        
        
    def open_game_form(self):
        '''
        Opens form for game 
        Check if name is entered
        '''
        
        if not self.name.get() == '':    
            self.parent.destroy()
            root = Tk()
            ChatMainForm(root,self.name.get())
            root.geometry("500x400+300+300")
            root.mainloop() 
        else:
            tkMessageBox.showwarning("Fingers","Please enter name")
        
class ChatMainForm(Template):
    '''
    Class for graphic presentation of chat client.
    ChatMainForm form with textbox and entry.
    '''
  
    def __init__(self, parent,name):
        Template.__init__(self, parent)    
        self.name = name
        self.parent = parent        
        self.initUI()
        
    def initUI(self):
        '''
        Initialize all gui components
        '''
        
        self.nameText = Label(self, text="Chat")
        self.nameText.place(x=270, y=10)

        self.messageDispley = Text(self,font=tkFont.Font(family="Calibri",size=10),width=30,height=15)
        self.messageDispley.place(x=270, y=40)
        self.messageDispley.insert(END,self.name)
        
        self.message = StringVar()
        self.messageText =Entry(self, textvariable=self.message, width=35)
        self.messageText.place(x=270, y=275)
        
        self.nameButton = Button(self, text="Continue", width=30)
        self.nameButton.place(x=270, y=300)
