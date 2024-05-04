import os
import json
import subprocess
import sys 
import random
import numpy as np
import datetime 

# Get the current datetime
current_time = datetime.datetime.now()


# Format the datetime to MM-DD-YYYY-HH-MM
formatted_time = current_time.strftime("%m-%d_%H-%M")

directory = f"./experiments_{formatted_time}"
if not os.path.exists(directory):
    os.makedirs(directory)

log_file_name = f"./experiments_{formatted_time}/run_log.txt"

def overall_log(file_name, line_to_write):

    # Open the file in append mode ('a') so that data is written to the end of the file
    # If the file does not exist, it will be created
    with open(file_name, 'a') as file:
        # Write the line_to_write to the file, and add a newline character to ensure
        # it starts on a new line
        file.write(line_to_write + '\n')


def NRA_value_calculation(me_score, opponent_score):
    '''
    return Normalized Relative Advantage (NRA) value
    '''
    # avoid division by zero
    if me_score == 0 and opponent_score == 0:
        return 0
    return (me_score - opponent_score) / (abs(me_score) + abs(opponent_score))


def process_game_data(json_data):

    status = json_data["matches"][0]["status"]

    if status != "Normal": 
        return "ABNORMAL STATUS"

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

    # just read the first line 
    with open(file_path, 'r') as file:
        for line in file:
            json_data = json.loads(line.strip())
            result = process_game_data(json_data)
            return result 

# RUN JUST ONE MATCH 
def run_single_experiment(
    seed=0,
    output_root=f"./experiments_{formatted_time}",
    exp_name='test',
    num_matches=1,
    num_workers=1,
    threshold_matches=1,
    game_name="crazy_eights",
    model_config_root='gamingbench/configs/model_configs',
    llm_name='Bob',
    opponent_llm_name='Alice',
    agent_config_root='gamingbench/configs/agent_configs',
    agent_name='prompt_agent',
    opponent_agent_name='prompt_agent',
    api_keys=[]
):
    
    rand =  str(int(np.random.rand() * 1000))
    command = [
        "python3",  "-W", "ignore", "-m", "gamingbench.main",
        "--num-matches", str(num_matches),
        "--exp-root", f"{output_root}/{exp_name}",
        "--seed", rand,
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
    # print("Running command:")
    # print(" ".join(command))

    try:
        # result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        resut = subprocess.run(command)
        # print("Command output:", result.stdout)
        # print("Error output:", result.stderr)
    except subprocess.CalledProcessError as e:
        print("Error running command:", e)


def setup_and_run_experiments(model, method, game, n):

    static_model = model

    exp_name = f'{static_model}_{method}_{n}'
    output_root = f'./experiments_{formatted_time}'

    output_dir = os.path.join(output_root, exp_name)
    os.makedirs(output_dir, exist_ok=True)

    if n % 2 == 1:
        opponent_model = 'gpt-35-turbo-1106'
        opponent_method = "prompt_agent"

        model = model 
        method = method 
    else:
        opponent_model = model
        opponent_method = method 

        model = 'gpt-35-turbo-1106'
        method = "prompt_agent"

    run_single_experiment(
        output_root=output_root,
        exp_name=exp_name,
        game_name=game,
        llm_name=model,
        opponent_llm_name=opponent_model,
        agent_name=method.lower(),
        opponent_agent_name=opponent_method.lower(), 
    )


def main():

    if len(sys.argv) != 5: 
        print("NRA_test.py usage: python3 NRA_test.py {game} {opponent_llm_model} {llm_reasoning_type} {num_matches}")
        print("NRA_test.py usage example: python3 NRA_test.py crazy_eights gpt-4-turbo prompt_agent 50")
        sys.exit(1)


    line_to_write = "python3"
    for el in sys.argv: 
        line_to_write += " " + el
        
    overall_log(log_file_name, line_to_write)

    game = sys.argv[1]
    model = sys.argv[2]
    method = sys.argv[3]
    num_matches = int(sys.argv[4])

    valid_matches_list = [] 
    overall_number_of_matches_run = 1 


    # while False:
    while len(valid_matches_list) < num_matches: 

        print(f"--------- On Match #{overall_number_of_matches_run:02} ---------")
        overall_log(log_file_name, f"--------- On Match #{overall_number_of_matches_run:02} ---------")

        try: 
            setup_and_run_experiments(model, method, game, overall_number_of_matches_run)
        except Exception as e:
            # Print the exception message
            print("Caught an exception:", e)
            overall_log(log_file_name, e)

            continue # just rerun 

        # evaluate the match result 
        result = check_if_match_result_was_valid(model, method, overall_number_of_matches_run, game) 

        # did not complete
        if result == "ABNORMAL STATUS": 

            print("did not finish this match")
            overall_log(log_file_name, "ABNORMAL STATUS DID NOT FINISH THIS MATCH")

        else:

            print("Winner of the Match: ", result[0])
            print("gpt_3.5 score", result[1])
            print(f"{model} score", result[2])

            overall_log(log_file_name, f"Winner of the Match: {result[0]}")
            overall_log(log_file_name, f"gpt_3.5 score: {result[1]}")
            overall_log(log_file_name, f"{model} score: {result[2]}")
            
            valid_matches_list.append(result)

        if overall_number_of_matches_run == 50: 
            completion_rate = len(valid_matches_list) / 50 
            

        print(f"------ Completed Match #{overall_number_of_matches_run:02} ------")
        overall_log(log_file_name, f"------ Completed Match #{overall_number_of_matches_run:02} ------")
        overall_number_of_matches_run+=1 


    gpt_35_score_sum = sum([el[1] for el in valid_matches_list])
    # print(gpt_35_score_sum)
    opponent_score_sum = sum([el[2] for el in valid_matches_list])
    # print(opponent_score_sum)


    nra_value = NRA_value_calculation(opponent_score_sum,gpt_35_score_sum)


    print("FINAL LOG:")
    print("NRA Value:" , nra_value)
    print("Completion Rate", completion_rate)

    overall_log(log_file_name, f"NRA Value: {nra_value}")
    overall_log(log_file_name, f"Completion Rate: {completion_rate}")


def check_if_match_result_was_valid(model, method, index, game): 

    folder = os.listdir(f'experiments_{formatted_time}/{model}_{method}_{index}/{game}')

    # get the jsonl file from the folder
    jsonl_file = [
        file for file in folder if file.endswith('.jsonl')][0]
    results = evaluate_single_file(
        f'experiments_{formatted_time}/{model}_{method}_{index}/{game}/{jsonl_file}')
    
    if results == "ABNORMAL STATUS": 
        return "ABNORMAL STATUS"

    print(f"Results for {model}_{method}_{index}:", results)

    gpt_35_nickame = "PromptAgent_gpt-3.5-turbo-1106"
    temp = list(results["scores"].keys())
    temp.remove("PromptAgent_gpt-3.5-turbo-1106")
    opponent_nickname = temp[0]

    winner = results["winner"]
    gpt_35_score = results['scores'][gpt_35_nickame]
    opponent_score = results['scores'][opponent_nickname]

    return (winner, gpt_35_score, opponent_score)

if __name__ == "__main__":

    main()
