
from gamingbench.prompts.step_prompts import prompt_agent
from gamingbench.prompts.step_prompts import cot_agent
from gamingbench.prompts.step_prompts import tot_agent

# maps
mapping = {
    'promptagent': prompt_agent
}


def construct_system_prompt(environment_name):

    return mapping[environment_name].SYSTEM_PROMPT
