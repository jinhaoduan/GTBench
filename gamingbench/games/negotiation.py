import numpy as np
from typing import List
from gamingbench.utils.history_tracker import GameMatch, Step
from gamingbench.utils import utils
from gamingbench.games.openspiel_adapter import OpenSpielGame
import re


class Negotiation(OpenSpielGame):
    def __init__(self) -> None:
        super().__init__("negotiation")
        pass

    def openspiel_action_to_agent(self, action):
        turn_type = self.get_turn_type()
        if turn_type == 'Proposal':
            agent_actions = []
            # TODO: default item pool is [5, 5, 5]
            for a in range(6):
                for b in range(6):
                    for c in range(6):
                        agent_actions.append(f'<Proposal: [{a}, {b}, {c}]>')
            agent_actions.append(f'<Agree>')

        elif turn_type == 'Utterance':
            agent_actions = []
            # TODO: default item pool is [5, 5, 5]
            for a in range(5):
                for b in range(5):
                    for c in range(5):
                        agent_actions.append(f'<Utterance: [{a}, {b}, {c}]>')

        else:
            raise ValueError()

        return agent_actions

    def openspiel_observation_to_dict(self, current_player_idx, openspiel_obs):
        opponent_idx = 1 if current_player_idx == 0 else 0
        turn_type = self.get_turn_type()

        agent_util_vec_match = re.search(r'Agent 0 util vec: (\d+ \d+ \d+)', openspiel_obs) if current_player_idx == 0 else re.search(
            r'Agent 1 util vec: (\d+ \d+ \d+)', openspiel_obs)
        agent_util_vec = agent_util_vec_match.group(1)
        agent_util_vec = agent_util_vec.split(' ')
        agent_util_vec = [int(v) for v in agent_util_vec]

        item_pool_match = re.search(r'Item pool: (\d+ \d+ \d+)', openspiel_obs)
        item_pool = item_pool_match.group(1)
        item_pool = item_pool.split(' ')
        item_pool = [int(v) for v in item_pool]

        most_recent_proposal_match = re.search(
            r'Most recent proposal: (.+)', self.env.observation_string())
        most_recent_utterance_match = re.search(
            r'Most recent utterance: (.+)', self.env.observation_string())

        res = {
            'opponent_moves': self.quick_action_memory_for_llm.get(opponent_idx, []),
            'self_moves': self.quick_action_memory_for_llm.get(current_player_idx, []),
            'turn_type': turn_type,
            'self_value_vector': agent_util_vec,
            'item_pool': item_pool,
            'most_recent_proposal': most_recent_proposal_match.group(1)[1:-1].replace(',', '').split(' ') if most_recent_proposal_match is not None else None,
            'most_recent_utterance': most_recent_utterance_match.group(1)[1:-1].replace(',', '').split(' ') if most_recent_utterance_match is not None else None
        }
        return res
        pass

    def get_turn_type(self):
        turn_type_match = re.search(r'Turn Type: (\w+)', str(self.env))
        turn_type = turn_type_match.group(1)
        return turn_type

    def encode_integer(self, container, num_digit_values):
        encoded_value = 0
        for digit in container:
            encoded_value = encoded_value * num_digit_values + digit
        return encoded_value

    def agent_action_to_openspiel(self, action):
        try:
            numbers_match = re.search(r'\[(\d+), (\d+), (\d+)\]', action)
            print(f"debug : numbers_match:{numbers_match},action:{action}")
            if self.get_turn_type() == 'Proposal':
                if action.lower().__contains__('agree'):
                    player_idx = self.env.current_player()
                    return self.env.legal_actions(player_idx)[-1]
                else:

                    first_number = int(numbers_match.group(1))
                    second_number = int(numbers_match.group(2))
                    third_number = int(numbers_match.group(3))
                    action = [min(5, first_number), min(
                        5, second_number), min(5, third_number)]
                    return self.encode_integer(action, 6)
            else:
                # kDefaultNumItems=3
                # kMaxQuantity=5
                # kDefaultNumSymbols=5
                first_number = int(numbers_match.group(1))
                second_number = int(numbers_match.group(2))
                third_number = int(numbers_match.group(3))
                action = [min(4, first_number), min(
                    4, second_number), min(4, third_number)]
                return int(pow(6, 3)) + 1 + self.encode_integer(action, 5)
        except Exception as e:
            self.logger.error(e)
            self.logger.info("Unsuccessful interpreting LLM move")
            self.logger.info(action)
            return None
