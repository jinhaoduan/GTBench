
from gamingbench.prompts.system_prompts import tictactoe
from gamingbench.prompts.system_prompts import connect4
from gamingbench.prompts.system_prompts import texasholdem
from gamingbench.prompts.system_prompts import backgammon
from gamingbench.prompts.system_prompts import breakthrough
from gamingbench.prompts.system_prompts import first_sealed_auction
from gamingbench.prompts.system_prompts import gin_rummy
from gamingbench.prompts.system_prompts import liars_dice
from gamingbench.prompts.system_prompts import negotiation
from gamingbench.prompts.system_prompts import nim
from gamingbench.prompts.system_prompts import pig
from gamingbench.prompts.system_prompts import kuhn_poker
from gamingbench.prompts.system_prompts import prisoners_dilemma


# maps
mapping = {
    'tictactoe': tictactoe,
    'connect4': connect4,
    'breakthrough': breakthrough,
    'first_sealed_auction': first_sealed_auction,
    'liars_dice': liars_dice,
    'negotiation': negotiation,
    'nim': nim,
    'pig': pig,
    'kuhn_poker': kuhn_poker,
    'python_iterated_prisoners_dilemma': prisoners_dilemma
}


def construct_system_prompt(environment_name):
    return mapping[environment_name].SYSTEM_PROMPT
