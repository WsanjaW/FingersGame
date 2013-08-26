

import java.io.*;
import java.net.*;
import java.util.*;

import com.thoughtworks.xstream.XStream;
import com.thoughtworks.xstream.io.xml.StaxDriver;


public class FingerGameServer {

    private static ServerSocket serverSocket;
    private static final int PORT = 1234;
    private static Vector<Socket> allUsers;

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
                    new ClientHandler(userSocket, allUsers);
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
    XStream xstream;

    public ClientHandler(Socket chatSocket,
            Vector<Socket> chatVector) {
//Set up references to associated socket and Vector
//of users...
        userSocket = chatSocket;
        allUsers = chatVector;
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
        allUsers.add(userSocket);
//Notify all people in chatroom (including new arrival)
//of the new arrival...
        
        ChatMessage msg = new ChatMessage(chatName + " has entered the chatroom!");
        XStream xstream = new XStream(new StaxDriver());
        String xml = xstream.toXML(msg);
        //xstream = null; //promeni da ne bude lokalna promenjiva
		
		Vector<String> listaIgara = new Vector<String>();
		listaIgara.add("SanjasGame");
		listaIgara.add("BuhasGame");
		ListOfGames msg1 = new ListOfGames(listaIgara);
		String xml1 = xstream.toXML(msg1);
        
		broadcast(xml);
		for (int i = 0; i < 700000; i++) {
			
		}
		broadcast(xml1);
		
    }

    public void run() {
        String received;
        do {
//Accept message from client on
//the socket's input stream...
            received = input.nextLine();
//Send message to all users, prepending
//the sender's nickname...
            

            if (xstream.fromXML(received) instanceof ChatMessage) {
				
            	ChatMessage newMesg = (ChatMessage)xstream.fromXML(received);
				newMesg.setMessage(chatName+": "+newMesg.getMessage());
				String xml = xstream.toXML(newMesg);
				broadcast(xml);
				
			} else {

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
        broadcast(chatName +"has left the chatroom.");
    }

    public void broadcast(String chat) {
        Socket socket;
        PrintWriter output;
        for (Socket userSocket : allUsers) {
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
}