'''
Created on Sep 8, 2013

@author: Aleksandar
'''

class Player():
    '''
    Represents data needed for game play
    '''


    def __init__(self,playerName,socketNumber):
        '''
        Assign values that are known to player attributes
        socketNumber is specific number(int) of current
        player's socket and it is used as unique id.
        ''' 
        self.playerName = playerName
        self.socketNumber = socketNumber
        self.fingersLeft = 1
        self.fingersRight = 1
        self.field = None
        
    def change_state(self,fingersLeft,fingersRight):
        '''
        Changes number of fingers
        '''
        self.fingersLeft = fingersLeft
        self.fingersRight = fingersRight
        
    def draw_player(self,screen):
        
        path = "D:\\ProjekiGit\\FingersGame\\FingersClient\\resources\\"
        #set left hand picture
        if self.fingersLeft == 1:
            self.field.image1 = pygame.image.load(path + "finger1.png")
        elif self.fingersLeft == 2:
            self.field.image1 = pygame.image.load(path +"finger2.png")
        elif self.fingersLeft == 3:
            self.field.image1 = pygame.image.load(path +"finger3.png")
        elif self.fingersLeft == 4:
            self.field.image1 = pygame.image.load(path +"finger4.png")
        elif self.fingersLeft == 5:
            self.field.image1 = pygame.image.load(path +"finger5.png")
        
        #set right hand picture
        if self.fingersRight == 1:
            self.field.image2 = pygame.image.load(path +"fingerright1.png")
        elif self.fingersRight == 2:
            self.field.image2 = pygame.image.load(path +"fingerright2.png")
        elif self.fingersRight == 3:
            self.field.image2 = pygame.image.load(path +"fingerright3.png")
        elif self.fingersRight == 4:
            self.field.image2 = pygame.image.load(path +"fingerright4.png")
        elif self.fingersRight == 5:
            self.field.image2 = pygame.image.load(path +"fingerright5.png")
        self.field.draw_field(screen)
        
        
'''
Created on Sep 8, 2013

@author: Aleksandar
'''
import pygame

class Field():
    '''
    Class that represents player hands and position on screen in pygame
    '''


    def __init__(self,image1,image2,position1,position2,rotation):
        '''
        image is picture on screen with position position1 and position2
        and rotation is pictures rotation from first pair of hands
        
        '''
        self.position1 = position1
        self.position2 = position2
        self.rotation = rotation
        self.image1 = image1
        self.image2 = image2
        
    def draw_field(self,screen):
        '''
        draws pictures on given screen
        '''
        
        screen.blit(pygame.transform.rotate(self.image1,self.rotation).convert(), self.position1)
        screen.blit(pygame.transform.rotate(self.image2,self.rotation).convert(),self.position2)

    def get_centers(self):
        '''
        returns list of tuples that represents centers of picture
        '''
        centers = []
        center1 = (self.position1[0]+self.image1.get_width()/2,
                    self.position1[1]+self.image1.get_height()/2)
        center2 = (self.position2[0]+self.image2.get_width()/2,
                   self.position2[1]+self.image2.get_height()/2)
        
        return [center1,center2]


class GameState():
    '''
    Class in which we create list of player in specific 
    game and assign them positions appropriate for every client's view
    '''    
    POSITION_ONE    = ((275,485),(395,485),0)
    POSITION_TWO    = ((680,300),(680, 180),90)
    POSITION_THEREE = ((395,15),(275,15),180)
    POSITION_FOUR   = ((15,180),(15,300),270)
    
    def __init__(self,xmlState, socketNumber):
        '''
        Creates list of players in game, playersList, using
        data in xmlState and assign them positions on screen
        socketNumber is specific number(int) of current
        player's socket and it is used as unique id.
        '''
        self.playersList = self.unpackXML(xmlState)
        self.ourIndex = self.find_index(socketNumber)
        self.newList = self.create_new_list()
        self.assign_field_positions()
       
                
    def changeGameState(self,xmlState):
        '''
        Changes number of fingers on players hands
        from xmlState
        '''
        self.playerTurn = int(xmlState[1].text)
        i = 0
        for el in iter(xmlState):
            if el.tag == 'players':
                for elem in iter(el):
                    self.playersList[i].fingersLeft = int(elem[3].text)
                    self.playersList[i].fingersRight = int(elem[4].text)
                    i += 1
                                             
        
            
    def unpackXML(self,xmlState):
        '''
        Unpack xmlState recieved from server and
        create Player object which are returned
        in playersList
        '''
        playersList = []
        self.playerTurn = int(xmlState[1].text)
        for el in iter(xmlState):
            if el.tag == 'players':
                for elem in iter(el):
                    playersList.append(Player(elem[0].text,int(elem[1].text))) #extract only player name for Player constructor
                                       
        return playersList
    
    def find_index(self,socketNumber):
        '''
        returns index of a current player in list 
        of all players in game using socketNumber
        which is unique for every player
        
        '''
        currentPlayer = [x for x in self.playersList if x.socketNumber == socketNumber] 
        index = self.playersList.index(currentPlayer[0])
        return index
    
    def create_new_list(self):
        '''
        Creates helper new_list which represent
        order from every player's 'point of view'
        '''
        new_list = [x for x in self.playersList]
        i = 0
        while i < self.ourIndex:
            new_list.append(new_list.pop(0))
            i+=1
        return new_list
    
    def assign_field_positions(self):
        '''
        Assign positions to field attribute in player class
        so every player in playersList is on the bottom in his 
        client window.
        Also it saves order of player's turns
        '''
       
        image1 = pygame.image.load("D:\\ProjekiGit\\FingersGame\\FingersClient\\resources\\finger1.png")
        image2 = pygame.image.load("D:\\ProjekiGit\\FingersGame\\FingersClient\\resources\\fingerright1.png")
      
        i = 0
        positions = [GameState.POSITION_ONE, GameState.POSITION_TWO, GameState.POSITION_THEREE, GameState.POSITION_FOUR]
        for elem in self.newList:
            #change playersLists field attribute with respect to order in new_list
            self.playersList[self.find_index(elem.socketNumber)].field = Field(image1,image2,positions[i][0],positions[i][1],positions[i][2])
            i+=1
                     
            
    def draw_state(self,screen):
          
        for el in self.playersList:
            el.draw_player(screen)
           
          
          
        
        
             
        
        
        
    
    
    