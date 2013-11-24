'''
Created on Nov 6, 2013

@author: SanjaK
'''

import pygame


class PlayGame:
    '''
    Class in which all game play logic is done
    '''
    def __init__(self, players, index):
        
            
        self.set_game_parametars(players, index)
        
                     
        
                         
    def set_game_parametars(self,players,index):
        
        # set all needed parameters
        self.playersList = players
        self.currentIndex = index
        self.currentPlayer = self.playersList[self.currentIndex];
        self.ourField = self.currentPlayer.field
        self.nextField = None
      
       
        self.firstClick = True
        self.secondClick = False
        self.hitting = None
        self.hitted  = None
    
    def set_next_plyer_index(self):
        
        self.nextIndex = self.find_next_player_index(self.currentIndex)
        self.nextPlayer = self.playersList[self.currentIndex]
        self.nextField = self.nextPlayer.field
    
    def find_next_player_index(self,currentPlayerIndex):
        '''
        finds index of next player on turn in playersList
        '''
        index = currentPlayerIndex + 1
        if index == len(self.playersList):
            index = 0
        
        while index != currentPlayerIndex:
            #print self.game.playersList[index].isOut
            #print type(self.game.playersList[index].isOut)
            if index ==  len(self.playersList):
                index = 0
            if str(self.playersList[index].isOut) == 'false':
                #print 'aaaaaaaaa'
                break
            else:
                index += 1;
        #print index
        return index
    
    def play_turn(self,x,y):
        
                                
        if self.firstClick:
            # check if left hand picture is clicked
            if self.ourField.image1.get_rect(center=self.ourField.get_centers()[0]).collidepoint(x, y) and self.currentPlayer.fingersLeft != 0:
                self.hitting = 'left'
                self.firstClick = False
                self.secondClick = True
                # check if right hand picture is clicked
            elif self.ourField.image2.get_rect(center=self.ourField.get_centers()[1]).collidepoint(x, y) and self.currentPlayer.fingersRight != 0:
                self.hitting = 'right'
                self.firstClick = False
                self.secondClick = True
        elif self.secondClick:
            # check if left hand picture is clicked
            if self.nextField.image1.get_rect(center=self.nextField.get_centers()[0]).collidepoint(x, y) and self.nextPlayer.fingersLeft != 0:
                self.hitted = 'left'
                self.secondClick = False
                #this turn over reset firstClick and secondClick
                self.firstClick = True
                self.secondClick = False
                                        
                return (self.hitting, self.hitted)
            # check if right hand picture is clicked
            elif self.nextField.image2.get_rect(center=self.nextField.get_centers()[1]).collidepoint(x, y) and self.nextPlayer.fingersRight != 0:
                                        
                self.hitted = 'right'
                self.secondClick = False
                #this turn over reset firstClick and secondClick
                self.firstClick = True
                self.secondClick = False
                return (self.hitting, self.hitted)
    
class Colors:
    '''
    '''
    WHITE = (255, 255, 255)

class Constants:
    '''
    '''
    SCREEN_SIZE = [800,600]
    SCREEN_CAPITON = 'Fingers game'
    
    