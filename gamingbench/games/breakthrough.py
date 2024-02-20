
import random
import copy
import pyspiel
import numpy as np
from gamingbench.utils import utils
from gamingbench.utils.history_tracker import GameMatch, Step
from gamingbench.games.openspiel_adapter import OpenSpielGame


class Breakthrough(OpenSpielGame):
    def __init__(self) -> None:
        super().__init__("breakthrough")
        self.game = pyspiel.load_game(
            "breakthrough", {'columns': 3})
        self.env = self.game.new_initial_state()
        pass

    def openspiel_action_to_agent(self, action):
        actions = [f'<{a[:2]}->{a[2:]}>' for a in action]
        return actions
        pass

    def openspiel_observation_to_dict(self, current_player_idx, openspiel_obs):
        opponent_idx = 1 if current_player_idx == 0 else 0
        board_preview = str(str(self.env).split('\n')[:-2])
        res = {
            'opponent_moves': copy.deepcopy(self.quick_action_memory_for_llm.get(opponent_idx, [])),
            'self_moves': copy.deepcopy(self.quick_action_memory_for_llm.get(current_player_idx, [])),
            'board': board_preview
        }
        return res
        pass

    def inverse_col_label(self, label):
        col = ord(label) - ord('a')
        return col

    def inverse_row_label(self, label):
        row = 8 - 1 - (ord(label) - ord('1'))
        return row

    def inverse(self, action):
        c1, c2 = action[0], action[2]
        r1, r2 = action[1], action[3]
        return self.inverse_col_label(c1), self.inverse_row_label(r1), self.inverse_col_label(c2), self.inverse_row_label(r2)

    def rank_action_mixed_base(self, digits):
        bases = [8, 3, 6, 2]
        action = 0
        one_plus_max = 1
        for i in range(len(digits) - 1, -1, -1):
            action += digits[i] * one_plus_max
            one_plus_max *= bases[i]
        return action

    def agent_action_to_openspiel(self, action):
        try:
            action = action.replace('-', '')
            action = action.replace('>', '')
            action = action.replace('<', '')
            c1, r1, c2, r2 = self.inverse(action)
            kDirRowOffsets = [1, 1, 1, -1, -1, -1]
            kDirColOffsets = [-1, 0, 1, -1, 0, 1]

            delta_r = r2 - r1
            delta_c = c2 - c1
            dir = -1
            for d, (offset_r, offset_c) in enumerate(zip(kDirRowOffsets, kDirColOffsets)):
                if delta_r == offset_r and delta_c == offset_c:
                    dir = d
                    break
            real_values = [r1, c1, dir, 1 if action.__contains__('*') else 0]
            game_action = self.rank_action_mixed_base(real_values)
            legal_actions = self.env.legal_actions(self.env.current_player())
            if game_action in legal_actions:
                return game_action
            else:
                if game_action % 2 == 0:
                    game_action += 1
                else:
                    game_action -= 1
                if game_action in legal_actions:
                    return game_action
            raise Exception
        except Exception as e:
            self.logger.info("Unsuccessful interpreting LLM move")
            self.logger.info(action)
            self.logger.exception(e)
            return None

        pass
