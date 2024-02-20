import numpy as np
from typing import List
from gamingbench.utils.history_tracker import GameMatch, Step
from gamingbench.utils import utils
from gamingbench.games.openspiel_adapter import OpenSpielGame


class FirstSealedAuction(OpenSpielGame):
    def __init__(self) -> None:
        super().__init__("first_sealed_auction")
        pass

    def openspiel_action_to_agent(self, action):
        agent_action_list = [a.split(' ')[-1] for a in action]
        agent_action_list = [f'<{a}>' for a in agent_action_list]
        return agent_action_list

    def openspiel_observation_to_dict(self, current_player_idx, openspiel_obs):
        return {
            'valuation': float(self.env.observation_string())
        }

    def agent_action_to_openspiel(self, action):
        try:
            bid = int(action[1:-1])
            legal_actions = self.env.legal_actions(self.env.current_player())
            legal_actions = [int(l) for l in legal_actions]
            if bid in legal_actions:
                return bid
            distance = float('inf')
            ans = bid
            for i in legal_actions:
                d = abs(i-bid)
                if d <= distance:
                    distance = d
                    ans = i
            return ans
        except Exception as e:
            self.logger.info("Unsuccessful interpreting LLM move")
            self.logger.info(action)
            return None
