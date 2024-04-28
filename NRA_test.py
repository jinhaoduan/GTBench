import os
import json
import subprocess


def nra_value(winner_score, loser_score):
    '''
    return Normalized Relative Advantage (NRA) value
    '''
    return (winner_score - loser_score) / (abs(winner_score) + abs(loser_score))


def process_game_data(json_data):
    agents_config = json_data['agents_config']
    models_config = json_data['models_config']
    matches = json_data['matches']

    agents_info = []
    for agent, model in zip(agents_config, models_config):
        agents_info.append({
            'agent_name': agent['agent_name'],
            'nickname': model['nick_name']
        })

    if matches:
        winner = matches[0]['winner']
        winner_score = matches[0]['winner_score']
        loser_score = matches[0]['loser_score']
        nra = nra_value(winner_score, loser_score)
    else:
        winner, nra = None, 0

    return {
        'agents': agents_info,
        'winner': winner,
        'nra': nra
    }


def evaluate_single_file(file_path):
    results = []
    with open(file_path, 'r') as file:
        for line in file:
            json_data = json.loads(line.strip())
            result = process_game_data(json_data)
            results.append(result)
    return results


def run_single_experiment(
    seed=0,
    output_root="./experiments",
    exp_name='test',
    num_matches=1,
    num_workers=1,
    threshold_matches=100,
    game_name='crazy_eights',
    model_config_root='gamingbench/configs/model_configs',
    llm_name='Bob',
    opponent_llm_name='Alice',
    agent_config_root='gamingbench/configs/agent_configs',
    agent_name='prompt_agent',
    opponent_agent_name='prompt_agent',
    api_keys=[]
):
    command = [
        "python3", "-m", "gamingbench.main",
        "--num-matches", str(num_matches),
        "--exp-root", f"{output_root}/{exp_name}/{llm_name}",
        "--seed", str(seed),
        "--game-name", game_name,
        "--agent-configs",
        f"{agent_config_root}/{agent_name}.yaml",
        f"{agent_config_root}/{opponent_agent_name}.yaml",
        "--model-configs",
        f"{model_config_root}/{llm_name}.yaml",
        f"{model_config_root}/{opponent_llm_name}.yaml",
        "--api-keys", *api_keys,
        "--exchange-first-player",
        "--num-workers", str(num_workers),
        "--threshold-matches", str(threshold_matches)
    ]

    # for debugging purposes
    print("Running command:")
    print(" ".join(command))

    try:
        result = subprocess.run(command)
        print("Command output:", result.stdout)
        print("Error output:", result.stderr)
    except subprocess.CalledProcessError as e:
        print("Error running command:", e)


def setup_and_run_experiments(model, method):
    opponent_model = 'gpt-35-turbo-1106'
    exp_name = f'{model}_{method}'
    output_root = './experiments'

    output_dir = os.path.join(output_root, exp_name)
    os.makedirs(output_dir, exist_ok=True)

    run_single_experiment(
        output_root=output_root,
        exp_name=exp_name,
        game_name='crazy_eights',
        llm_name=model,
        opponent_llm_name=opponent_model,
        agent_name=method.lower(),
        opponent_agent_name='prompt_agent'
    )


def main():
    models_methods = [
        # ("gpt-4-turbo", "prompt_agent"),
        # ("gpt-4-turbo", "cot_agent"),
        # ("gpt-35-turbo-1106", "cot_agent"),
        # ("gpt-35-turbo-1106", "sccot_agent"),
        # ("gpt-35-turbo-1106", "tot_agent"),
        ("CodeLlama-34b-Instruct-hf", "prompt_agent"),
        # ("Llama-2-70b-chat-hf", "sccot_agent"),
        # ("CodeLlama-34b-Instruct-hf", "cot_agent"),
        # ("Llama-2-70b-chat-hf", "cot_agent"),
        # ("Mistral-7B-OpenOrca", "cot_agent"),
        # ("CodeLlama-34b-Instruct-hf", "sccot_agent"),
        # ("Mistral-7B-Instruct-v01", "sccot_agent"),
        # ("CodeLlama-34b-Instruct-hf", "tot_agent"),
        # ("Llama-2-70b-chat-hf", "prompt_agent"),
        # ("Mistral-7B-OpenOrca", "tot_agent"),
        # ("Mistral-7B-OpenOrca", "prompt_agent")
    ]

    for model, method in models_methods:
        setup_and_run_experiments(model, method)

if __name__ == "__main__":
    main()
