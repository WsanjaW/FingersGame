import java.net.Socket;

import com.thoughtworks.xstream.annotations.XStreamOmitField;


public class Player {
	private String name;
	@XStreamOmitField
	private Socket socket;
	private int socketNumber;
	private String gameName;
	private int fingersLeft;
	private int fingersRight;
	
	
	public Player(String name, Socket socket){
		this.name = name;
		this.socket = socket;
		this.socketNumber = socket.getPort();
		fingersLeft = 1;
		fingersRight = 1;
	}

	/**
	 * @return the name
	 */
	public String getName() {
		return name;
	}

	/**
	 * @param name the name to set
	 */
	public void setName(String name) {
		this.name = name;
	}

	/**
	 * @return the socket
	 */
	public Socket getSocket() {
		return socket;
	}

	/**
	 * @param socket the socket to set
	 */
	public void setSocket(Socket socket) {
		this.socket = socket;
	}

	/**
	 * @return the gameName
	 */
	public String getGameName() {
		return gameName;
	}

	/**
	 * @param gameName the gameName to set
	 */
	public void setGameName(String gameName) {
		this.gameName = gameName;
	}
	
	public int getFingersLeft() {
		return fingersLeft;
	}

	public void setFingersLeft(int fingersLeft) {
		this.fingersLeft = fingersLeft;
	}

	public int getFingersRight() {
		return fingersRight;
	}

	public void setFingersRight(int fingersRight) {
		this.fingersRight = fingersRight;
	}

	public int getSocketNumber() {
		return socketNumber;
	}

	public void setSocketNumber(int socketNumber) {
		this.socketNumber = socketNumber;
	}
	
}
