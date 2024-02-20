import json
from collections import defaultdict


class Query:
    def __init__(self, messages: list, prompt_type: str, llm_output: list, token_size: int = 0) -> None:

        assert prompt_type in ['move', 'plan', 'vote']
        self.messages = messages
        self.prompt_type = prompt_type
        self.llm_output = llm_output
        self.token_size = token_size
        pass

    def set_token_size(self, num):
        self.token_size = num

    def to_dict(self):
        return {"messages": self.messages,
                "prompt_type": self.prompt_type,
                "llm_output": self.llm_output,
                "token_size": self.token_size}

    def append_llm_output(self, output: str):
        self.llm_output.append(output)

    def __json__(self):
        return self.to_dict()


class Step:
    def __init__(self, agent: str, observation: str = "", move: str = "") -> None:
        self.agent = agent                       # agents name
        self.observation = observation           # observation
        self.move = move
        self.queries = []                          # should be list of str

    def set_observation(self, observation):
        self.observation = observation

    def set_model_name(self, name):
        self.model_name = name

    def set_move(self, move):
        self.move = move

    def add_query(self, query):
        self.queries.append(query)
        pass

    def get_token_size(self):
        self.token_size = sum([q.token_size for q in self.queries])
        return self.token_size

    def to_dict(self):
        return {"agent": self.agent,
                "observation": self.observation,
                "move": self.move,
                "queries": [q.to_dict() for q in self.queries],
                "token_size": self.get_token_size(),
                "model_name": self.model_name
                }

    def __json__(self):
        return self.to_dict()


class GameMatch:

    def __init__(self) -> None:
        self.winner = ""   # the name of the agent
        self.steps = []
        self.status = "Normal"
        self.agents_at_fault = []
        self.agents = set()
        self.winner_score = 0
        self.loser_score = 0
        pass

    def set_winner(self, winner):
        self.winner = winner

    def reset(self):
        '''
        This function will clear all steps and agents
        '''
        self.steps.clear()
        self.winner = ""

    def add_step(self, step):
        self.steps.append(step)
        self.agents.add(step.agent)

    def get_steps_by_agent(self, agent_name):
        steps = [step for step in self.steps if step.agent == agent_name]
        return steps
        pass

    def get_token_size(self):
        self.token_size = sum([s.get_token_size() for s in self.steps])
        return self.token_size

    def get_moves_by_agent(self, agent_name):
        steps = self.get_steps_by_agent(agent_name)
        return [s.move for s in steps]

    def to_dict(self):
        return {"winner": self.winner,
                "agents": list(self.agents),
                "steps": [s.to_dict() for s in self.steps],
                "status": self.status,
                "agents_at_fault": self.agents_at_fault,
                "winner_score": self.winner_score,
                "loser_score": self.loser_score,
                "token_size": self.get_token_size()}

    def __json__(self):
        return self.to_dict()


class HistoryTracker:
    def __init__(self) -> None:
        self.game_config = {}
        self.matches = []
        self.agents = set()
        self.agents_config = []
        self.models_config = []
        pass

    def get_win_rate(self):

        valid_match_num = 0
        agents_win_match = defaultdict(lambda: 0)

        for m in self.matches:
            if m.status == "Normal":
                valid_match_num += 1
                if m.winner != "":
                    agents_win_match[m.winner] += 1
        if valid_match_num != 0:
            for key, val in agents_win_match.items():
                agents_win_match[key] = val/valid_match_num
        else:
            for key, val in agents_win_match.items():
                agents_win_match[key] = 0

        return dict(agents_win_match)

    def get_all_matches(self):
        return self.matches

    def set_game_config(self, config):
        self.game_config = config

    def add_agents_config(self, config):
        self.agents_config.append(config)

    def add_models_config(self, config):
        self.models_config.append(config)

    def add_match(self, match):
        self.matches.append(match)
        for agent in match.agents:
            self.agents.add(agent)

    def get_token_size(self):
        self.token_size = sum([s.get_token_size() for s in self.matches])
        return self.token_size

    def to_dict(self):
        return {
            "game_config": self.game_config,
            "agents_config": self.agents_config,
            "models_config": self.models_config,
            "win_rate": self.get_win_rate(),
            "matches": [m.to_dict() for m in self.matches],
            "token_size": self.get_token_size()}

    def __json__(self):
        return self.to_dict()

    def clear(self):
        '''
        This function will clear all steps and agents
        '''
        self.matches.clear()
        self.agents.clear()

    def save_as_json(self, path):
        '''
        outout a json file containing agents' name and steps
        '''
        data = self.to_dict()
        json_data = json.dumps(data, indent=2)
        # Save JSON to a file
        with open(path, 'w') as json_file:
            json_file.write(json_data)
        pass

