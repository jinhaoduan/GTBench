import copy
import os.path
import argparse
import pathlib
import threading
from gamingbench.utils import utils
from gamingbench.environments.base_env import BaseGameEnv
import json

games = ['tictactoe', 'connect4', 'texasholdem', 'neuron_poker', 'backgammon', 'breakthrough',
         'first_sealed_auction', 'gin_rummy', 'liars_dice', 'negotiation', 'nim', 'pig', 'kuhn_poker',
         'prisoners_dilemma', 'dots_and_boxes', 'crazy_eights']


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--num-matches', type=int,
                        default=100, help='The number gaming matches')
    parser.add_argument('--exp-root', type=str, default='../experiments')
    parser.add_argument('--seed', type=int, default=0)
    # gaming parameters
    parser.add_argument('--game-names', type=str, nargs='+',
                        default=['tictactoe'], choices=games)
    parser.add_argument('--game-config-root', type=str, default='gamingbench/configs/game_configs',
                        help='Path of gaming environment configurations')
    # agent parameters
    parser.add_argument('--agent-configs', type=str, nargs='+',
                        default=[
                        ],
                        help='List of paths of agent configurations')

    parser.add_argument('--model-configs', type=str, nargs='+',
                        default=[
                        ],
                        help='List of paths of model configurations')

    parser.add_argument('--output-folder', default='./')

    parser.add_argument('--api-keys', default='', nargs='+')

    parser.add_argument('--exchange-first-player',
                        default=False, action='store_true')
    parser.add_argument('--num-workers', default=1, type=int)
    parser.add_argument('--threshold-matches', default=50, type=int)
    args = parser.parse_args()

    return args


def run_game(game_name):
    log_root = os.path.join(args.exp_root, game_name)
    pathlib.Path(log_root).mkdir(parents=True, exist_ok=True)
    agent_names = [a.split('/')[-1].split('.')[0] for a in args.agent_configs]
    model_names = [m.split('/')[-1].split('.')[0] for m in args.model_configs]

    run_name = f'{agent_names[0]}_{model_names[0]}_{agent_names[1]}_{model_names[1]}'

    log_path = os.path.join(log_root, run_name + '.log')
    logger = utils.LLMBenchLogger(log_path)
    result_path = os.path.join(log_root, run_name + '.jsonl')

    if not os.path.exists(result_path):
        file = open(result_path, 'w')
        file.close()

    # initialize env and game
    game_env = BaseGameEnv()
    print(os.path.join(
        args.game_config_root, f'{game_name}.yaml'))
    game = utils.load_game(os.path.join(
        args.game_config_root, f'{game_name}.yaml'))
    game_env.save_game_config(utils.load_config(
        os.path.join(args.game_config_root, f'{game_name}.yaml')))

    # initialize agents
    agents = [utils.load_agent(config_path, game=game.game)
              for config_path in args.agent_configs]
    models = [utils.load_model(config_path)
              for config_path in args.model_configs]

    for a, m in zip(agents, models):
        a.set_model(m)

    # exchange first player to mitigate first-player advantage
    reversed_agent_configs = copy.deepcopy(args.agent_configs)
    reversed_agent_configs.reverse()
    reversed_agents = [utils.load_agent(
        config_path, game=game.game) for config_path in reversed_agent_configs]
    reversed_model_configs = copy.deepcopy(args.model_configs)
    reversed_model_configs.reverse()
    reversed_models = [utils.load_model(config_path)
                       for config_path in reversed_model_configs]

    for a, m in zip(reversed_agents, reversed_models):
        a.set_model(m)

    for config_path in args.model_configs:
        game_env.append_models_config(utils.load_config(config_path))

    game_env.set_game(game)

    lock = threading.Lock()

    if args.num_workers == 1:
        results = []
        for match_idx in range(args.num_matches):
            match_arg = {
                'match_idx': match_idx,
                'game_name': game_name,
                'agents': agents,
                'reversed_agents': reversed_agents,
                'models': models,
                'reversed_models': reversed_models,
                'result_path': result_path,
                'args': args,
                'lock': lock
            }
            results.append(run_match(match_arg))
    else:
        match_arg_list = []
        for match_idx in range(args.num_matches):
            match_arg_list.append({
                'match_idx': match_idx,
                'game_name': game_name,
                'models': models,
                'reversed_models': reversed_models,
                'agents': agents,
                'reversed_agents': reversed_agents,
                'result_path': result_path,
                'args': args,
                'lock': lock
            })
        results = utils.parallel_func(run_match, match_arg_list,
                                      num_workers=args.num_workers)
        remaining_matches_param = pick_out_invalid_matches(results)

        while len(results) < args.threshold_matches and len(remaining_matches_param) != 0:
            added_results = utils.parallel_func(run_match, remaining_matches_param,
                                                num_workers=min(args.num_workers, len(remaining_matches_param)))
            results = results + added_results
            remaining_matches_param = pick_out_invalid_matches(added_results)
        # save to jsonl
        results = [r[0] for r in results]
    # utils.save_jsonl(results, result_path)


def pick_out_invalid_matches(results):
    invalid_matches_param = []
    for history, parameters in results:
        if history["matches"][0]["status"] != "Normal":
            invalid_matches_param.append(parameters)
    return invalid_matches_param


def run_match(params):
    match_idx = params['match_idx']
    game_name = params['game_name']
    agents = params['agents']
    reversed_agents = params['reversed_agents']
    models = params['models']
    reversed_models = params['reversed_models']
    result_path = params['result_path']

    args = params['args']
    game_env = BaseGameEnv()
    game = utils.load_game(os.path.join(
        args.game_config_root, f'{game_name}.yaml'))
    game_env.save_game_config(utils.load_config(
        os.path.join(args.game_config_root, f'{game_name}.yaml')))

    game_env.set_game(game)

    if args.exchange_first_player and match_idx >= (args.num_matches / 2):
        # exchange first player
        game_env.set_agents(reversed_agents)
        game_env.set_models(reversed_models)
        reversed_agent_configs = copy.deepcopy(args.agent_configs)
        reversed_agent_configs.reverse()
        for config_path in reversed_agent_configs:
            game_env.append_agents_config(utils.load_config(config_path))

        reversed_model_configs = copy.deepcopy(args.model_configs)
        reversed_model_configs.reverse()
        for config_path in reversed_model_configs:
            game_env.append_models_config(utils.load_config(config_path))
    else:
        game_env.set_agents(agents)
        game_env.set_models(models)

        for config_path in args.agent_configs:
            game_env.append_agents_config(utils.load_config(config_path))

        for config_path in args.model_configs:
            game_env.append_models_config(utils.load_config(config_path))

    game_env.play()
    res = game_env.history_tracker.to_dict()
    with params['lock']:
        with open(result_path, 'a') as file:
            file.writelines(json.dumps(res) + '\n')

    return (res, params)


def main(args):
    if args.api_keys:
        for k in args.api_keys:
            if k.startswith('sk-'):
                os.environ["OPENAI_API_KEY"] = k
            elif k.startswith('esecret'):
                os.environ["ANYSCALE_API_KEY"] = k
            else:
                os.environ["DEEPINFRA_API_KEY"] = k

    utils.set_seed(args.seed)

    for game_name in args.game_names:
        run_game(game_name)


if __name__ == '__main__':
    args = get_args()
    main(args)
