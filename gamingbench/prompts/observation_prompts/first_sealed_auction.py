
def _construct_head_prompt():
    return 'A first-price sealed-bid auction (FPSBA) is a common type of auction. It is also known as blind auction. ' \
           'In this type of auction, all bidders simultaneously submit sealed bids so that no bidder knows the bid of any other participant. ' \
           'The highest bidder pays the price that was submitted.' \
           '\n' \
           'Each action is represented by <x> where x refers to the bid.'


def construct_observation_prompt(observations):

    legal_moves = observations['legal_moves']
    valuation = observations['valuation']
    legal_move_str = ', '.join(legal_moves)

    prompt = f'Now, you are in an auction with an opponent.You want to win the object and at the same time, you budget is {valuation}. Your bid must be strictly lower than or equal to {valuation}.' \
             f'You shall bid wisely against your opponent \n' \
             f'Your opponent also has an expected valuation and you don not know it.' \
             f'\n\n' \
             f'The legal actions are: {legal_move_str}. '
    return _construct_head_prompt() + '\n' + prompt
