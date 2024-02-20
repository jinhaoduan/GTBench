
import numpy as np

from gamingbench.agents.base_agent import BaseAgent

class TitForTatAgent(BaseAgent):

    def __init__(self, config, **kwargs):
        super(TitForTatAgent, self).__init__(config)

    def step(self, observations):
        assert observations, print('Tit-for-Tat Agent only works for Iterated Prisoner\'s Dilemma')
        opponent_moves = observations['opponent_moves']
        if len(opponent_moves) > 0:
            move = '<Silent>' if opponent_moves[-1] == 'C' else '<Testify>'
        else:
            move = '<Silent>'
        return move, []