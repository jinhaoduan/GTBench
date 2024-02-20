

def _construct_head_prompt():
    return """Breakthrough is a two-player game played on a rectangular board. Players take turns moving their pieces, which can move one space straight or diagonally forward if the target square is empty. A piece can also move diagonally forward to capture an opponent's piece. Capturing is optional, and a player can only capture one piece per turn. The goal is to be the first to reach the opponent's home row, the farthest row from the player. If all of a player's pieces are captured, they lose. The game does not allow draws, as pieces can only move forward or be captured.The Breakthrough board is identified by columns labeled start from A (from left to right) and rows numbered 1 to 8 (from bottom to top). The intersection of a column and a row specifies a unique square on the board."""


def construct_observation_prompt(observations):

    legal_actions = observations.get('legal_moves', [])
    opponent_actions = observations.get('opponent_moves', [])
    agent_actions = observations.get('self_moves', [])
    board_str = observations.get('board', '')
    if board_str == '':
        board_preview = ''
    else:
        board_preview = f"The board now looks like :\n{board_str} \nAmong which, the letter 'b' represents black piece, while the letter 'w' represents white piece.\n And the character '.' represents vacant space.\n And the numbers in the board are the indexes of the rows."

    assert len(legal_actions) != 0

    if len(opponent_actions) == 0:
        opponent_prompt = 'Your opponent does not have any action so far.'
    else:
        finished_moves = ' and '.join(opponent_actions)
        opponent_prompt = f'Your opponent has finished actions: {finished_moves}.'

    if len(agent_actions) == 0:
        agent_prompt = 'You do not have any action so far.'
    else:
        finished_moves = ', '.join(agent_actions)
        agent_prompt = f'You have finished actions: {finished_moves}.'

    legal_pos = ' or '.join(legal_actions)
    legal_position_prompt = f'Currently, the legal actions are: {legal_pos}.'

    prompt = f'{_construct_head_prompt()}\n\n{board_preview}\n{opponent_prompt} {agent_prompt}\n\n{legal_position_prompt}'

    return prompt
