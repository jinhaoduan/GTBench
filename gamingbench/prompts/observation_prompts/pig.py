
def _construct_head_prompt():
    return """Pig is a fast-paced dice game where players risk accumulating points with each roll but risk losing them all if they roll a 1. Each player must decide when to stop rolling and bank their points, aiming to be the first to reach 100 points.
    You are playing Pig with the other. """


def construct_observation_prompt(observations):

    agent_current_score = observations['self_current_score']
    opponent_current_score = observations['opponent_current_score']
    turn_total_score = observations['turn_total_score']
    legal_moves = observations['legal_moves']
    legal_move_str = ', '.join(legal_moves)

    prompt = f"""Right now, your current score is {agent_current_score} and your opponent's current score is {opponent_current_score}. In this turn, you have earned {turn_total_score} score.
    
    The legal moves are: {legal_move_str}."""

    return _construct_head_prompt() + '\n' + prompt


