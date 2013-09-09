/**
 * 
 */

/**
 * @author SanjaK
 * Class that represent one move in a game.
 *
 */
public class Move {
	private int playerPlayed;
	private String hittingHand;//Takes values either 'left' or 'right' 
	private String hittedHand;
	
	
	public Move(int playerPlayed, String hittingHand, String hittedHand) {
		super();
		this.playerPlayed = playerPlayed;
		this.hittingHand = hittingHand;
		this.hittedHand = hittedHand;
	}
	/**
	 * @return the playerPlayed
	 */
	public int getPlayerPlayed() {
		return playerPlayed;
	}
	/**
	 * @param playerPlayed the playerPlayed to set
	 */
	public void setPlayerPlayed(int playerPlayed) {
		this.playerPlayed = playerPlayed;
	}
	/**
	 * @return the hittingHand
	 */
	public String getHittingHand() {
		return hittingHand;
	}
	/**
	 * @param hittingHand the hittingHand to set
	 */
	public void setHittingHand(String hittingHand) {
		this.hittingHand = hittingHand;
	}
	/**
	 * @return the hittedHand
	 */
	public String getHittedHand() {
		return hittedHand;
	}
	/**
	 * @param hittedHand the hittedHand to set
	 */
	public void setHittedHand(String hittedHand) {
		this.hittedHand = hittedHand;
	}
	
	
}
