

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
    private static Map<String,GameState> gameStateMap;

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
        gameStateMap = new HashMap<String, GameState>();
        
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
                    new ClientHandler(userSocket, allUsers,gameMap,gameStateMap);
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
    private Map<String, Vector<Player>> gameMap;
    private Map<String,GameState> gameStateMap;
    
    

	public ClientHandler(Socket chatSocket, Vector<Socket> chatVector,
			Map<String, Vector<Player>> map, Map<String, GameState> gameStateMap) {
		
		// Set up references to associated socket and Vector of users...
		userSocket = chatSocket;
		allUsers = chatVector;
		gameMap = map;
		this.gameStateMap = gameStateMap;
		xstream = new XStream(new StaxDriver());
		xstream.processAnnotations(Player.class);

		try {
			input = new Scanner(userSocket.getInputStream());
			output = new PrintWriter(userSocket.getOutputStream(), true);
		} catch (IOException ioEx) {
			ioEx.printStackTrace();
		}
		// Connecting user must send chat nickname as first transmission...
		chatName = input.nextLine();
		player = new Player(chatName, userSocket);
		allUsers.add(userSocket);
		// Notify all people in chatroom (including new arrival)
		// of the new arrival...
		
		ChatMessage msg = new ChatMessage(chatName
				+ " has entered the chatroom!");
		String xml = xstream.toXML(msg);

		broadcast(xml, allUsers);
		try {
			Thread.sleep(400);
		} catch (InterruptedException e) {

			e.printStackTrace();
		}
		broadcast(createListOfGameMessage(), allUsers);

	}

    public void run() {
        String received;
        do {
        	//Accept message from client on 
        	//the socket's input stream...
        	try {
        		received = input.nextLine();
			} catch (NoSuchElementException e) {
				break;
			}
            

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
            //START GAME
            else if(received.equals("Start game")){
    
            	System.out.println("Nova igra startovana");
            	GameState gameState = new GameState(false, userSocket.getPort(),gameMap.get(player.getGameName()));//creates game state 
            	System.out.println(received);
            	System.out.println(player.getGameName());
            	String xml = xstream.toXML(new ChatMessage("Start game"));
            	broadcast(xml, getSocketVector(gameMap.get(player.getGameName())));
            	gameStateMap.put(player.getGameName(),gameState);//puts new game state in map so everyone can see it
            	try {
            		Thread.sleep(400);
            		System.out.println(xstream.toXML(gameStateMap.get(player.getGameName())));
					broadcast(xstream.toXML(gameStateMap.get(player.getGameName())),getSocketVector(gameMap.get(player.getGameName())));
				} catch (InterruptedException e) {
					// TODO Auto-generated catch block
					e.printStackTrace();
				}
            	
            }
            //QUIT
            else if (received.equals("QUIT")) {
            	
            	//reset fileds for player who left 
				gameMap.get(player.getGameName()).remove(player);
				
				//if all players left remove game from game map
				if (gameMap.get(player.getGameName()).size() == 0) {
					System.out.println("IZASLI SVI");
					gameMap.remove(player.getGameName());
					gameStateMap.remove(player.getGameName());
				}
				else if(!player.isOut()) {
					// game is over, send new state to other players
					gameStateMap.get(player.getGameName()).setGameOver(true);

					// if somebody left in game send new state
					if (gameMap.get(player.getGameName()) != null) {
						broadcast(xstream.toXML(gameStateMap.get(player
								.getGameName())),
								getSocketVector(gameMap.get(player
										.getGameName())));
					}
				}
				else {
					
				}
				
				
				//reset fileds for player who left 
				player.setFingersLeft(1);
				player.setFingersRight(1);
				allUsers.add(player.getSocket());
				player.setGameName(null);
		        ChatMessage msg = new ChatMessage(chatName + " has entered the chatroom!");
		        String xml = xstream.toXML(msg);
		        //send him initial massages
				broadcast(xml,allUsers);
				try {
					Thread.sleep(400);
				} catch (InterruptedException e) {
					
					e.printStackTrace();
				}
				broadcast(createListOfGameMessage(),allUsers);
				
				
				
			}
            //CHAT MESSAGE
            else if (xstream.fromXML(received) instanceof ChatMessage) {
				
            	ChatMessage newMesg = (ChatMessage)xstream.fromXML(received);
				newMesg.setMessage(chatName+": "+newMesg.getMessage());
				String xml = xstream.toXML(newMesg);
				System.out.println(newMesg);
				if(player.getGameName() == null){
					broadcast(xml,allUsers); //DONE check whether user belongs to allUsers or in gameMap
				}
				else{
					System.out.println(player.getGameName());
					broadcast(xml,getSocketVector(gameMap.get(player.getGameName())));
				}
				
			} 
            //JOIN GAME
            else if(xstream.fromXML(received) instanceof JoinGame) {
            	
            	JoinGame joinMessage = (JoinGame)xstream.fromXML(received);
            	String selectedGame = joinMessage.getGame();
            	//checks if there is less than four players in selected game or if game already started
            	if (gameMap.get(selectedGame).size() == 4 || gameStateMap.containsKey(selectedGame)) {
            		
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
            //MOVE
            else if(xstream.fromXML(received) instanceof Move){
            	Move move = (Move)xstream.fromXML(received);
            	System.out.println(received);
            	gameStateMap.get(player.getGameName()).changeGameState(move);
            	broadcast(xstream.toXML(gameStateMap.get(player.getGameName())),getSocketVector(gameMap.get(player.getGameName())));
            }
            
            //Repeat above until 'Bye' sent by client...
        }
        while (!received.equals("Bye") || userSocket == null); //TODO do something with this
		
        try {
			if (userSocket != null) {
				System.out.println("Closing down connection...");
				userSocket.close();
			}
		} catch (IOException ioEx) {
			System.out.println("Unable to disconnect!");
		}
		allUsers.remove(userSocket);
		broadcast(xstream.toXML(new ChatMessage(chatName + " has left the chatroom.")), allUsers);
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