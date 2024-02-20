
from gamingbench.agents.prompt_agent import PromptAgent
from gamingbench.prompts.step_prompts.cot_agent import construct_step_prompt


class CoTAgent(PromptAgent):

    def __init__(self, config, **kwargs):
        super(CoTAgent, self).__init__(config)

        self.step_prompt_constructor = construct_step_prompt
