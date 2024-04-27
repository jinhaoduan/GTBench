
def _construct_head_prompt():
           
    prompt = "Crazy Eights is a shedding-type card game with a standard 52-card deck. The object of the game is to be the first player to discard all of their cards. There are two players in this game.\n" 
    prompt += "Seven cards are dealt to each player. The remaining cards of the deck are placed face down at the center of the table as the stock pile. The top card is then turned face up to start the game as the first card in the discard pile.\n" 
    prompt += "In each player's turn, it needs to play a card that either match the suit or the rank of the card on the top of the discard pile. And then place this card on the discard pile top for the next player to match. \n" 
    prompt += "A player can play an 8 as a wild card, however, at anytime. If it does, it needs to nominate a card suit needs to be nominated for the next player to match." 
    prompt += "A player can also decide to draw cards from the stock pile. Notice that it is the only action available if it does not have a available card to play at its turn. But it doesn't prevent the player to draw cards even if it has playable.\n" 
    prompt += "If a player plays a card, it cannot draw at the current turn anymore. A player cannot skip a turn.\n" 
    prompt += "If there are no remaining cards in the stock pile, all cards in the discard pile are shuffled and add those cards are added to the stock pile.\n"
    prompt += "The game ends once a player exhausted all cards in its hand.\n"

    prompt += "You are playing CrazyEights with the opponent. The actions are denoted by <draw> for drawing a card from the stockpile, <play <card>> for putting on the discard pile the specific card, and <play8 <card> <suit_to_change>> for playing a 8 wild card and nominating a new suit to change."

    return prompt 


'''
Observation Prompt to Create: 

Your current hand contains <CARDS>. 
You must match the top card <TOP CARD> with the next card you play or must draw from the stockpile. 
The moves in the past from you and your opponent are <MOVES>.
'''


# TO-DO: 
def construct_observation_prompt(observations):

    prompt = ""

    # card_mapping = {
    #     '1': 'Ace (A)',
    #     '2': '2 (2)',
    #     '3': '3 (3)', 
    #     '4': '4 (4)', 
    #     '5': '5 (5)', 
    #     '6': '6 (6)', 
    #     '7': '7 (7)', 
    #     '8': '8 (8)', 
    #     '9': '9 (9)', 
    #     '10': '10 (10)', 
    #     '11': 'Jack (J)', 
    #     '12': 'Queen (Q)', 
    #     '13': 'King (K)'
    # }

    # suit_mapping = {
    #     'C': 'Clubs (C)', 
    #     'D': 'Diamonds (D)', 
    #     'H': 'Hearts (H)', 
    #     'S': 'Spades (S)'
    # }


    cards = observations.get('cards', []) 
    top_card = observations.get('top_card', [])
    moves = observations.get('moves', [])
    player_idx = observations.get('player_idx', "")

    # To-Do: Cards may involve mapping 
    CARDS = "" # convert the above cards variable to a string representation for CARDS 
    TOP_CARD = "" # convert the above top_card variable to a string representation for TOP_CARD 
    MOVES = "" # below for-loop structure converts the moves variable to a stirng represent

    card_prompt = f"Your current hand contains {CARDS}. "
    top_prompt = f"You must match the top card {TOP_CARD} with the next card you play or must draw from the stockpile."
    moves_prompt = ""



    # need to figure out the coding schematic for the moves 

    if moves != None: 
        
        MOVES = ""

        moves_prompt

        for idx, m in enumerate(moves): 

            if (player_idx + 1) % (idx + 1) == 0:
                role = 'your'
            else:
                role = 'the opponent\'s'

            if m.startswith('d'): 
                action_prompt = "to draw a card" 
            elif m.startswith('p8'): 
                card_played = None
                action_prompt = f"to play {card_played}"  
            elif m.startswith('p'): 
                card_played = None
                suit_nominated = None
                action_prompt = f"to play {card_prompt} and chose to switch the suit to {suit_nominated}"
            else: 
                raise ValueError
            
            move_prompt = f"In round {idx}, {role} move was {action_prompt}."
            
            MOVES+=move_prompt
        
        moves_prompt = f"The moves in the past from you and your oppoent are: {MOVES}."

    prompt += _construct_head_prompt() + "\n" + card_prompt + "\n" + top_prompt + "\n" + moves_prompt

    return prompt