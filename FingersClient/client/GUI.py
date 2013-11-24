'''
Created on Jul 5, 2013

@author: SanjaK
'''


from Tkinter import Tk, Frame, Label, BOTH, Button,Listbox, StringVar, Entry, Text, LEFT, RIGHT, BOTTOM, E, N,CENTER,NW,W, S, END, DISABLED,NORMAL
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
from game import GameState

import sys

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
        self.startGameButton.config(state=DISABLED)
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
        #if nothing is selected
        if items == tuple():
            return
        # creating xml document to be send
        root2 = etree.Element("JoinGame")
        ge = etree.SubElement(root2, "game").text =  self.gameList.get(items[0])  
        
        self.client.send_message(etree.tostring(root2))
        #join massage send 
        self.joinEvent.clear()
        #first receive_server_messages thread needs to finish processing message from server        
        self.joinEvent.wait()
        print "BUHA"
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
        self.startGameButton.place(x=50, y=270)
        #can't start until somebody joins
        self.startGameButton.config(state=DISABLED)
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
        
    
    def find_next_player_index(self,currentPlayerIndex):
        '''
        finds index of next player on turn in playersList
        '''
        index = currentPlayerIndex + 1
        if index == len(self.game.playersList):
            index = 0
        
        while index != currentPlayerIndex:
            #print self.game.playersList[index].isOut
            #print type(self.game.playersList[index].isOut)
            if index ==  len(self.game.playersList):
                index = 0
            if str(self.game.playersList[index].isOut) == 'false':
                #print 'aaaaaaaaa'
                break
            else:
                index += 1;
        #print index
        return index
            
   
    def start_game(self,id):
        
        try:
            white = (255, 255, 255)
            # Call this function so the Pygame library can initialize itself
            pygame.init()
            # Create an 800x600 sized screen
            self.screen = pygame.display.set_mode([800, 600])
            # This sets the name of the window
            pygame.display.set_caption('Fingers game')
            clock = pygame.time.Clock()
            done = False
            firstClick = True
            secondClick = False
            # waits until process_message finish with game object   
            self.gameStateEvent.wait()
                     
            currentPlayer = self.game.playersList[self.game.ourIndex];
            ourField = currentPlayer.field
            nextField = None
                         
            
            hitting = None
            hitted  = None
          
            print "AAAAAAAAAAA"
            while done == False:
              
                clock.tick(10)
                nextIndex = self.find_next_player_index(self.game.ourIndex)
                nextPlayer = self.game.playersList[nextIndex]
                nextField = nextPlayer.field
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        #enable all filed for choosing game
                      
                        self.createGameButton.place(x=50, y=270)
                        self.joinGameButton.place(x=50, y=230)
                        self.nameText2.place(x=50,y=10)
                        self.gameList.place(x=50, y=30)
                        self.initialGameState = True
                        self.game = None
                        
                        self.client.send_message("QUIT")
                        pygame.quit()
                    
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        x, y = event.pos
                        # if game is over we can't play
                       
                        if self.game.gameOver == 'false':
                        
                            if self.client.comSocket.getsockname()[1] == self.game.playerTurn:
                                if firstClick:
                                    # check if left hand picture is clicked
                                    if ourField.image1.get_rect(center=ourField.get_centers()[0]).collidepoint(x, y):
                                        hitting = 'left'
                                        firstClick = False
                                        secondClick = True
                                    # check if right hand picture is clicked
                                    elif ourField.image2.get_rect(center=ourField.get_centers()[1]).collidepoint(x, y):
                                        hitting = 'right'
                                        firstClick = False
                                        secondClick = True
                                elif secondClick:
                                    # check if left hand picture is clicked
                                    if nextField.image1.get_rect(center=nextField.get_centers()[0]).collidepoint(x, y) and nextPlayer.fingersLeft != 0:
                                        hitted = 'left'
                                        secondClick = False
                                        #this turn over reset firstClick and secondClick
                                        firstClick = True
                                        secondClick = False
                                        
                                        self.send_move_message(hitting, hitted)
                                    # check if right hand picture is clicked
                                    elif nextField.image2.get_rect(center=nextField.get_centers()[1]).collidepoint(x, y) and nextPlayer.fingersRight != 0:
                                        
                                        hitted = 'right'
                                        secondClick = False
                                        #this turn over reset firstClick and secondClick
                                        firstClick = True
                                        secondClick = False
                                        self.send_move_message(hitting, hitted)
                                    #check if second hand is from same player and if separation is possible
                                    elif ourField.image1.get_rect(center=ourField.get_centers()[0]).collidepoint(x, y):
                                                                            
                                        if currentPlayer.fingersRight == 0 and (currentPlayer.fingersLeft == 2 or currentPlayer.fingersLeft == 4):                                       
                                            hitted = 'separation'
                                            secondClick = False 
                                            print "SANJA"
                                            #this turn over reset firstClick and secondClick
                                            firstClick = True
                                            secondClick = False
                                            self.send_move_message(hitting, hitted)
                                        else:
                                            firstClick = True
                                    elif ourField.image2.get_rect(center=ourField.get_centers()[1]).collidepoint(x, y):
                                        print "BUHA1"
                                        print currentPlayer.fingersLeft
                                        
                                        if currentPlayer.fingersLeft == 0 and (currentPlayer.fingersRight== 2 or currentPlayer.fingersRight == 4):                                       
                                            print "SANJA"
                                            hitted = 'separation'
                                            secondClick = False 
                                            #this turn over reset firstClick and secondClick
                                            firstClick = True
                                            secondClick = False
                                            self.send_move_message(hitting, hitted)
                                        else:
                                            firstClick = True
                                    
                                    
                                                                
                       
                #write text on screen
                myfont = pygame.font.SysFont("Comic Sans MS", 20)
                winnerFont = pygame.font.SysFont("Comic Sans MS", 36)
                #refresh screen
                self.screen.fill((0, 0, 0))
                
                if self.game.gameOver == 'true':
                    if not self.all_out():
                        labelWinner = winnerFont.render("**** Game over ****", 1, white)
                        labelWinner2 = winnerFont.render("**** somebody left :( *****", 1, white)
                    else:
                        labelWinner = winnerFont.render("*****Winner is " + self.return_winner_name() + " *****", 1, white)
                        labelWinner2 = winnerFont.render(" ", 1, white)
                    self.screen.blit(labelWinner, (180, 220))
                    self.screen.blit(labelWinner2, (180, 250))
                label1 = myfont.render("You: " + self.game.playersList[self.game.ourIndex].playerName, 1, white)
                label2 = myfont.render("Players turn: " + self.game.playersList[self.game.find_index(self.game.playerTurn)].playerName, 1, white)
                
                #add text
                self.screen.blit(label1, (40, 450))
                self.screen.blit(label2, (40, 480))       
                #draw hands         
                self.game.draw_state(self.screen)
                pygame.display.flip()
                
        except:
            traceback.print_exc()
            
    
    def all_out(self):
        '''
        checks if only one player
        is left in game
        '''
        return len([x for x in self.game.playersList if x.isOut == 'false']) == 1
    
    def return_winner_name(self):
        '''
        returns winers name
        '''
        return next(x.playerName for x in self.game.playersList if x.isOut == 'false')
    
    def send_move_message(self,hitting,hitted):
        '''
        creates and sends move message
        based on hitting and hitted hands
        '''
        xmlroot = etree.Element("Move")
        etree.SubElement(xmlroot, "playerPlayed").text = str(self.game.playerTurn)
        etree.SubElement(xmlroot, "hittingHand").text = hitting
        etree.SubElement(xmlroot, "hittedHand").text = hitted
        print etree.tostring(xmlroot)
        self.client.send_message(etree.tostring(xmlroot))
        
    def process_message(self):
        '''
        
        Recieve xml data as parameter and calls appropriate methods 
        for specific type of messges
        '''
                
        messageType = self.root.tag
        
        if messageType == "ChatMessage":
            self.messageDispley.insert(END,self.root[0].text+'\n')
            # if game is full we receive message and set shared object canJoin to false 
            if self.root[0].text.startswith('Unable to join'):
                print "SANJA"
                self.canJoin = False
                #unable to join massage processed so enable joinEvent, 
                self.joinEvent.set()
                
            #trying to start game ****TO BE CHANGED***
            if self.root[0].text.startswith('Start game'):
                self.game = None
                self.gameThread = thread.start_new_thread(self.start_game, (2,))
                
        elif messageType == "ListOfGames":
            #****Mora posebna metoda koja nema parametre jedino tako radi***
            self.list_all_games(self.gameList)
        elif messageType == "ListOfPlayers":
            
            self.list_all_games(self.playersList)
            #if there is more then tow players in game enable startGameButton
            if len(self.playersList.get(0, END)) > 1:
                self.startGameButton.config(state=NORMAL)
         
        elif messageType == "GameState":
            if self.initialGameState:
                self.gameStateEvent.clear()
                self.game = GameState(self.root,self.client.comSocket.getsockname()[1])
                self.gameStateEvent.set()
                self.initialGameState = False
            else:
               
                self.game.changeGameState(self.root)
                print str(self.game.playersList[self.game.ourIndex].fingersRight) + '->' + self.game.playersList[self.game.ourIndex].playerName
                
            
        else:
            print "Error while processing massages"
        
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
        
        #event must be defined here because in process_message we 
        # create another event for every message, no good.
        self.gameStateEvent = threading.Event()
        #creating event for disabling thread while event is not set
        self.joinEvent = threading.Event()
        
        self.initialGameState = True
        
        while not self.end:
            try:
                mes = self.client.comSocket.recv(1024)
                # http://lxml.de/tutorial.html
                print mes + '*****'
                self.root = etree.fromstring(mes) 
                
                self.gameStateEvent.clear()
                self.process_message()
                #massage processed so enable joinEvent,
                self.joinEvent.set()
              
                
            except:
                
                traceback.print_exc()
        

        
        
        
        
