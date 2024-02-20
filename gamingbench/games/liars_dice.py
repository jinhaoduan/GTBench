import numpy as np
from typing import List
from gamingbench.utils.history_tracker import GameMatch, Step
from gamingbench.utils import utils
from gamingbench.games.openspiel_adapter import OpenSpielGame

# Note: the action is comprised of two parts, the quantity and face value, written as q-v


class LiarsDice(OpenSpielGame):
    def __init__(self) -> None:
        super().__init__("liars_dice")
        pass

    def extract_quantity_and_face_value(self, text):
        numbers = text.split('-')
        quantity = int(numbers[0])
        face_value = int(numbers[1])
        return quantity, face_value

    def cvt_to_agent_action(self, a):
        if a == 'Liar':
            a = '<Liar>'
        else:
            x, y = self.extract_quantity_and_face_value(a)
            a = f'<{x} dices, {y} value>'
        return a

    def openspiel_action_to_agent(self, action):
        new_actions = []
        for a in action:
            new_actions.append(self.cvt_to_agent_action(a))
        return new_actions

    def openspiel_observation_to_dict(self, current_player_idx, openspiel_obs):
        opponent_idx = 1 if current_player_idx == 0 else 0
        obs = openspiel_obs.split(' ')

        res = {
            'opponent_moves': self.quick_action_memory_for_llm.get(opponent_idx, []),
            'self_moves': self.quick_action_memory_for_llm.get(current_player_idx, []),
            'self_dice_face_value': obs[current_player_idx],
            'opponent_dice_face_value': obs[0 if current_player_idx == 1 else 1],
            'last_move': self.cvt_to_agent_action(obs[-1]) if '-' in obs[-1] else None
        }
        return res

    def agent_action_to_openspiel(self, action):
        try:
            action = action.replace('<', '')
            action = action.replace('>', '')
            if action.lower() == 'liar':
                return 12
            else:
                q = int(action.strip().split(' ')[0])
                v = int(action.strip().split(' ')[-2])
                # q, v = self.extract_quantity_and_face_value(action)
                val = (q-1)*6+(v-1)
                return val
        except Exception:
            self.logger.info("Unsuccessful interpreting LLM move")
            self.logger.info(action)
            return None

