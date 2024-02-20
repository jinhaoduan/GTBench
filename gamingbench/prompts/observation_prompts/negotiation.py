
def _construct_head_prompt():
    return 'You are negotiating the division of Peppers, Strawberries, and Cherries with the opponent. Different values these items hold for both you and your opponent. The process is structured into two stages per round: the proposal stage and the utterance stage.' \

def _construct_propose_stage_prompt():
    return 'Now, you are in the Proposal stage: you\'ll determine the division of items you desire. This is expressed as [a, b, c], where \'a\' represents the quantity of Peppers, \'b\' the quantity of Strawberries, and \'c\' the quantity of Cherries you wish to acquire. It\'s crucial to base this division on the perceived value these items have for you, keeping in mind that the goal is to reach a mutually agreeable solution.'

def _construct_utterance_stage_prompt():
    return 'Now, you are in the Utterance Stage: you communicate to your opponent what you want, again in the format [a, b, c]. This utterance is your strategic communication and doesn\'t necessarily have to reflect your actual desires or the proposal you formulated in the first stage. It\'s a tool for negotiation, potentially used to mislead, bluff, or strategically reveal information to your opponent.'

def _solution_prompt():
    return 'Remember, the key in such negotiations is understanding that your opponent also has their value system for these items, which is unknown to you. Balancing between revealing your true desires and misleading your opponent to gain a favorable outcome is essential. It\'s also important to be adaptive, as the negotiation progresses and you gather more information about your opponent\'s preferences and tactics.'


def construct_observation_prompt(observations):

    turn_type = observations['turn_type']
    item_pool = observations['item_pool']
    most_recent_proposal = observations['most_recent_proposal']
    most_recent_utterance = observations['most_recent_utterance']
    value_vector = observations['self_value_vector']

    item_pool_prompt = f'There are {item_pool[0]} peppers, {item_pool[1]} strawberries, and {item_pool[2]} cherries in the item pool.'

    value_vector = f'The value of each pepper is {value_vector[0]} for you. The value of each strawberry is {value_vector[1]} for you. ' \
                   f'The value of each cherry is {value_vector[2]} for you.'

    if turn_type == 'Proposal':
        if most_recent_utterance is not None:
            last_utterance_prompt = f'Last time, the utterance of the opponent was to take ' \
                                    f'{most_recent_utterance[0]} peppers, {most_recent_utterance[1]} strawberries, ' \
                                    f'and {most_recent_utterance[2]} cherries from the item pool.'
        else:
            last_utterance_prompt = ''

        if most_recent_proposal is not None:
            last_proposal_prompt = f'Now, the opponent propose to take {most_recent_proposal[0]} peppers, ' \
                                   f'{most_recent_proposal[1]} strawberries, and {most_recent_proposal[2]} cherries from the item pool.'
        else:
            last_proposal_prompt = ''

        stage_prompt = _construct_propose_stage_prompt()
        last_situation_prompt = '\n' + last_proposal_prompt + '\n' + last_utterance_prompt
        query_prompt = 'Now, it is your decision. ' \
                       'If you find the proposal raised by the opponent is acceptable, you should output <Agree>. ' \
                       'Otherwise, you should output your proposal in the format <Proposal: [a, b, c]>.'

    elif turn_type == 'Utterance':
        if most_recent_utterance is not None:
            last_utterance_prompt = f'Last time, the utterance of the opponent was to take ' \
                                    f'{most_recent_utterance[0]} peppers, {most_recent_utterance[1]} strawberries, ' \
                                    f'and {most_recent_utterance[2]} cherries from the item pool.'
        else:
            last_utterance_prompt = ''

        if most_recent_proposal is not None:
            last_proposal_prompt = f'You proposed to take {most_recent_proposal[0]} peppers, ' \
                                   f'{most_recent_proposal[1]} strawberries, and {most_recent_proposal[2]} cherries from the item pool.'
        else:
            last_proposal_prompt = ''

        stage_prompt = _construct_utterance_stage_prompt()
        last_situation_prompt = _construct_propose_stage_prompt() + '\n' + last_utterance_prompt + '\n' + last_proposal_prompt
        query_prompt = 'Now, it is your turn to provide your utterance regarding the division of items. The utterance is what you' \
                       'want to told to your opponent and does not mean your real intent. You should output your utterance in the format <Utterance: [a, b, c]>.\n' \
                       'For each category, you can not take all the items in a category, i.e., you can not take all 5 Peppers, 5 Strawberries, or 5 Cherries. ' \
                       'Instead, you have to leave at least one item for each category to your opponent.'
    else:
        raise ValueError

    return _construct_head_prompt() + '\n' + stage_prompt + '\n' + item_pool_prompt + '\n' + value_vector + '\n' + last_situation_prompt + '\n' + query_prompt

if __name__ == '__main__':
    observation = {
        'turn_type': 'Proposal',
        'item_pool': '5 5 5'.split(' '),
        'most_recent_proposal': '2 1 4'.split(' '),
        'most_recent_utterance': '1 3 3'.split(' '),
        'self_value_vector': '6 5 1'.split(' ')
    }
    print(_construct_head_prompt() + '\n\n' + construct_observation_prompt(observation))