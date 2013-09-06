

import java.io.*;
import java.net.*;
import java.util.*;

import com.thoughtworks.xstream.XStream;
import com.thoughtworks.xstream.io.xml.StaxDriver;


public class FingerGameServer {

    private static ServerSocket serverSocket;
    private static final int PORT = 1234;
    private static Vector<Socket> allUsers;
    private static Map<String, Vector<Player>> gameMap;
    

    public static void main(String[] args) throws IOException {
        System.out.println("\nOpening port...\n");
        try {
            serverSocket = new ServerSocket(PORT);
        } catch (IOException ioEx) {
            System.out.println("\nUnable to set up port!");
            System.exit(1);
        }
        Socket userSocket = null;
        allUsers = new Vector<Socket>();
        
        //Map of created games
        gameMap = new HashMap<String, Vector<Player>>();
        
        do {
//Wait for client...
            userSocket = serverSocket.accept();
            System.out.println("\nNew client accepted.\n");
            /*
            Create a thread to handle communication with
            this client and pass the constructor for this
            thread references to the relevant socket and
            the Vector of all open sockets...
             */
            ClientHandler handler =
                    new ClientHandler(userSocket, allUsers,gameMap);
            handler.start();//As usual, this method calls run.
        } while (true);
    }
}

class ClientHandler extends Thread {

    private Socket userSocket;
    private String chatName;
    private Vector<Socket> allUsers;
    private Scanner input;
    private PrintWriter output;
    private XStream xstream;
    private Player player;
    Map<String, Vector<Player>> gameMap;
    

    public ClientHandler(Socket chatSocket,
            Vector<Socket> chatVector, Map<String, Vector<Player>> map) {
//Set up references to associated socket and Vector
//of users...
        userSocket = chatSocket;
        allUsers = chatVector;
        gameMap = map; 
       
        xstream = new XStream(new StaxDriver());
       
        try {
            input = new Scanner(userSocket.getInputStream());
            output = new PrintWriter(
                    userSocket.getOutputStream(), true);
        } catch (IOException ioEx) {
            ioEx.printStackTrace();
        }
//Connecting user must send chat nickname as first
//transmission...
        chatName = input.nextLine();
        player = new Player(chatName, userSocket);
        allUsers.add(userSocket);
//Notify all people in chatroom (including new arrival)
//of the new arrival...
        
        ChatMessage msg = new ChatMessage(chatName + " has entered the chatroom!");
        xstream = new XStream(new StaxDriver());
        String xml = xstream.toXML(msg);
        
		broadcast(xml,allUsers);
		try {
			Thread.sleep(400);
		} catch (InterruptedException e) {
			
			e.printStackTrace();
		}
		broadcast(createListOfGameMessage(),allUsers);
		
    }

    public void run() {
        String received;
        do {
        	//Accept message from client on
        	//the socket's input stream...
            received = input.nextLine();

            //CREATE GAME
            //Adds new game into gameMap and broadcast new state 
            if(received.equals("Create game")){
            	
            	String gameName = chatName+"sGame";
            	boolean unique = false;
            	int i = 1;
            	//checks if game name is unique
                while (!unique) {
					if (!gameMap.containsKey(gameName)) {
						unique = true;
					}
					else {
						gameName = chatName + i + "sGame";
						i++;
					}
				}
            	            	
            	player.setGameName(gameName);
            	gameMap.put(gameName, new Vector<Player>());
            	gameMap.get(gameName).add(player);
            	allUsers.remove(userSocket);
            	
            	ChatMessage msg = new ChatMessage("You have succesfully created the game!");
            	
            	broadcast(xstream.toXML(msg), getSocketVector(gameMap.get(gameName)));
            	
            	//send list of players just for player that created the game
            	ListOfPlayers players = new ListOfPlayers(getPlayerNames(gameMap.get(gameName)));
            	sendMessage(xstream.toXML(players),player.getSocket());
            	broadcast(createListOfGameMessage(),allUsers);
            	
            	
            }
            //CHAT MESSAGE
            else if (xstream.fromXML(received) instanceof ChatMessage) {
				
            	ChatMessage newMesg = (ChatMessage)xstream.fromXML(received);
				newMesg.setMessage(chatName+": "+newMesg.getMessage());
				String xml = xstream.toXML(newMesg);
				if(player.getGameName() == null){
					broadcast(xml,allUsers); //DONE check whether user belongs to allUsers or in gameMap
				}
				else{
					broadcast(xml,getSocketVector(gameMap.get(player.getGameName())));
				}
				
			} 
            //JOIN GAME
            else if(xstream.fromXML(received) instanceof JoinGame) {
            	
            	JoinGame joinMessage = (JoinGame)xstream.fromXML(received);
            	String selectedGame = joinMessage.getGame();
            	//checks if there is less than four players in selected game
            	if (gameMap.get(selectedGame).size() == 4) {
            		
            		//if game is full send message 
            		ChatMessage msg = new ChatMessage("Unable to join, game is full.");
            		sendMessage(xstream.toXML(msg), player.getSocket());
					
				} else {
					player.setGameName(selectedGame);
	            	gameMap.get(selectedGame).add(player);
	            	allUsers.remove(userSocket);
	            	
	            	ListOfPlayers players = new ListOfPlayers(getPlayerNames(gameMap.get(selectedGame)));
	            	String XMLNames = xstream.toXML(players);
	            	broadcast(XMLNames, getSocketVector(gameMap.get(selectedGame)));
				}
            	
            	
            	
            	
            	
            	
            	
            	

			}
            
//Repeat above until 'Bye' sent by client...
        } while (!received.equals("Bye"));
        try {
            if (userSocket != null) {
                System.out.println(
                        "Closing down connection...");
                userSocket.close();
            }
        } catch (IOException ioEx) {
            System.out.println("Unable to disconnect!");
        }
        allUsers.remove(userSocket);
        broadcast(chatName +"has left the chatroom.",allUsers);
    }
    
   

	private Vector<String> getPlayerNames(Vector<Player> vector) {
		Vector<String> names = new Vector<String>();
    	for (int i = 0; i < vector.size(); i++) {
    		names.add(vector.get(i).getName());
		}
		return names;
	}

	private Vector<Socket> getSocketVector(Vector<Player> vector) {
		
    	Vector<Socket> sockets = new Vector<Socket>();
    	for (int i = 0; i < vector.size(); i++) {
			sockets.add(vector.get(i).getSocket());
		}
		return sockets;
	}

	//added additional parameter to handle sending messages to different groups of users 
    public void broadcast(String chat, Vector<Socket> users) {
        
        PrintWriter output;
        for (Socket userSocket : users) {
            try {
                output = new PrintWriter(
                        userSocket.getOutputStream(), true);
                output.println(chat);
            } catch (IOException ioEx) {
                allUsers.remove(userSocket);
                ioEx.printStackTrace();
            }
        }
    }
    //sends message to one user
    public void sendMessage(String mes, Socket user){
    	try {
            output = new PrintWriter(
                    userSocket.getOutputStream(), true);
            output.println(mes);
        } catch (IOException ioEx) {
            allUsers.remove(userSocket);
            ioEx.printStackTrace();
        }
    }
    //from gameMap creates list of game names
    public String createListOfGameMessage(){
    	
    	Vector<String> games = new Vector<String>();
    	for (String key : gameMap.keySet()){
    		games.add(key);
    	}
    	ListOfGames msg1 = new ListOfGames(games);
		String xml1 = xstream.toXML(msg1);
		return xml1;
    }
}