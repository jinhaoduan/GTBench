

from gamingbench.games.openspiel_adapter import OpenSpielGame


class KuhnPoker(DotsAndBoxes):

    def __init__(self) -> None:
        super().__init__("dots_and_boxes")
        self.game_name = 'dots_and_boxes'
        pass

    def openspiel_action_to_agent(self, action):
        pass

    def openspiel_observation_to_dict(self, current_player_idx, openspiel_obs):
        pass

    def agent_action_to_openspiel(self, action):
        pass

