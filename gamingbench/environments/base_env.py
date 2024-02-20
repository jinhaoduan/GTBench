import os.path

from gamingbench.utils import history_tracker
import json
import jsonlines


class BaseObservation(object):

    def __init__(self):
        pass


class BaseGameEnv(object):

    def __init__(self):
        self.agent_list = []
        self.env = None
        self.history_tracker = history_tracker.HistoryTracker()

    def set_game(self, game):
        self.game = game

    def save_game_config(self, game_config):
        self.history_tracker.set_game_config(game_config)

    def append_agents_config(self, config):
        self.history_tracker.add_agents_config(config)

    def append_models_config(self, config):
        self.history_tracker.add_models_config(config)

    def set_agents(self, agents):
        self.agent_list = agents

    def set_models(self, models):
        self.model_list = models

    def initialization(self):
        self.history_tracker.clear()
        pass

    def play(self):
        if self.game:
            self.game.play(self.agent_list, self.model_list,
                           self.history_tracker)
        pass

    def reset(self):
        if self.game:
            self.game.reset()

    def summarize(self, path=""):
        self.history_tracker.save_as_json(
            f"{path}/{self.agent_list[0].agent_name}_{self.agent_list[1].agent_name}_{self.agent_list[0].model.nick_name}_{self.agent_list[1].model.nick_name}.json")
        pass

    def save_result_to_jsonl(self, path):

        if os.path.exists(path):
            with open(path, 'a') as f:
                f.writelines(json.dumps(self.history_tracker.to_dict()) + '\n')
        else:
            raise FileNotFoundError()
