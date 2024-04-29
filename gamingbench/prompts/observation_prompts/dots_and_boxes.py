

def _construct_head_prompt():
    return """Dots and Boxes is a two-player game of strategy and cunning, played on a grid of 3 x 3 dots. Players alternate turns, drawing a single line to connect two adjacent dots either horizontally or vertically. The objective is to complete the fourth side of a 1x1 box, which allows the player to claim that box by placing their initial inside it. Claiming a box grants the player an additional turn. The game proceeds until all possible lines are drawn and no further boxes can be formed. The winner is determined by the total count of boxes claimed. Each move is recorded using a coordinate system, where the grid columns are labeled with letters (A, B, C, ...) and the rows with numbers (1, 2, 3, ...). A move is noted by specifying the coordinates of the two dots that the line connects. For a horizontal line, the coordinate is written as <A1−B1>, connecting the dot at A1 to the one directly to its right at B1. For a vertical line, the coordinate is written as <A1−A2>, connecting the dot at A1 to the one directly below it at A2."""

def construct_observation_prompt(observations):
    legal_actions = observations.get('legal_moves', [])
    #print("in prompts: legal actions")
    #print(legal_actions)
    opponent_actions = observations.get('opponent_moves', [])
    agent_actions = observations.get('self_moves', [])
    #print("in prompts: opponent actions")
    #print(opponent_actions)
    #print("in prompts: agent actions")
    #print(agent_actions)

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
    legal_position_prompt = f'Currently, the legal positions are {legal_pos}'

    prompt = f'{_construct_head_prompt()}\n{opponent_prompt} {agent_prompt} {legal_position_prompt}'
    

    return prompt
