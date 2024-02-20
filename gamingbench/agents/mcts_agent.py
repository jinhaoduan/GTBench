import pyspiel
import numpy as np

from open_spiel.python.algorithms import mcts
from gamingbench.agents.base_agent import BaseAgent


class MCTSAgent(BaseAgent):

    def __init__(self, config, **kwargs):
        super(MCTSAgent, self).__init__(config)
        self.rollout_count = config.rollout_count
        self.uct_c = config.uct_c
        self.max_simulations = config.max_simulations
        self.solve = config.solve
        self.verbose = config.verbose
        rng = np.random.RandomState()
        evaluator = mcts.RandomRolloutEvaluator(self.rollout_count, rng)
        self.bot = mcts.MCTSBot(
            kwargs['game'],
            self.uct_c,
            self.max_simulations,
            evaluator,
            random_state=rng,
            solve=self.solve,
            verbose=self.verbose)

    def step(self, observations):
        agent_action_list = observations['legal_moves']
        openspiel_action_list = observations['openspiel_legal_actions']
        state = observations['state']
        action = self.bot.step(state)

        print(agent_action_list)
        print(openspiel_action_list)
        print(action)
        return agent_action_list[openspiel_action_list.index(action)], []

    def inform_action(self, state, player_idx, action):
        self.bot.inform_action(state, player_idx, action)

