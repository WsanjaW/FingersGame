'''
Created on Jul 6, 2013

@author: SanjaK
'''
from socket import socket


class ChatClient():
    '''
    Main class for game
    Handles network communication 
    
    '''
    
    def __init__(self):
              
        self.comSocket = None
       
        
    def connect_to_server(self):
        '''
        Connect to server
        '''
        self.comSocket = socket()      
        host = 'localhost'
        port = 1234
        try:               
            self.comSocket.connect((host, port))
            print self.comSocket.getpeername()
            print self.comSocket.getsockname()
            
        except:
            print 'Error'
    
    def send_message(self,mess):
        try:
            self.comSocket.send(str(mess)+'\n')
        except:
            print 'Unable to send message'
 
        
        
        
        
        
        
