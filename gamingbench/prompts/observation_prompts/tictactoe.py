

def _construct_head_prompt():
    return """Tic Tac Toe is a two-player game played on a grid. Players take turns marking a space with their respective symbols. The goal is to get 3 of one\'s own symbols in a row, either horizontally, vertically, or diagonally, before the opponent does. If all nine squares are filled and no player has three in a row, the game is a draw. The Tic Tac Toe game is played on a 3 by 3 grid, with the winning length as 3.
Each move is represented by a string consisting of two parts: the column (C) and the row (R), in that order. For instance, C1R2 means the movement at the position of the first column and the second row of the grid. You are playing this game with the user (opponent)."""

def construct_observation_prompt(observations):
    """
    :param observations: tic tac toe observation
    :return: observation prompts
    """

    legal_moves = observations.get('legal_moves', [])
    opponent_moves = observations.get('opponent_moves', [])
    self_moves = observations.get('self_moves', [])

    assert len(legal_moves) != 0

    if len(opponent_moves) != 0 or len(self_moves) != 0:
        if len(opponent_moves) == 0:
            opponent_prompt = ''
        else:
            finished_moves = ', '.join(opponent_moves)
            opponent_prompt = f'Your opponent has finished actions: {finished_moves}.'
        if len(self_moves) == 0:
            agent_prompt = ''
        else:
            finished_moves = ', '.join(self_moves)
            agent_prompt = f'You have finished actions: {finished_moves}.'
        finished_move_prompt = f'{opponent_prompt} {agent_prompt}'
    else:
        finished_move_prompt = f'You are the first to go.'

    legal_pos = ', '.join(legal_moves)
    legal_position_prompt = f'Currently, the legal actions are {legal_pos}.'

    prompt = f'{_construct_head_prompt()}\n{finished_move_prompt}\n{legal_position_prompt}'

    return prompt
