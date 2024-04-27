
def _construct_head_prompt():
    return 'Kuhn poker is a simple model zero-sum two-player imperfect-information game, amenable to a complete game-theoretic analysis. In Kuhn poker, the deck includes only three playing cards: a King (K), a Queen (Q), and a Jack (J).\n' \
           'One card is dealt to each player, and the third is put aside unseen. The players take turns either <Bet> to match the bet raised by the opponent or <Pas> to conceds the game.\n' \
           'If a player bets, the other player must either call the bet by matching it or fold by conceding the game. If both players pass, the game is over, and the player with the higher-ranking card wins. The card rankings are as follows: King (K) > Queen (Q) > Jack (J).\n' \
           '\n' \
           'You are playing Kuhn poker with the opponent. The actions are denoted by <Bet> and <Pass>.' \

def construct_observation_prompt(observations):

    card_mapping = {
        '0': 'Jack (J)',
        '1': 'Queen (Q)',
        '2': 'King (K)'
    }

    card = card_mapping[observations['card']]
    moves = observations['moves']
    player_idx = observations['player_idx']

    move_prompt = ''
    if moves is not None:
        move_prompt = 'Here are the past moves in this match:\n'

        for idx, m in enumerate(moves):
            if (player_idx + 1) % (idx + 1) == 0:
                role = 'you'
            else:
                role = 'the opponent'

            if m == 'b':
                move = '<Bet>'
            elif m == 'p':
                move = '<Pass>'
            else:
                raise ValueError

            if idx == 0:
                move_prompt += f'In the {idx + 1}st round, {role} choose to {move};\n'
            elif idx == 1:
                move_prompt += f'In the {idx + 1}nd round, {role} choose to {move};\n'
            elif idx == 2:
                move_prompt += f'In the {idx + 1}rd round, {role} choose to {move};\n'
            else:
                raise ValueError

    prompt = f'In this match, your card is {card}.\n' \
             f'{move_prompt}\n' \
             f'Your legal moves are: <Pass>, <Bet>.'

    return _construct_head_prompt() + '\n' + prompt


if __name__ == '__main__':
    prompt = _construct_head_prompt()
    obs_prompt = construct_observation_prompt(
        {'card': 0, 'moves': 'pb', 'player_idx': 0})
    prompt += '\n' + obs_prompt
    print(prompt)
