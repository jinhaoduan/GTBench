
import copy
from gamingbench.games.openspiel_adapter import OpenSpielGame
import re


class ConnectFour(OpenSpielGame):
    def __init__(self) -> None:
        super().__init__("connect_four")
        self.game_name = 'connect4'
        pass

    def openspiel_action_to_agent(self, action):

        actions = [f'<C{int(a[1]) + 1}>' for a in action]
        return actions
        pass

    def openspiel_observation_to_dict(self, current_player_idx, openspiel_obs):
        opponent_idx = 1 if current_player_idx == 0 else 0
        res = {
            'opponent_moves': copy.deepcopy(self.quick_action_memory_for_llm.get(opponent_idx, [])),
            'self_moves': copy.deepcopy(self.quick_action_memory_for_llm.get(current_player_idx, [])),
        }
        return res
        pass

    def agent_action_to_openspiel(self, action):
        try:
            regex = r"\s*(\d+)\s*"
            numbers_match = re.findall(
                regex, action)
            column = int(numbers_match[0])-1
            return min(column, 6)
        except Exception as e:

            self.logger.info("Unsuccessful interpreting LLM move")
            self.logger.info(action)
            return None
        pass
