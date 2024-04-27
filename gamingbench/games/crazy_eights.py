

from gamingbench.games.openspiel_adapter import OpenSpielGame

# TO-DO: 
class CrazyEights(OpenSpielGame):


    def __init__(self) -> None:
        super().__init__("crazy_eights")
        self.game_name = 'crazy_eights'
    
    def openspiel_action_to_agent(self, action):

       pass
    
    #    cards = observations.get('cards', []) 
    # top_card = observations.get('top_card', [])
    # moves = observations.get('moves', [])
    # player_idx = observations.get('player_idx', "")

#  // The action space of this game is as follows.
# // action id 0, 1,..., 51: play/deal a card from the standard 52-card deck.
# // action id 52: a player draw a card from the dealer's deck.
# // action id 53: a player passes if it had already drawn max_draw_cards.
# // action id 54, 55, 56, 57: a player nominate one of the four suit.
# // (for chance) action id 0, 1,...., 51 are cards to be drawn
# // action id 52, 53, ...., 52 + num_player-1: decide the dealer.



    def openspiel_observation_to_dict(self, current_player_idx, openspiel_obs):
        
        
        cards = None 
        top_card = None 
        moves = None 
        player_idx = current_player_idx
        
        res = {
            "cards": cards, 
            "top_card": top_card, 
            "moves": moves, 
            "player_idx": player_idx 
        }
        
        
        return res

    def agent_action_to_openspiel(self, action):
        pass

