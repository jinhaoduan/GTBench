import re
from gamingbench.chat.chat import chat_llm
from gamingbench.utils.history_tracker import Query


class BaseModel(object):

    def __init__(self, config):
        self.model_path = config.llm_model_path
        self.max_tokens = config.max_tokens
        self.timeout = config.timeout
        self.temperature = config.temperature
        self.nick_name = config.nick_name

    def query(self, messages, n, stop, prompt_type):
        pass
