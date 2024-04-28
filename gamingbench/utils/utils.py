
import os
import logging
import random
import numpy as np
import yaml
import concurrent
import json

from concurrent.futures import ThreadPoolExecutor
from box import Box
from gamingbench import agents
from gamingbench import games
from gamingbench import models


def get_game_config_path(game):
    config_root = './gamingbench/configs/game_configs'
    if game == 'tictactoe':
        return os.path.join(config_root, 'tictactoe.yaml')
    elif game == 'connect4':
        return os.path.join(config_root, 'connect4.yaml')
    elif game == 'backgammon':
        return os.path.join(config_root, 'backgammon.yaml')
    elif game == 'breakthrough':
        return os.path.join(config_root, 'breakthrough.yaml')
    elif game == 'first_sealed_auction':
        return os.path.join(config_root, 'first_sealed_auction.yaml')
    elif game == 'gin_rummy':
        return os.path.join(config_root, 'gin_rummy.yaml')
    elif game == 'liars_dice':
        return os.path.join(config_root, 'liars_dice.yaml')
    elif game == 'negotiation':
        return os.path.join(config_root, 'negotiation.yaml')
    elif game == 'nim':
        return os.path.join(config_root, 'nim.yaml')
    elif game == 'pig':
        return os.path.join(config_root, 'pig.yaml')
    elif game == 'kuhn_poker':
        return os.path.join(config_root, 'kuhn_poker.yaml')
    elif game == 'crazy_eights':
        return os.path.join(config_root, 'crazy_eights.yaml')
    elif game == 'dots_and_boxes':
        return os.path.join*(config_root, 'dots_and_boxes.yaml')
    else:
        raise NotImplementedError


def load_game(game_config_path):
    game_config = Box.from_yaml(
        filename=game_config_path, Loader=yaml.FullLoader)
    return getattr(games, game_config.game_name)()


def load_config(config_path):
    config = Box.from_yaml(
        filename=config_path, Loader=yaml.FullLoader)

    return config


def load_agent(agent_config_path, **kwargs):
    agent_config = Box.from_yaml(
        filename=agent_config_path, Loader=yaml.FullLoader)
    return getattr(agents, agent_config.agent_name)(agent_config, **kwargs)


def load_model(model_config_path):
    model_config = Box.from_yaml(
        filename=model_config_path, Loader=yaml.FullLoader)
    return getattr(models, model_config.model_type)(model_config)


def set_seed(seed):
    np.random.seed(seed)
    random.seed(seed)


def get_logger(logger_path, debug=False, rm_existed=False):
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)
    ch = logging.StreamHandler()
    ch.setFormatter(logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
    logger.addHandler(ch)

    if rm_existed and os.path.exists(logger_path):
        os.remove(logger_path)

    fh = logging.FileHandler(logger_path)
    fh.setFormatter(logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
    logger.addHandler(fh)

    return logger


def parallel_func(worker, arg_list, num_workers=20):
    results = []
    futures = []
    with ThreadPoolExecutor(max_workers=num_workers) as executor:
        for idx, arg in enumerate(arg_list):
            futures.append(executor.submit(worker, arg))

        for future in concurrent.futures.as_completed(futures):
            results.append(future.result())
    return results


def load_jsonl(path):
    result = []
    with open(path, 'r') as f:
        for l in f.readlines():
            r = json.loads(l)
            result.append(r)
    return result


def save_jsonl(results, path):
    with open(path, 'w') as f:
        for r in results:
            f.writelines(json.dumps(r) + '\n')


class LLMBenchLogger:
    _instance = None

    def __new__(cls, logger_path, debug=False, rm_existed=False):
        if cls._instance is None:
            cls._instance = super(LLMBenchLogger, cls).__new__(cls)
            cls._instance.logger = cls._configure_logger(
                logger_path, debug, rm_existed)
        return cls._instance.logger

    @staticmethod
    def _configure_logger(logger_path, debug, rm_existed):
        logger = logging.getLogger(__name__)
        logger.setLevel(logging.INFO)
        ch = logging.StreamHandler()
        ch.setFormatter(logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
        logger.addHandler(ch)

        if rm_existed and os.path.exists(logger_path):
            os.remove(logger_path)

        fh = logging.FileHandler(logger_path)
        fh.setFormatter(logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
        logger.addHandler(fh)

        return logger
