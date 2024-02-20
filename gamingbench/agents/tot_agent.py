
import itertools

from gamingbench.agents.base_agent import BaseAgent
from gamingbench.prompts.system_prompts import construct_system_prompt
from gamingbench.prompts.observation_prompts import construct_observation_prompt
from gamingbench.prompts.step_prompts.tot_agent import construct_step_prompt, construct_voting_prompt

class ToTAgent(BaseAgent):

    def __init__(self, config, **kwargs):
        super(ToTAgent, self).__init__(config)
        self.task_steps = config.task_steps
        self.method_generate = config.method_generate
        self.method_evaluate = config.method_evaluate
        self.method_select = config.method_select
        self.n_generate_sample = config.n_generate_sample
        self.n_evaluate_sample = config.n_evaluate_sample
        self.n_select_sample = config.n_select_sample
        self.prompt_sample = config.prompt_sample

    def step(self, observations):
        self.logger.info('-' * 20 + 'ToTAgent Begin' + '-' * 20)
        # we follow the official tot implementation: https://github.com/princeton-nlp/tree-of-thought-llm/blob/master/src/tot/methods/bfs.py
        env_name = observations['env_name']
        system_prompt = construct_system_prompt(env_name)
        observation_prompt = construct_observation_prompt(observations, environment_name=env_name)

        step_instruct = construct_step_prompt(observations)
        step_prompt = step_instruct['prompt']
        step_regex = step_instruct['regex']
        stop_signs = step_instruct['stop_signs']

        voting_instruct = construct_voting_prompt(observations)
        voting_prompt = voting_instruct['prompt']
        voting_regex = voting_instruct['regex']

        ys = ['']
        query_list = []
        for step in range(self.task_steps):
            # generation
            x = self.construct_init_messages(system_prompt, observation_prompt + '\n' + step_prompt)
            if self.method_generate == 'sample':
                new_ys = [self._get_samples(x, y, self.n_generate_sample, stop=stop_signs[step]) for y in ys]
                query_list += [query[1] for query in new_ys]
                new_ys = [new_y[0] for new_y in new_ys]

            else:
                raise NotImplementedError
            new_ys = list(itertools.chain(*new_ys))
            ids = list(range(len(new_ys)))
            # evaluation
            x = self.construct_init_messages(system_prompt, observation_prompt)
            if self.method_evaluate == 'vote':
                values, query = self._vote(x, new_ys, self.n_evaluate_sample, voting_prompt, voting_regex)
                query_list.append(query)
            else:
                raise NotImplementedError

            # selection
            if self.method_select == 'greedy':
                select_ids = sorted(ids, key=lambda x: values[x], reverse=True)[:self.n_select_sample]
            else:
                raise NotImplementedError

            ys = [new_ys[select_id] for select_id in select_ids]

        parsed_moves = self.parse_with_regex(ys, step_regex)
        parsed_moves = self.post_processing(parsed_moves, majority_vote=True)
        self.logger.info('-' * 20 + 'ToTAgent End' + '-' * 20)
        return parsed_moves, query_list

    def _get_samples(self, messages, y, n_generate_sample, stop):
        messages[-1]['content'] += '\n' + y
        self.logger.info('Thought/Action Prompt:')
        self.logger.info(messages[-1]['content'])
        responses, query = self.llm_query(messages, n=n_generate_sample, stop=stop, prompt_type='plan')
        self.logger.info('Thought/Action Response:')
        self.logger.info(responses)
        return responses, query


    def _vote(self, messages, y, n_evaluation_sample, voting_prompt, voting_regex):
        values = [0] * len(y)
        for idx, gen in enumerate(y):
            messages[-1]['content'] += '\n' + f'Choice{idx + 1}: {gen}'
        messages[-1]['content'] += '\n' + voting_prompt
        self.logger.info('Voting Prompt:')
        self.logger.info(messages[-1]['content'])
        responses, query = self.llm_query(messages, n=n_evaluation_sample, stop=None, prompt_type='vote')
        self.logger.info('Voting Response:')
        self.logger.info(responses)
        votes = self.parse_with_regex(responses, regex=voting_regex)
        filtered_votes = []
        for r in votes:
            # Use the last matched item as the model answer
            r = r[-1]
            if r is not None and int(r) - 1 in list(range(len(y))):
                filtered_votes.append(int(r) - 1)
            else:
                # TODO error print
                pass

        for v in filtered_votes:
            values[v] += 1

        return values, query
