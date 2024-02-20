import numpy as np
from typing import List
from gamingbench.utils.history_tracker import GameMatch, Step
from gamingbench.utils import utils
from gamingbench.games.openspiel_adapter import OpenSpielGame
import re


class Nim(OpenSpielGame):
    def __init__(self) -> None:
        super().__init__("nim")
        pass

    def openspiel_action_to_agent(self, action):
        actions = [f'<{a[:-1]}>' for a in action] # a[:-1] for pile:4, take:2; -> pile:4, take:2
        return actions
        pass

    def openspiel_observation_to_dict(self, current_player_idx, openspiel_obs):
        opponent_idx = 1 if current_player_idx == 0 else 0
        numbers = openspiel_obs.split(' ')
        numbers = numbers[1:]
        res = {
            'opponent_moves': self.quick_action_memory_for_llm.get(opponent_idx, []),
            'self_moves': self.quick_action_memory_for_llm.get(current_player_idx, []),
            'piles': numbers
        }
        return res
        pass

    def agent_action_to_openspiel(self, action):
        try:
            pattern = r'\d+'
            # Use re.findall to extract all numbers in the string
            numbers = re.findall(pattern, action)
            numbers = [int(n) for n in numbers]
            result = (numbers[-1] - 1) * 4 + numbers[0]
            return result-1
        except Exception as e:
            self.logger.error(e)
            self.logger.info("Unsuccessful interpreting LLM move")
            self.logger.info(action)
            return None
