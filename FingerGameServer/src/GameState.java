import java.util.Vector;


public class GameState {
	
	private boolean gameOver;
	private int playersTurn;
	private Vector<Player> players;
	

	public void createGameState(boolean gameOver, int playersTurn, Vector<Player> players) {
		this.gameOver = gameOver;
		this.playersTurn = playersTurn;
		this.players = players;
	}
	/**
	 * 
	 * Method that changes game state with data
	 * from move.
	 * @param m current move in game
	 * TODO Check if game is over.
	 */
	public void changeGameState(Move m){
		int numFingers = 0;
		int hittingIndex = -1;
		int hittedIndex = -1;
		for (int i=0;i<players.size();i++) {
			if(players.get(i).getSocketNumber() == m.getPlayerPlayed()){
				if(m.getHittingHand().equals("left")) 
					numFingers=players.get(i).getFingersLeft();
				if(m.getHittingHand().equals("right")) 
					numFingers=players.get(i).getFingersRight();
				hittingIndex = i;
				hittedIndex = i+1;
				if(hittedIndex == (players.size())){
					hittedIndex = 0;
				}
				break;
			}
		}
		if(m.getHittedHand().equals("left")){
			int numHittedFingers = players.get(hittedIndex).getFingersLeft();
			players.get(hittedIndex).setFingersLeft(numFingers+numHittedFingers);
			
		}
		else{
			int numHittedFingers = players.get(hittedIndex).getFingersRight();
			players.get(hittedIndex).setFingersRight(numFingers+numHittedFingers);
		}
		playersTurn = players.get(hittedIndex).getSocketNumber();
	}
	/**
	 * @return the gameOver
	 */
	public boolean isGameOver() {
		return gameOver;
	}
	/**
	 * @param gameOver the gameOver to set
	 */
	public void setGameOver(boolean gameOver) {
		this.gameOver = gameOver;
	}
	/**
	 * @return the playersTurn
	 */
	public int getPlayersTurn() {
		return playersTurn;
	}
	/**
	 * @param playersTurn the playersTurn to set
	 */
	public void setPlayersTurn(int playersTurn) {
		this.playersTurn = playersTurn;
	}
	/**
	 * @return the players
	 */
	public Vector<Player> getPlayers() {
		return players;
	}
	/**
	 * @param players the players to set
	 */
	public void setPlayers(Vector<Player> players) {
		this.players = players;
	}
}
