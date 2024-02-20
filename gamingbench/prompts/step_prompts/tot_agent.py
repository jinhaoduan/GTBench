
from gamingbench.prompts.regex_and_format import get_step_env_regex_and_format

def _get_stop_signs(env_name):
    stop_signs = ['Action:', None]
    return stop_signs


def construct_step_prompt(observation):

    env_name = observation.get('env_name', '')

    regex, format = get_step_env_regex_and_format(env_name)

    stop_signs = _get_stop_signs(env_name)

    prompt = f"""First think about your current situation, then you must choose one action from legal actions to set up advantages.
    
Your output should be of the following format:

Thought:
Your thought.
    
Action:
Your action wrapped with <>, e.g., {format}
"""

    return {
        'prompt': prompt,
        'regex': regex,
        'stop_signs': stop_signs
    }


def construct_voting_prompt(observation):
    prompt = '''Given an instruction and several choices, decide which choice is most promising. Analyze each choice in detail, then conclude in the last line "The best choice is {s}", where s the integer id of the choice.'''
    return {
        'prompt': prompt,
        'regex': '.*best choice is .*(\d+).*'
    }
