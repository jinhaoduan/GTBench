import os
import json
import subprocess


def nra_value(me_score, opponent_score):
    '''
    return Normalized Relative Advantage (NRA) value
    '''
    # avoid division by zero
    if me_score == 0 and opponent_score == 0:
        return 0
    return (me_score - opponent_score) / (abs(me_score) + abs(opponent_score))


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

    me = f'{agents_info[0]["agent_name"]}_{agents_info[0]["nickname"]}'
    opponent = f'{agents_info[1]["agent_name"]}_{agents_info[1]["nickname"]}'

    if matches:
        winner = matches[0]['winner']
        winner_score = matches[0]['winner_score']
        loser_score = matches[0]['loser_score']
        # make dic mapping agent name to score
        if winner == me:
            scores = {me: winner_score,
                      opponent: loser_score}
        else:
            scores = {me: loser_score,
                      opponent: winner_score}
    else:
        winner = None
        scores = {me: 0,
                  opponent: 0}

    return {
        'agents': agents_info,
        'winner': winner,
        'scores': scores,
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
    api_keys=['sk-proj-PhZgYSrRcosjJzEi1ARxT3BlbkFJVpFfRaqj7EtQ0ihuBf9O' 'LpsCdyMP09m8BFVz85Zwrnihk2aNpMMA']
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


def setup_and_run_experiments(model, method, n):
    static_model = model
    if n % 2 == 1:
        opponent_model = 'gpt-35-turbo-1106'
    else:
        opponent_model = model
        model = 'gpt-35-turbo-1106'
    exp_name = f'{static_model}_{method}_{n}'
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
        ("gpt-4-turbo", "prompt_agent"),
        ("gpt-4-turbo", "cot_agent"),
        ("gpt-35-turbo-1106", "cot_agent"),
        ("gpt-35-turbo-1106", "sccot_agent"),
        ("CodeLlama-34b-Instruct-hf", "prompt_agent"),
        ("Llama-2-70b-chat-hf", "sccot_agent"),
        ("CodeLlama-34b-Instruct-hf", "cot_agent"),
        ("Llama-2-70b-chat-hf", "cot_agent"),
        ("CodeLlama-34b-Instruct-hf", "sccot_agent"),
        ("Llama-2-70b-chat-hf", "prompt_agent"),
    ]

    for model, method in models_methods:
        llm_score = 0
        opponent_score = 0
        static_model = model
        for i in range(8):
            # setup_and_run_experiments(model, method, n=i+1)
            if i % 2 == 1:
                model = 'gpt-35-turbo-1106'
            else:
                model = static_model
            # check if this folder exists
            if not os.path.exists(f'experiments/{static_model}_{method}_{i+1}/{model}/crazy_eights'):
                continue
            folder = os.listdir(
                f'experiments/{static_model}_{method}_{i+1}/{model}/crazy_eights')
            # get the jsonl file from the folder
            jsonl_file = [
                file for file in folder if file.endswith('.jsonl')][0]
            results = evaluate_single_file(
                f'experiments/{static_model}_{method}_{i+1}/{model}/crazy_eights/{jsonl_file}')
            if len(results) == 0:
                continue
            # print("results", results)
            if i % 2 == 1:
                me = f'{results[0]["agents"][1]["agent_name"]}_{results[0]["agents"][1]["nickname"]}'
                opponent = f'{results[0]["agents"][0]["agent_name"]}_{results[0]["agents"][0]["nickname"]}'
            else:
                me = f'{results[0]["agents"][0]["agent_name"]}_{results[0]["agents"][0]["nickname"]}'
                opponent = f'{results[0]["agents"][1]["agent_name"]}_{results[0]["agents"][1]["nickname"]}'
            llm_score += results[0]['scores'][me]
            opponent_score += results[0]['scores'][opponent]
        nra = nra_value(llm_score, opponent_score)
        print(f"{static_model}_{method} NRA value:", nra)
        # break


if __name__ == "__main__":
    main()
