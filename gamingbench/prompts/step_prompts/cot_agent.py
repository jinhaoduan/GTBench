
from gamingbench.prompts.regex_and_format import get_step_env_regex_and_format

def construct_step_prompt(observation):

    env_name = observation.get('env_name', '')

    regex, format = get_step_env_regex_and_format(env_name)

    action_reminder = f"Remember, you can only choose one move from the legal actions which is {observation['legal_moves']}" if len(observation[
        'legal_moves']) <= 10 else f"Remember, you can only choose one move from the legal actions."

    prompt = f"""First think about your current situation, then you must choose one action from legal actions to set up advantages.

Your output must be in the following format strictly:

Thought:
Your thought.

Action:
Your action wrapped by <>, i.e., {format}

{action_reminder}
"""
    return {
        'prompt': prompt,
        'regex': regex,
    }