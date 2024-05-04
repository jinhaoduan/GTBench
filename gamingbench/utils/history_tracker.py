import json
from collections import defaultdict


class Query:
    def __init__(self, messages: list, prompt_type: str, llm_output: list, token_size: int = 0) -> None:

        assert prompt_type in ['move', 'plan', 'vote']
        self.messages = messages
        self.prompt_type = prompt_type
        self.llm_output = llm_output
        self.token_size = token_size
        pass

    def set_token_size(self, num):
        self.token_size = num

    def to_dict(self):
        return {"messages": self.messages,
                "prompt_type": self.prompt_type,
                "llm_output": self.llm_output,
                "token_size": self.token_size}

    def append_llm_output(self, output: str):
        self.llm_output.append(output)

    def __json__(self):
        return self.to_dict()


class Step:
    def __init__(self, agent: str, observation: str = "", move: str = "") -> None:
        self.agent = agent                       # agents name
        self.observation = observation           # observation
        self.move = move
        self.queries = []                          # should be list of str

    def set_observation(self, observation):
        self.observation = observation

    def set_model_name(self, name):
        self.model_name = name

    def set_move(self, move):
        self.move = move

    def add_query(self, query):
        self.queries.append(query)
        pass

    def get_token_size(self):
        self.token_size = sum([q.token_size for q in self.queries])
        return self.token_size

    def to_dict(self):
        return {"agent": self.agent,
                "observation": self.observation,
                "move": self.move,
                "queries": [q.to_dict() for q in self.queries],
                "token_size": self.get_token_size(),
                "model_name": self.model_name
                }

    def __json__(self):
        return self.to_dict()


class GameMatch:

    def __init__(self) -> None:
        self.winner = ""   # the name of the agent
        self.steps = []
        self.status = "Normal"
        self.agents_at_fault = []
        self.agents = set()
        self.winner_score = 0
        self.loser_score = 0
        pass

    def set_winner(self, winner):
        self.winner = winner

    def reset(self):
        '''
        This function will clear all steps and agents
        '''
        self.steps.clear()
        self.winner = ""

    def add_step(self, step):
        self.steps.append(step)
        self.agents.add(step.agent)

    def get_steps_by_agent(self, agent_name):
        steps = [step for step in self.steps if step.agent == agent_name]
        return steps
        pass

    def get_token_size(self):
        self.token_size = sum([s.get_token_size() for s in self.steps])
        return self.token_size

    def get_moves_by_agent(self, agent_name):
        steps = self.get_steps_by_agent(agent_name)
        return [s.move for s in steps]

    def to_dict(self):
        return {"winner": self.winner,
                "agents": list(self.agents),
                "steps": [s.to_dict() for s in self.steps],
                "status": self.status,
                "agents_at_fault": self.agents_at_fault,
                "winner_score": self.winner_score,
                "loser_score": self.loser_score,
                "token_size": self.get_token_size()}

    def __json__(self):
        return self.to_dict()


class HistoryTracker:
    def __init__(self) -> None:
        self.game_config = {}
        self.matches = []
        self.agents = set()
        self.agents_config = []
        self.models_config = []
        pass

    def get_win_rate(self):

        valid_match_num = 0
        agents_win_match = defaultdict(lambda: 0)

        for m in self.matches:
            if m.status == "Normal":
                valid_match_num += 1
                if m.winner != "":
                    agents_win_match[m.winner] += 1
        if valid_match_num != 0:
            for key, val in agents_win_match.items():
                agents_win_match[key] = val/valid_match_num
        else:
            for key, val in agents_win_match.items():
                agents_win_match[key] = 0

        return dict(agents_win_match)

    def get_all_matches(self):
        return self.matches

    def set_game_config(self, config):
        self.game_config = config

    def add_agents_config(self, config):
        self.agents_config.append(config)

    def add_models_config(self, config):
        self.models_config.append(config)

    def add_match(self, match):
        self.matches.append(match)
        for agent in match.agents:
            self.agents.add(agent)

    def get_token_size(self):
        self.token_size = sum([s.get_token_size() for s in self.matches])
        return self.token_size

    def to_dict(self):
        return {
            "game_config": self.game_config,
            "agents_config": self.agents_config,
            "models_config": self.models_config,
            "win_rate": self.get_win_rate(),
            "matches": [m.to_dict() for m in self.matches],
            "token_size": self.get_token_size()}

    def __json__(self):
        return self.to_dict()

    def clear(self):
        '''
        This function will clear all steps and agents
        '''
        self.matches.clear()
        self.agents.clear()

    def save_as_json(self, path):
        '''
        outout a json file containing agents' name and steps
        '''
        data = self.to_dict()
        json_data = json.dumps(data, indent=2)
        # Save JSON to a file
        with open(path, 'w') as json_file:
            json_file.write(json_data)
        pass


# import os
# import logging
# import random
# import numpy as np
# import yaml
# import concurrent
# import json

# from concurrent.futures import ThreadPoolExecutor
# from box import Box
# from gamingbench import agents
# from gamingbench import games
# from gamingbench import models

# def get_game_config_path(game):
#     config_root = './gamingbench/configs/game_configs'
#     if game == 'tictactoe':
#         return os.path.join(config_root, 'tictactoe.yaml')
#     elif game == 'connect4':
#         return os.path.join(config_root, 'connect4.yaml')
#     elif game == 'backgammon':
#         return os.path.join(config_root, 'backgammon.yaml')
#     elif game == 'breakthrough':
#         return os.path.join(config_root, 'breakthrough.yaml')
#     elif game == 'first_sealed_auction':
#         return os.path.join(config_root, 'first_sealed_auction.yaml')
#     elif game == 'gin_rummy':
#         return os.path.join(config_root, 'gin_rummy.yaml')
#     elif game == 'liars_dice':
#         return os.path.join(config_root, 'liars_dice.yaml')
#     elif game == 'negotiation':
#         return os.path.join(config_root, 'negotiation.yaml')
#     elif game == 'nim':
#         return os.path.join(config_root, 'nim.yaml')
#     elif game == 'pig':
#         return os.path.join(config_root, 'pig.yaml')
#     elif game == 'kuhn_poker':
#         return os.path.join(config_root, 'kuhn_poker.yaml')
#     elif game == 'crazy_eights':
#         return os.path.join(config_root, 'crazy_eights.yaml')
#     else:
#         raise NotImplementedError

# def load_game(game_config_path):
#     game_config = Box.from_yaml(filename=game_config_path, Loader=yaml.FullLoader)
#     return getattr(games, game_config.game_name)()

# def load_config(config_path):
#     config = Box.from_yaml(filename=config_path, Loader=yaml.FullLoader)
#     return config

# def load_agent(agent_config_path, **kwargs):
#     agent_config = Box.from_yaml(filename=agent_config_path, Loader=yaml.FullLoader)
#     return getattr(agents, agent_config.agent_name)(agent_config, **kwargs)

# def load_model(model_config_path):
#     model_config = Box.from_yaml(filename=model_config_path, Loader=yaml.FullLoader)
#     return getattr(models, model_config.model_type)(model_config)

# def set_seed(seed):
#     np.random.seed(seed)
#     random.seed(seed)

# def get_logger(logger_path, debug=False, rm_existed=False):
#     logger = logging.getLogger(__name__)
#     logger.setLevel(logging.INFO)

#     if rm_existed and os.path.exists(logger_path):
#         os.remove(logger_path)

#     fh = logging.FileHandler(logger_path)
#     fh.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
#     logger.addHandler(fh)

#     return logger

# def parallel_func(worker, arg_list, num_workers=20):
#     results = []
#     futures = []
#     with ThreadPoolExecutor(max_workers=num_workers) as executor:
#         for idx, arg in enumerate(arg_list):
#             futures.append(executor.submit(worker, arg))

#         for future in concurrent.futures.as_completed(futures):
#             results.append(future.result())
#     return results

# def load_jsonl(path):
#     result = []
#     with open(path, 'r') as f:
#         for l in f.readlines():
#             r = json.loads(l)
#             result.append(r)
#     return result

# def save_jsonl(results, path):
#     with open(path, 'w') as f:
#         for r in results:
#             f.writelines(json.dumps(r) + '\n')

# class LLMBenchLogger:
#     _instance = None

#     def __new__(cls, logger_path, debug=False, rm_existed=False):
#         if cls._instance is None:
#             cls._instance = super(LLMBenchLogger, cls).__new__(cls)
#             cls._instance.logger = cls._configure_logger(logger_path, debug, rm_existed)
#         return cls._instance.logger

#     @staticmethod
#     def _configure_logger(logger_path, debug, rm_existed):
#         logger = logging.getLogger(__name__)
#         logger.setLevel(logging.INFO)

#         if rm_existed and os.path.exists(logger_path):
#             os.remove(logger_path)

#         fh = logging.FileHandler(logger_path)
#         fh.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
#         logger.addHandler(fh)

#         return logger
