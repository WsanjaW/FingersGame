/**
 * 
 * @author Aleksandar
 * Class that encapsulates chatMessage and 
 * it is used with XStream for easier server-client communication.
 * http://xstream.codehaus.org/tutorial.html
 */
public class ChatMessage {
	
	//Body of a message
	private String message;
	
	public ChatMessage(String message){
		this.message = message;
	}
	
	public String getMessage() {
		return message;
	}
	

}
