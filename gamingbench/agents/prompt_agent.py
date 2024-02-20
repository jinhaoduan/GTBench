
from gamingbench.agents.base_agent import BaseAgent
from gamingbench.prompts.step_prompts.prompt_agent import construct_step_prompt
from gamingbench.prompts.observation_prompts import construct_observation_prompt
from gamingbench.prompts.system_prompts import construct_system_prompt


class PromptAgent(BaseAgent):

    def __init__(self, config, **kwargs):
        super(PromptAgent, self).__init__(config)

        self.step_prompt_constructor = construct_step_prompt

    def step(self, observations):
        """

        :param observations:
        :return:
        """

        self.logger.info('-' * 20 + f'{self.agent_name} Begin' + '-' * 20)
        query_list = []

        env_name = observations['env_name']
        system_prompt = construct_system_prompt(env_name)
        observation_prompt = construct_observation_prompt(
            observations, env_name)
        step_instruct = self.step_prompt_constructor(observations)
        step_prompt = step_instruct['prompt']
        observation_prompt = observation_prompt + '\n' + step_prompt
        regex = step_instruct['regex']

        msgs = self.construct_init_messages(
            system_prompt, observation_prompt)

        responses, query = self.llm_query(
            msgs, n=self.num_generations, stop=None, prompt_type='move')
        query_list.append(query)

        self.logger.info(f'Prompt: {observation_prompt}')
        self.logger.info(f'Response: {responses}')

        moves = self.parse_with_regex(responses, regex)
        if len(moves) != 0:
            move = self.post_processing(moves, majority_vote=False)
        else:
            move = ""

        self.logger.info('-' * 20 + f'{self.agent_name} End' + '-' * 20)
        return move, query_list
