import java.net.Socket;

import com.thoughtworks.xstream.annotations.XStreamOmitField;


public class Player {
	private String name;
	@XStreamOmitField
	private Socket socket;
	private String gameName;
	
	public Player(String name, Socket socket){
		this.name = name;
		this.socket = socket;
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
	
}
