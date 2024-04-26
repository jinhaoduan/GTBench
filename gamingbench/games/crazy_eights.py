

from gamingbench.games.openspiel_adapter import OpenSpielGame

# TO-DO: 
class CrazyEights(OpenSpielGame):


    def __init__(self) -> None:
        super().__init__("crazy_eights")
        self.game_name = 'crazy_eights'
        pass
    
    def openspiel_action_to_agent(self, action):
        pass

    def openspiel_observation_to_dict(self, current_player_idx, openspiel_obs):
        pass

    def agent_action_to_openspiel(self, action):
        pass

