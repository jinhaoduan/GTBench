
from typing import List
from gamingbench.utils.history_tracker import GameMatch, Step
from gamingbench.utils import utils
from gamingbench.games.openspiel_adapter import OpenSpielGame
import re
import pyspiel


class Pig(OpenSpielGame):
    def __init__(self) -> None:
        super().__init__("pig")
        self.game = pyspiel.load_game(
            "pig", {'winscore': 20})
        self.env = self.game.new_initial_state()
        pass

    def openspiel_action_to_agent(self, action):
        return [f'<{a}>' for a in action]
        pass

    def openspiel_observation_to_dict(self, current_player_idx, openspiel_obs):
        opponent_idx = 1 if current_player_idx == 0 else 0

        pattern = r'\b\d+\b'

        # Use re.findall to extract all numbers in the string
        numbers = re.findall(pattern, openspiel_obs)
        # Extract the first three numbers
        num1, num2, num3 = map(int, numbers[:3])

        res = {
            # 'opponent_moves': self.quick_action_memory_for_llm.get(opponent_idx, []),
            # 'self_moves': self.quick_action_memory_for_llm.get(current_player_idx, []),
            'self_current_score': num2 if current_player_idx == 1 else num1,
            'opponent_current_score': num2 if current_player_idx == 0 else num1,
            'turn_total_score': num3,

        }
        return res
        pass

    def agent_action_to_openspiel(self, action):
        try:
            action = action.lower()
            stop_index = float("inf")
            roll_index = float("inf")

            if action.__contains__("stop"):
                stop_index = action.index("stop")
                # return 1
            if action.__contains__("roll"):
                roll_index = action.index("roll")
                # return 0
            if stop_index < roll_index:
                return 1
            elif stop_index > roll_index:
                return 0
            else:
                raise Exception
        except Exception:
            self.logger.info("Unsuccessful interpreting LLM move")
            self.logger.info(action)
            return None
