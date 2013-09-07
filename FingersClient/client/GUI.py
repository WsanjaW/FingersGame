'''
Created on Jul 5, 2013

@author: SanjaK
'''


from Tkinter import Tk, Frame, Label, BOTH, Button,Listbox, StringVar, Entry, Text, LEFT, RIGHT, BOTTOM, E, N,CENTER,NW,W, S, END
import tkMessageBox
import tkFont
#PROVERI zasto nece from!!!!!
import ChatClient
import thread
import time
from lxml import etree
import traceback
import threading
import pygame

 
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
    Welcome form with two buttons.
    Choosing between game against computer and network game
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
        Opens form for network game end connects to server
        '''

        self.parent.destroy() 
        root = Tk()
        ex = ChatNetworkForm(root)
        root.geometry("300x250+300+300")
        root.mainloop() 
       
        
class ChatNetworkForm(Template):
    '''
    Class for graphic presentation of chat client. 
    ChatNetworkForm form with one text boxes and one button.
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
        For entering name that will be use during game.
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
    Main form with chat, list of created games, button for creating game.
    If you created game button becomes start game.
    ChatMainForm form with textbox, entry, listbox and button.
    '''
  
    def __init__(self, parent,name):
        '''
        Initialize all gui components...
        
        parent represents root of tk window
        name is  name that client entered
        
        Creates instance of client class and starts thread for receiving messages
        '''
        Template.__init__(self, parent)  
        
        self.client = ChatClient.ChatClient()
        #where to put try block here or in connect method
        self.client.connect_to_server()
          
        self.end = False #for stopping receiving thread 
        self.name = name
      
        #start new thread
        self.thread=thread.start_new_thread( self.receive_server_messages, (1,) )#!!!doesn't work without second argument
        
        #send first message with name
        self.client.send_message(self.name)
        
        self.parent = parent       
        self.initUI()
        
    def initUI(self):
        '''
        Initialize all gui components
        '''
        
        self.nameText = Label(self, text="Chat")
        self.nameText.place(x=270, y=10)
        self.nameText3 = Label(self, text="Players in game")
        self.nameText3.place(x=50,y=10)
        self.nameText2 = Label(self, text="Game list            ")# **********Popravi ovo!!!!!!********
        self.nameText2.place(x=50,y=10)
       
        
        #display chat messages
        self.messageDispley = Text(self,font=tkFont.Font(family="Calibri",size=10),width=28,height=13)
        self.messageDispley.place(x=270, y=40)
        self.messageDispley.insert(END,"Welcome...\n")
        
        #write text messages
        self.message = StringVar()
        self.messageText =Entry(self, textvariable=self.message, width=28)
        self.messageText.place(x=270, y=275)
        
        #send chat massage
        self.nameButton = Button(self, text="Send", width=26, command=self.send_chat_message)
        self.nameButton.place(x=270, y=300)
        
        #lists players in specific game
        self.playersList = Listbox(self)
        self.playersList.place(x=50, y=30)
        
        #lists all games
        self.gameList = Listbox(self)
        self.gameList.place(x=50, y=30)

        #join created game
        self.joinGameButton = Button(self,text="Join game",width=15, command=self.send_join_message)
        self.joinGameButton.place(x=50, y=230)
        
        #start created game
        self.startGameButton = Button(self,text="Start game",width=15, command=self.send_game_start_message)
        self.startGameButton.place(x=50, y=270)
        
        #create new game
        self.createGameButton = Button(self,text="Create new game",width=15, command=self.create_new_game)
        self.createGameButton.place(x=50, y=270)
        
     
    def send_game_start_message(self):
        '''
        Sends signal to server that game is starting
        '''
        
        self.client.send_message("Start game")
        
    def send_join_message(self):
        '''
        Hides 'create new game' and 'Join game'  buttons and 
        shows 'Players list' listbox.
        Send message with selected game to server
        '''
        #first we think you can join
        self.canJoin = True
        
        items = self.gameList.curselection()  
        
        # creating xml document to be send
        root2 = etree.Element("JoinGame")
        ge = etree.SubElement(root2, "game").text =  self.gameList.get(items[0])  
        
        self.client.send_message(etree.tostring(root2))
        
        #first receive_server_messages thread needs to finish processing message from server        
        self.event.wait()
        
        #if we don't receive message from server we hide fields 
        if self.canJoin:
            self.joinGameButton.place_forget()
            self.createGameButton.place_forget()
            self.gameList.place_forget()
            self.nameText2.place_forget()
            self.startGameButton.place_forget()
        
        
        
           
        
    
    def create_new_game(self):
        '''
        Hides 'create new game' and 'Join game'  buttons and 
        shows 'Start game' button and 'Players list' listbox.
        '''
        self.joinGameButton.place_forget()
        self.createGameButton.place_forget()
        self.gameList.place_forget()
        self.nameText2.place_forget()
        
        self.client.send_message("Create game")
        
         
    def send_chat_message(self):
        '''
        sends chat message to server
        if message is 'Bye' ends program**to be changed**
         
        '''
        
        # creating xml document to be send
        root2 = etree.Element("ChatMessage")
        etree.SubElement(root2, "message").text = self.message.get()
        
        self.client.send_message(etree.tostring(root2))
        
        if self.message.get() =='Bye':
            print 'sss'
            self.client.comSocket.close
            self.end = True
            self.parent.destroy()   
                     
        self.message.set('')   
        
    def send_message(self):
        '''
        sends message to server
        if message is 'Bye' ends program
         
        '''
          
    def start_game(self,id):
        
        # Call this function so the Pygame library can initialize itself
        pygame.init()
        # Create an 800x600 sized screen
        screen = pygame.display.set_mode([800, 600])
        # This sets the name of the window
        pygame.display.set_caption('Fingers')
        clock = pygame.time.Clock()
        done = False
        while done == False:
            clock.tick(10)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    done = True
                    pygame.quit()
        
    def process_message(self):
        '''
        
        Recieve xml data as parameter and calls appropriate methods 
        for specific type of messges
        '''
        messageType = self.root.tag
        print '****', self.root[0].tag
        if messageType == "ChatMessage":
            self.messageDispley.insert(END,self.root[0].text+'\n')
            # if game is full we receive message and set shared object canJoin to false 
            if self.root[0].text.startswith('Unable to join'):
                self.canJoin = False
                
            #trying to start game ****TO BE CHANGED***
            if self.root[0].text.startswith('Start game'):
                self.gameThread = thread.start_new_thread(self.start_game, (2,))
                 
        elif messageType == "ListOfGames":
            #****Mora posebna metoda koja nema parametre jedino tako radi***
            self.list_all_games(self.gameList)
        elif messageType == "ListOfPlayers":
            self.list_all_games(self.playersList)
            
        else:
            print "Neka greska"
        
    def list_all_games(self,listBox):
        '''
        Reads all <game> elements from xml
        and shows them in gameList listbox
        '''
        #******Ovov nekad radi nekad ne*********
        lis = []
        print self.root[0]
        for el in iter(self.root[0]):
            lis.append(el.text)
       
        listBox.delete(0, END)
        for e in lis:
            #t = e.text
            listBox.insert(END,e)
        
    
    def receive_server_messages(self,id):
        '''
        receives messages while main thread is running
        
        '''
        #creating event for disabling thread while event is not set
        self.event = threading.Event()
        while not self.end:
            try:
                mes = self.client.comSocket.recv(1024)
                # http://lxml.de/tutorial.html
                print mes + '*****'
                self.root = etree.fromstring(mes) 
                
                self.event.clear() 
                self.process_message()
                self.event.set()
                
            except:
                
                traceback.print_exc()
        

        
        
        
        