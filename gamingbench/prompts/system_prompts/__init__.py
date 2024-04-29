
from gamingbench.prompts.system_prompts import tictactoe
from gamingbench.prompts.system_prompts import connect4
from gamingbench.prompts.system_prompts import breakthrough
from gamingbench.prompts.system_prompts import first_sealed_auction
from gamingbench.prompts.system_prompts import liars_dice
from gamingbench.prompts.system_prompts import negotiation
from gamingbench.prompts.system_prompts import nim
from gamingbench.prompts.system_prompts import pig
from gamingbench.prompts.system_prompts import kuhn_poker
from gamingbench.prompts.system_prompts import prisoners_dilemma
from gamingbench.prompts.system_prompts import crazy_eights
from gamingbench.prompts.system_prompts import dots_and_boxes




# maps
# mapping = {
#     'tictactoe': tictactoe,
#     'connect4': connect4,
#     'breakthrough': breakthrough,
#     'first_sealed_auction': first_sealed_auction,
#     'liars_dice': liars_dice,
#     'negotiation': negotiation,
#     'nim': nim,
#     'pig': pig,
#     'kuhn_poker': kuhn_poker,
#     'python_iterated_prisoners_dilemma': prisoners_dilemma
# }

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
    'python_iterated_prisoners_dilemma': prisoners_dilemma,
    'dots_and_boxes': dots_and_boxes,
    'crazy_eights': crazy_eights
}


def construct_system_prompt(environment_name):
    return mapping[environment_name].SYSTEM_PROMPT
