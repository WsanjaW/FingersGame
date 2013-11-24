

import java.util.Vector;


public class GameState {
	
	private boolean gameOver;
	private int playersTurn;
	private Vector<Player> players;
	
	

	public GameState(boolean gameOver, int playersTurn, Vector<Player> players) {
		this.gameOver = gameOver;
		this.playersTurn = playersTurn;
		this.players = players;
		for (Player player : this.players) {
			player.setOut(false);
		}
	}
	/**
	 * 
	 * Method that changes game state with data
	 * from move.
	 * @param m current move in game
	 * TODO Check if game is over.
	 */
	public void changeGameState(Move m) {
		
		int numFingers = 0;
		int hittingIndex = -1;
		int hittedIndex = -1;
		for (int i=0;i<players.size();i++) {
			if(players.get(i).getSocketNumber() == m.getPlayerPlayed()){
				if(m.getHittingHand().equals("left")) {
					numFingers=players.get(i).getFingersLeft();
					//handle separation case
					if (m.getHittedHand().equals("separation")) {
						int numHittedFingers = players.get(i).getFingersRight();
						players.get(i).setFingersLeft(numHittedFingers/2);
						players.get(i).setFingersRight(numHittedFingers/2);
					}
				}
				if(m.getHittingHand().equals("right")){ 
					numFingers=players.get(i).getFingersRight();
					//handle separation case
					if (m.getHittedHand().equals("separation")) {
						int numHittedFingers = players.get(i).getFingersLeft();
						players.get(i).setFingersLeft(numHittedFingers/2);
						players.get(i).setFingersRight(numHittedFingers/2);
					}
				}
				hittingIndex = i;
				hittedIndex = findNextPlayer(hittingIndex);
				break;
			}
		}
		
	
		if(m.getHittedHand().equals("left")){
			int numHittedFingers = players.get(hittedIndex).getFingersLeft();
			players.get(hittedIndex).setFingersLeft((numFingers+numHittedFingers)%5);
			
		}
		else{
			int numHittedFingers = players.get(hittedIndex).getFingersRight();
			players.get(hittedIndex).setFingersRight((numFingers+numHittedFingers)%5);
		}
		players.get(hittedIndex).setOut(isPlayerOut(players.get(hittedIndex))); //check if hitted player is out of game
		int nextPlayerToPlay = findNextPlayer(hittingIndex);
		//check if game is over and sets gameOver attribute
		// game is over if there is only one player left i.e nextPlayerToPlay == hittingIndex
		gameOver = (nextPlayerToPlay == hittingIndex);
		playersTurn = players.get(nextPlayerToPlay).getSocketNumber();
	}
	/**
	 * 
	 * If some player is out we must skip him
	 * @param currentPlayerIndex
	 * @return next active player in game
	 */
	public int findNextPlayer(int currentPlayerIndex){
		int index = currentPlayerIndex + 1;
		if(index == (players.size())){
			index = 0;
		}
		while(index != currentPlayerIndex){
			if(index == (players.size())){
				index = 0;
			}
			if(!players.get(index).isOut()){
				break;
			}
			else{
				index++;
			}
		}
		return index;
	}
	/**
	 * 
	 * @param player
	 * check whether player has no fingers left and set paramater isOut
	 * 
	 */
	public boolean isPlayerOut(Player player){
		return player.getFingersLeft() == 0 && player.getFingersRight() == 0;
			
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
