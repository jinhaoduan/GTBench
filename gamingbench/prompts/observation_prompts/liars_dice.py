
def _construct_head_prompt():
    # 1-4: at least 1 dice with face value as 4
    # the player may bid a higher quantity of any particular face, or the same quantity of a higher face (allowing a player to "re-assert" a face value they believe prevalent if another player increased the face value on their bid);
    return 'Liar\'s Dice is a game of bluffing and probability, played with two players and each player has 1 dice.' \
           'During each turn, a player can either bid a higher quantity of any particular face value or ' \
           'the same quantity of a higher face value than the previous bid. ' \
           'Each player tries to outbid their opponent without being caught in a lie. ' \
           '\n' \
           'The move in this game is denoted in <x dices, y value>, meaning there are at least x dices with face values as y.' \


def construct_observation_prompt(observations):

    self_dice_face_value = observations['self_dice_face_value']
    last_move = observations['last_move']
    legal_moves = observations['legal_moves']
    legal_move_str = ', '.join(legal_moves)

    if last_move is None:
        prompt = f'Currently, the face value of your dice is {self_dice_face_value}. You are the first to go.' \
                 '\n' \
                 'You are playing the Liar\'s Dice with another opponent. Therefore, there are only two dices in total.' \
                 f'\n\n' \
                 f'The legal actions are: {legal_move_str}.'
                 # 'You should call action <Liar> if the opponent called <2 dices, 6 value> in the last round. Because there is no other actions.' \
    else:
        prompt = f'Currently, the face value of your dice is {self_dice_face_value}. Last time, the opponent called action <{last_move}>.' \
                 '\n' \
                 'You are playing the Liar\'s Dice with another opponent. Therefore, there are only two dices in total.' \
                 f'\n\n' \
                 f'The legal actions are: {legal_move_str}.'
                 # 'You should call action <Liar> if the opponent called <2 dices, 6 value> in the last round. Because there is no other actions.' \

    return _construct_head_prompt() + '\n' + prompt