
import numpy as np

from gamingbench.agents.base_agent import BaseAgent

class RandomAgent(BaseAgent):

    def __init__(self, config, **kwargs):
        super(RandomAgent, self).__init__(config)

    def step(self, observations):
        agent_action_list = observations['legal_moves']
        return np.random.choice(agent_action_list), []