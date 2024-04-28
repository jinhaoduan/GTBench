
from gamingbench.prompts.observation_prompts import connect4
from gamingbench.prompts.observation_prompts import tictactoe
from gamingbench.prompts.observation_prompts import breakthrough
from gamingbench.prompts.observation_prompts import first_sealed_auction
from gamingbench.prompts.observation_prompts import liars_dice
from gamingbench.prompts.observation_prompts import negotiation
from gamingbench.prompts.observation_prompts import nim
from gamingbench.prompts.observation_prompts import pig
from gamingbench.prompts.observation_prompts import kuhn_poker
from gamingbench.prompts.observation_prompts import prisoners_dilemma
from gamingbench.prompts.observation_prompts import dots_and_boxes
from gamingbench.prompts.observation_prompts import crazy_eights



# maps
mapping = {
    'connect4': connect4,
    'tictactoe': tictactoe,
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


def construct_observation_prompt(observations, environment_name):

    return mapping[environment_name].construct_observation_prompt(observations)


# from gamingbench.prompts.observation_prompts import connect4
# from gamingbench.prompts.observation_prompts import tictactoe
# from gamingbench.prompts.observation_prompts import breakthrough
# from gamingbench.prompts.observation_prompts import first_sealed_auction
# from gamingbench.prompts.observation_prompts import liars_dice
# from gamingbench.prompts.observation_prompts import negotiation
# from gamingbench.prompts.observation_prompts import nim
# from gamingbench.prompts.observation_prompts import pig
# from gamingbench.prompts.observation_prompts import kuhn_poker
# from gamingbench.prompts.observation_prompts import prisoners_dilemma

from gamingbench.prompts.observation_prompts import crazy_eights


# maps
# mapping = {
#     'connect4': connect4,
#     'tictactoe': tictactoe,
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
    'crazy_eights': crazy_eights
}


def construct_observation_prompt(observations, environment_name):

    return mapping[environment_name].construct_observation_prompt(observations)
