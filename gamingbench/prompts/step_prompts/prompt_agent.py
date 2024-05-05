
from gamingbench.prompts.regex_and_format import get_step_env_regex_and_format


def construct_step_prompt(observation):

    env_name = observation.get('env_name', '')

    regex, format = get_step_env_regex_and_format(env_name)

    prompt = f"""First think about your current situation, then you must choose one action from legal actions to set up advantages.

Your output must be in the following format:

Action:
Your action wrapped with <>, {format}

Please return your answer without explanation!
"""
    return {
        'prompt': prompt,
        'regex': regex,
    }
