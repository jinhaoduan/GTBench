import copy
from gamingbench.games.openspiel_adapter import OpenSpielGame
import re

class DotsAndBoxes(OpenSpielGame):
    def __init__(self) -> None:
        super().__init__("dots_and_boxes")
        self.game_name = 'dots_and_boxes'

    def openspiel_action_to_agent(self, action, num_rows, num_cols):
        # Convert action IDs into the coordinate format
        actions = []
        maxh = (num_rows + 1) * num_cols
        if action < maxh:
            # Horizontal
            row = action // num_cols
            col = action % num_cols
            start = f'{chr(65 + col)}{row + 1}'
            end = f'{chr(66 + col)}{row + 1}'
        else:
            # Vertical
            action -= maxh
            row = action // (num_cols + 1)
            col = action % (num_cols + 1)
            start = f'{chr(65 + col)}{row + 1}'
            end = f'{chr(65 + col)}{row + 2}'
        
        actions.append(f'<{start}−{end}>')
        return actions

    def openspiel_observation_to_dict(self, current_player_idx, openspiel_obs):
        opponent_idx = 1 if current_player_idx == 0 else 0
        res = {
            'opponent_moves': copy.deepcopy(self.quick_action_memory_for_llm.get(opponent_idx, [])),
            'self_moves': copy.deepcopy(self.quick_action_memory_for_llm.get(current_player_idx, [])),
        }
        return res

    def agent_action_to_openspiel(self, action, num_rows, num_cols):
        try:
            regex = r"([A-Z]+)(\d+)"
            matches = re.findall(regex, action)
            if not matches or len(matches) < 2:
                raise ValueError("Invalid action format")
            
            col_start = ord(matches[0][0][0]) - 65
            row_start = int(matches[0][1]) - 1
            col_end = ord(matches[1][0][0]) - 65
            #row_end = int(matches[1][1]) - 1

            if col_start == col_end:
                # Vertical
                action_id = (num_rows + 1) * num_cols + row_start * (num_cols + 1) + col_start
            else:
                # Horizontal
                action_id = row_start * num_cols + col_start

            return action_id
        except Exception as e:
            self.logger.info("Unsuccessful interpreting LLM move")
            self.logger.info(action)
            return None
