'''
Created on Jul 6, 2013

@author: SanjaK
'''
from socket import socket


class ChatClient():
    '''
    Main class for chat
    Handles network communication 
    One thread for sending messages and one for receiving
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
            
        except:
            print 'Error'
    
    def send_message(self,mess):
        self.comSocket.send(str(mess)+'\n')
            
 
        
        
        
        
        
        
