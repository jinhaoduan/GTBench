

def _construct_head_prompt():
    return """Dots and Boxes is a two-player game of strategy, played on a grid of 3 x 3 dots. The game starts with an empty grid of dots. Each player take turns adding a single line between two unjoined adjacent dots. A valid move consists either of a horizontal or vertical line, not a diagonal one. A player who completes the fourth side of a 1x1 box earns one point and takes another turn. A point is typically recorded by placing a mark that identifies the player in the box, such as an initial. The game ends when no more lines can be placed. The winner is the player with the most points. Each move is recorded using a coordinate system, where the grid columns are labeled with letters (A, B, C) and the rows with numbers (1, 2, 3). A move is noted by specifying the coordinates of the two dots that the line connects. For a horizontal line, the coordinate is written like <A1-B1>, connecting the dot at A1 to the one directly to its right at B1. For a vertical line, the coordinate is written like <A1-A2>, connecting the dot at A1 to the one directly below it at A2. Again, diagonal moves like <A1-B2> or <B1-C2> that consistute both a hotizontal and vertical step are not allowed."""

def construct_observation_prompt(observations):
    legal_actions = observations.get('legal_moves', [])
    opponent_actions = observations.get('opponent_moves', [])
    agent_actions = observations.get('self_moves', [])

    assert len(legal_actions) != 0

    if len(opponent_actions) == 0:
        opponent_prompt = 'Your opponent does not have any move so far.'
    else:
        finished_moves = ','.join(opponent_actions)
        opponent_prompt = f'Your opponent has finished moves: {finished_moves}'

    if len(agent_actions) == 0:
        agent_prompt = 'You do not have any move so far.'
    else:
        finished_moves = ','.join(agent_actions)
        agent_prompt = f'You have finished moves: {finished_moves}'

    legal_pos = ','.join(legal_actions)
    legal_position_prompt = f'Currently, the legal actions are {legal_pos}'

    prompt = f'{_construct_head_prompt()}\n\n{opponent_prompt} {agent_prompt} {legal_position_prompt}'


    return prompt
