import numpy as np
import pyspiel
import open_spiel

from typing import List
from pettingzoo.classic import tictactoe_v3
from gamingbench.utils.history_tracker import GameMatch, Step
from gamingbench.utils import utils

from open_spiel.python import games  # import prisoners_dilemma

import copy

from time import sleep


class OpenSpielGame:
    def __init__(self, game_name) -> None:
        self.game_name = game_name

        if game_name == "crazy_eights": 
            game_name = "crazy_eights(players=2)"


        if game_name == "dots_and_boxes": 
            game_name = "dots_and_boxes"
        

        self.game = pyspiel.load_game(game_name)
        self.env = self.game.new_initial_state()
        self.logger = utils.LLMBenchLogger(None)
        self.status = "Normal"
        self.quick_action_memory_for_llm = {}
        pass

    def reset(self):
        self.game = pyspiel.load_game(self.game_name)
        self.env = self.game.new_initial_state()
        self.logger = utils.LLMBenchLogger(None)
        self.status = "Normal"
        self.quick_action_memory_for_llm = {}

    def print_game_info(self):
        self.logger.info(self.env.agents)
        self.logger.info(self.env.agent_selection)
        self.logger.info(self.env.action_spaces)

    def play(self, agent_list, model_list, tracker):
        self.status = "Normal"
        _match = GameMatch()

        num_step = 0
        while not self.env.is_terminal():
            if self.env.is_chance_node():
                # Chance node: sample an outcome
                outcomes = self.env.chance_outcomes()
                num_actions = len(outcomes)
                print("Chance node, got " + str(num_actions) + " outcomes")
                action_list, prob_list = zip(*outcomes)
                action = np.random.choice(action_list, p=prob_list)
                print("Sampled outcome: ",
                      self.env.action_to_string(self.env.current_player(), action))
                self.env.apply_action(action)

            elif self.env.is_simultaneous_node():
                # TODO: only support prisoners dilemma
                chosen_actions = []
                abnormal = False
                for player_idx in range(self.env.num_players()):
                    observation_dict = self.openspiel_observation_to_dict(
                        player_idx, str(self.env))
                    _step = Step(agent_list[player_idx].agent_name)
                    _step.set_model_name(model_list[player_idx].nick_name)
                    _step.set_observation(observation_dict)
                    legal_actions = self.env.legal_actions(player_idx)
                    observation_dict['openspiel_legal_actions'] = legal_actions
                    valid_action = [self.env.action_to_string(
                        a) for a in legal_actions]
                    valid_action = self.openspiel_action_to_agent(valid_action)
                    observation_dict['legal_moves'] = valid_action
                    observation_dict['env_name'] = self.game_name
                    self.logger.info(
                        f"openspiel_game_legal_action:{legal_actions}")
                    self.logger.info(f"validMove:{valid_action}")
                    action, query_list = agent_list[player_idx].step(
                        observation_dict)
                    self.logger.info(
                        f"player: {player_idx} agent:{agent_list[player_idx].agent_name}, action: {action}")
                    act = self.quick_action_memory_for_llm.get(
                        player_idx, [])

                    act.append(action)
                    self.quick_action_memory_for_llm[player_idx] = act

                    for q in query_list:
                        _step.add_query(q)

                    _step.set_move(action)
                    _match.add_step(_step)
                    game_action = self.agent_action_to_openspiel(action)
                    self.logger.info(f"game_action:{game_action}")

                    num_step += 1

                    if not self.is_valid_move(game_action, legal_actions):
                        game_action = None
                        agent_name = agent_list[player_idx].agent_name
                        self.logger.info(
                            f"agent {agent_name} made a invalid step")
                        _match.agents_at_fault.append(agent_name)
                        _match.status = "Abnormal"
                        self.status = "Abnormal"
                        abnormal = True
                        break
                    chosen_actions.append(game_action)
                if abnormal:
                    break
                self.env.apply_actions(chosen_actions)

                # inform other opponents
                for action_idx, action in enumerate(chosen_actions):
                    for player_idx, agent in enumerate(agent_list):
                        if player_idx != action_idx:
                            agent.inform_action(
                                self.env, self.env.current_player, action)

            else:

                # print("num of players" + str(self.env.num_players()))
                player_idx = self.env.current_player()

                # continuePlaying = True 

                # while continuePlaying: 
                # init step

                # print(f"player_idx {player_idx}")
                # print(f"agent_list {agent_list}")
                _step = Step(agent_list[player_idx].agent_name)
                _step.set_model_name(model_list[player_idx].nick_name)

                try:
                    observations = self.env.observation_string()
                except Exception as e:
                    observations = str(self.env)

                observation_dict = self.openspiel_observation_to_dict(
                    self.env.current_player(), observations)
                observation_dict['state'] = self.env

                legal_actions = self.env.legal_actions(player_idx)
                observation_dict['openspiel_legal_actions'] = legal_actions
                valid_action = [self.env.action_to_string(
                    a) for a in legal_actions]
                valid_action = self.openspiel_action_to_agent(valid_action)

                observation_dict['legal_moves'] = valid_action
                observation_dict['env_name'] = self.game_name
                if len(legal_actions) != 1:
                    action, query_list = agent_list[player_idx].step(
                        observation_dict)
                    if self.game_name == 'dots_and_boxes':
                        action = ''.join(('<', action[1], action[2], '-', action[3], action[4], '>'))
                else:
                    action, query_list = valid_action[0], []

                #action = ''.join(('<',action[0],'>'))

                act = self.quick_action_memory_for_llm.get(
                    player_idx, [])

                act.append(action)
                self.quick_action_memory_for_llm[player_idx] = act

                observation_dict.pop('state')
                _step.set_observation(copy.deepcopy(observation_dict))
                # _step.set_observation(observation_dict)
                self.logger.info(
                    f"openspiel_game_legal_action:{legal_actions}")

                self.logger.info(f"validMove:{valid_action}")

                for q in query_list:
                    _step.add_query(q)

                self.logger.info(
                    f"player: {player_idx} agent:{agent_list[player_idx].agent_name}, action: {action}")

                _step.set_move(action)
                _match.add_step(_step)
                game_action = self.agent_action_to_openspiel(action)
                self.logger.info(f"game_action:{game_action}")
                num_step += 1
                if not self.is_valid_move(game_action, legal_actions):
                    game_action = None
                    agent_name = agent_list[player_idx].agent_name
                    self.logger.info(f"agent {agent_name} made a invalid step")
                    _match.agents_at_fault.append(agent_name)
                    _match.status = "Abnormal"
                    self.status = "Abnormal"
                    break

                self.env.apply_action(game_action)
                # inform other opponents
                for idx, agent in enumerate(agent_list):
                    if player_idx != idx:
                        agent.inform_action(self.env, player_idx, game_action)

        results = self.env.returns()
        if results[0] > results[1]:
            # player 0 wins
            winner_name = agent_list[0].agent_name + \
                "_"+agent_list[0].model.nick_name
            _match.loser_score = results[1]
            _match.winner_score = results[0]
        elif results[1] > results[0]:
            # player 1 wins
            winner_name = agent_list[1].agent_name + \
                "_"+agent_list[1].model.nick_name
            _match.loser_score = results[0]
            _match.winner_score = results[1]
        else:
            # draw
            winner_name = ""

        _match.set_winner(winner_name)
        tracker.add_match(_match)
        if _match.winner != "":
            self.logger.info(f"The winner is {_match.winner}")
        else:
            self.logger.info("There are no winner in this game.")

    def openspiel_observation_to_dict(self, current_player_idx, openspiel_obs):
        return {}

    def openspiel_action_to_agent(self, action):
        return action

    def agent_action_to_openspiel(self, action):
        return action

    def is_match_normal(self) -> bool:
        return self.status == 'Normal'

    def is_valid_move(self, move, valid_moves):
        return move in valid_moves and move != None
