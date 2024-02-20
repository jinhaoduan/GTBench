
from gamingbench.agents.cot_agent import CoTAgent
from gamingbench.prompts.step_prompts.cot_agent import construct_step_prompt


class SCCoTAgent(CoTAgent):

    def __init__(self, config, **kwargs):
        super(SCCoTAgent, self).__init__(config)
